from requests import get
from eel import init, start
import os, sys

# for library in ("", "index.min.js"):
#     with open(library, "w") as f:
#         f.write(str(get("https://cdn.jsdelivr.net/npm/pixi-live2d-display/dist/"+library).content))

init("../src/CubismSdkForWeb-5-r.4/Samples/TypeScript/Demo")
start("index.html", size=(720,480))
