import tkdesigner.figma.endpoints as endpoints
from tkdesigner.figma.frame import Frame

from tkdesigner import __version__
from tkdesigner.inspection import DesignReport, build_design_report
from tkdesigner.template import CLASS_TEMPLATE, PAGES_TEMPLATE, TEMPLATE

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Optional, Tuple
from uuid import uuid4


FRAME_NODE_TYPES = {"FRAME", "COMPONENT", "COMPONENT_SET", "INSTANCE"}
FRAME_CONTAINER_TYPES = {"CANVAS", "SECTION"}


@dataclass(frozen=True)
class GenerationResult:
    """Details about a successfully generated project."""

    output_path: Path
    code_files: Tuple[Path, ...]
    asset_files: Tuple[Path, ...]
    manifest_path: Optional[Path]
    report: Optional[DesignReport]


class Designer:
    def __init__(
        self,
        token,
        file_key,
        output_path: Path,
        *,
        node_id=None,
        template_style="script",
        theme="",
    ):
        self.output_path = output_path
        self.figma_file = endpoints.Files(token, file_key)
        self.file_data = self.figma_file.get_file()
        self.node_id = node_id
        self.template_style = template_style
        self.theme = theme

    def to_code(self, frame_nodes=None) -> list:
        """Return generated code for each frame."""
        frame_nodes = frame_nodes or self._target_frame_nodes()

        if not frame_nodes:
            raise RuntimeError(
                "No Figma frames were found. Select a frame in Figma and copy "
                "its URL, or add a top-level frame to the file.")

        self._prefetch_image_exports(frame_nodes)

        frames = []
        for frame_counter, frame_node in enumerate(frame_nodes):
            frame = Frame(
                frame_node,
                self.figma_file,
                self.output_path,
                frame_counter,
                theme=self.theme,
            )
            frame.page_index = frame_counter
            frame.class_name = f"Page{frame_counter}"
            frame.assets_rel_path = frame.assets_path.relative_to(
                self.output_path).as_posix()
            frames.append(frame)

        if self.template_style == "pages":
            return [self._to_pages_code(frames)]

        template = CLASS_TEMPLATE if self.template_style == "class" else TEMPLATE
        return [frame.to_code(template) for frame in frames]

    def inspect(self) -> DesignReport:
        """Return a read-only preview without downloading assets."""
        frame_nodes = self._target_frame_nodes()
        if not frame_nodes:
            raise RuntimeError(
                "No Figma frames were found. Select a frame in Figma and copy "
                "its URL, or add a top-level frame to the file.")
        return build_design_report(
            file_data=self.file_data,
            file_key=self.figma_file.file_key,
            selected_node_id=self.node_id,
            template=self.template_style,
            frame_nodes=frame_nodes,
        )

    def _prefetch_image_exports(self, frame_nodes):
        item_ids = []
        for frame_node in frame_nodes:
            item_ids.extend(Frame.image_export_ids(frame_node))
        if item_ids:
            self.figma_file.get_images(item_ids)

    def _to_pages_code(self, frames):
        from jinja2 import Template

        return Template(PAGES_TEMPLATE).render(
            pages=frames,
            window=frames[0],
            assets_path="assets",
            theme=self.theme,
        )

    def _target_frame_nodes(self):
        document = self.file_data.get("document", {})

        if self.node_id:
            selected_node = self._find_node(document, self.node_id)
            if selected_node is None:
                raise RuntimeError(
                    f"Node `{self.node_id}` was not found in the Figma file.")
            if self._is_frame_node(selected_node):
                return [selected_node]
            selected_frames = list(self._collect_frame_nodes(selected_node))
            if selected_frames:
                return selected_frames
            raise RuntimeError(
                f"Selected node `{self.node_id}` is not a frame and does not "
                "contain any frames.")

        frame_nodes = []
        for page in document.get("children", []):
            frame_nodes.extend(self._collect_frame_nodes(page))
        return frame_nodes

    def _collect_frame_nodes(self, node):
        node_type = node.get("type")
        if self._is_frame_node(node):
            yield node
            return
        if node_type not in FRAME_CONTAINER_TYPES and node_type is not None:
            return
        for child in node.get("children", []) or []:
            yield from self._collect_frame_nodes(child)

    def _find_node(self, node, node_id):
        if node.get("id") == node_id:
            return node
        for child in node.get("children", []) or []:
            result = self._find_node(child, node_id)
            if result is not None:
                return result
        return None

    def _is_frame_node(self, node):
        return (
            "absoluteBoundingBox" in node
            and node.get("type") in FRAME_NODE_TYPES
        )

    def design(self, *, clean=False, write_manifest=True) -> GenerationResult:
        """Generate into a staging directory, then atomically replace output.

        A failed API call or image download can no longer leave the user's last
        successful build half-deleted or partially updated.
        """
        target = self.output_path
        if target.exists() and not target.is_dir():
            raise RuntimeError(f"`{target}` already exists and is not a directory.")
        if target.exists() and any(target.iterdir()) and not clean:
            raise RuntimeError(
                f"`{target}` is not empty. Pass `clean=True` to replace it.")

        target.parent.mkdir(parents=True, exist_ok=True)
        stage = target.parent / f".{target.name}.tkdesigner-{uuid4().hex}"
        report = self.inspect() if hasattr(self, "file_data") else None
        original_output = self.output_path

        try:
            self.output_path = stage
            stage.mkdir(parents=True)
            code = self.to_code()
            code_paths = []
            for index, source in enumerate(code):
                # Keep gui.py as the first filename for compatibility with the
                # original tutorials and existing integrations.
                filename = "gui.py" if index == 0 else f"gui{index}.py"
                path = stage / filename
                path.write_text(source, encoding="UTF-8")
                code_paths.append(path)

            manifest_path = None
            if write_manifest:
                manifest_path = stage / "tkdesigner.json"
                manifest_path.write_text(
                    self._manifest_json(stage, report), encoding="UTF-8")

            asset_paths = tuple(
                path for path in sorted(stage.rglob("*"))
                if path.is_file() and path.parent != stage
            )
            self._commit_stage(stage, target)
        except Exception:
            if stage.exists():
                shutil.rmtree(stage)
            raise
        finally:
            self.output_path = original_output

        return GenerationResult(
            output_path=target,
            code_files=tuple(target / path.name for path in code_paths),
            asset_files=tuple(target / path.relative_to(stage) for path in asset_paths),
            manifest_path=(target / "tkdesigner.json" if manifest_path else None),
            report=report,
        )

    def _manifest_json(self, stage: Path, report: Optional[DesignReport]) -> str:
        files = [
            str(path.relative_to(stage))
            for path in sorted(stage.rglob("*"))
            if path.is_file() and path.name != "tkdesigner.json"
        ]
        payload = {
            "schema_version": 1,
            "generator": {
                "name": "Tkinter Designer",
                "version": __version__,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
            "settings": {
                "template": getattr(self, "template_style", "script"),
                "theme": getattr(self, "theme", "") or None,
            },
            "design": report.to_dict() if report is not None else None,
            "files": files,
        }
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"

    @staticmethod
    def _commit_stage(stage: Path, target: Path):
        backup = None
        try:
            if target.exists():
                backup = target.parent / f".{target.name}.backup-{uuid4().hex}"
                target.replace(backup)
            stage.replace(target)
        except Exception:
            if backup is not None and backup.exists() and not target.exists():
                backup.replace(target)
            raise
        else:
            if backup is not None and backup.exists():
                try:
                    shutil.rmtree(backup)
                except OSError:
                    # The new build is already committed. A stale hidden backup
                    # is safer than reporting a false generation failure.
                    pass
