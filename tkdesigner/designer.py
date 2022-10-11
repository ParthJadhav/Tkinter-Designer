import tkdesigner.figma.endpoints as endpoints
from tkdesigner.figma.frame import Frame

from tkdesigner.template import TEMPLATE

from pathlib import Path

class Designer:
    def __init__(self, token, file_key, output_path: Path):
        self.output_path = output_path
        self.figma_file = endpoints.Files(token, file_key)
        self.file_data = self.figma_file.get_file()

    def to_code(self) -> str:
        """Return main code.
        """
        frames = [];
        for f in self.file_data["document"]["children"][0]["children"]:
            try:
                frame = Frame(f, self.figma_file, self.output_path)
            except Exception:
                raise Exception("Frame not found in figma file or is empty")
            frames.append(frame.to_code(TEMPLATE))
        return frames


    def design(self):
        """Write code and assets to the specified directories.
        """
        code = self.to_code()
        for index in range(len(code)):
            self.output_path.joinpath(f"frame{index}.py").write_text(code[index], encoding='UTF-8')
