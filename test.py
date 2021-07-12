from tkdesigner.generator.frame import Frame
from tkdesigner.figma_api import FigmaUser

import os
from pathlib import Path


token = os.environ.get("FIGMA_TOKEN")
user = FigmaUser(token)
print(user)

output_path = Path("/tmp/generated").expanduser().resolve()
output_path.mkdir(exist_ok=True)
output_path.joinpath("assets").mkdir(exist_ok=True)

# https://www.figma.com/file/vApXvnJ9cvz0RHg96kRGD2/Untitled?node-id=0%3A1
# https://www.figma.com/file/WVLnulVsI177tvnxSdqOUZ/Untitled?node-id=0%3A1

file_key = "WVLnulVsI177tvnxSdqOUZ"

data = user.get_files(file_key)
window_json = data["document"]["children"][0]["children"][0]
fr = Frame(window_json, file_key, user, output_path)

with open(output_path.joinpath("main.py"), "w") as main:
    main.write(fr.to_code())
