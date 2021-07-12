from tkdesigner.figma_api import FigmaUser
from tkdesigner.generator.frame import Frame
from tkdesigner.template import TEMPLATE
from pathlib import Path


class Designer:
    def __init__(self, token, file_key, output_path: Path):
        self.figma_user = FigmaUser(token)
        self.file_key = file_key
        self.output_path = output_path
        self.file_data = self.figma_user.get_files(self.file_key)

    def to_code(self) -> str:
        window_data = self.file_data["document"]["children"][0]["children"][0]

        frame = Frame(
            window_data, self.file_key, self.figma_user, self.output_path)
        return frame.to_code(TEMPLATE)

    def design(self):
        code = self.to_code()
        self.output_path.joinpath("gui.py").write_text(code)
