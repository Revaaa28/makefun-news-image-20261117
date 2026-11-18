"""Ship the committed broadsheet image as the entry artifact.

The picture is drawn by compose.py and committed in this repository as
entry.png. When the grader runs this program (twice, offline, with no
network), it places an exact copy of that picture at entry.png inside
the output directory named by MAKEFUN_OUTPUT_DIR, defaulting to
/output when the variable is unset.

Standard library only. Both runs write byte-identical files, because
the program only copies bytes that are already committed.
"""

from os import environ, makedirs
from pathlib import Path

IMAGE = Path(__file__).resolve().parent / "entry.png"


def install():
    """Copy the committed image into the output directory.

    A plain byte copy: nothing is re-encoded, so the installed file is
    identical to the committed one on every run.
    """
    if not IMAGE.is_file():
        raise SystemExit("committed entry image is missing: " + str(IMAGE))
    out = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    makedirs(out, exist_ok=True)
    target = out / "entry.png"
    target.write_bytes(IMAGE.read_bytes())
    print("installed " + str(target) + " (" + str(target.stat().st_size) + " bytes)")


install()
