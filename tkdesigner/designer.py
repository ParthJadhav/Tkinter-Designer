import tkdesigner.figma.endpoints as endpoints
from tkdesigner.figma.frame import Frame

from tkdesigner.template import TEMPLATE

from pathlib import Path


CODE_FILE_NAME = "gui.py"


class Designer:
    def __init__(self, token, file_key, output_path: Path):
        self.output_path = output_path
        self.figma_file = endpoints.Files(token, file_key)
        self.file_data = self.figma_file.get_file()

    def to_code(self) -> str:
        """Return main code.
        """
        window_data = self.file_data["document"]["children"][0]["children"][0]

        frame = Frame(window_data, self.figma_file, self.output_path)
        return frame.to_code(TEMPLATE)

    def design(self):
        """Write code and assets to the specified directories.
        """
        code = self.to_code()
        self.output_path.joinpath(CODE_FILE_NAME).write_text(code)
