import tkdesigner.figma.endpoints as endpoints
from tkdesigner.figma.frame import Frame

from tkdesigner.template import CLASS_TEMPLATE, PAGES_TEMPLATE, TEMPLATE

from pathlib import Path
import shutil


FRAME_NODE_TYPES = {"FRAME", "COMPONENT", "COMPONENT_SET", "INSTANCE"}
FRAME_CONTAINER_TYPES = {"CANVAS", "SECTION"}


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

    def to_code(self) -> list:
        """Return generated code for each frame."""
        frame_nodes = self._target_frame_nodes()

        if not frame_nodes:
            raise RuntimeError(
                "No Figma frames were found. Select a frame in Figma, copy "
                "its URL, and make sure the frame is not empty.")

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
            frame.assets_rel_path = frame.assets_path.relative_to(self.output_path)
            frames.append(frame)

        if self.template_style == "pages":
            return [self._to_pages_code(frames)]

        template = CLASS_TEMPLATE if self.template_style == "class" else TEMPLATE
        return [frame.to_code(template) for frame in frames]

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
        return "absoluteBoundingBox" in node and node.get("type") in FRAME_NODE_TYPES and bool(node.get("children"))

    def design(self, *, clean=False):
        """Write code and assets to the specified directories."""
        if clean and self.output_path.exists():
            shutil.rmtree(self.output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

        code = self.to_code()
        for index in range(len(code)):
            # tutorials on youtube mention `python3 gui.py` added the below check to keep them valid
            if (index == 0):
                self.output_path.joinpath("gui.py").write_text(code[index], encoding='UTF-8')
            else:
                self.output_path.joinpath(f"gui{index}.py").write_text(code[index], encoding='UTF-8')
