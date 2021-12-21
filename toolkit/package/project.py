import os
import os.path as osp
from pathlib import Path
from toolkit.utils.files import touch


def manage_project(crabs_folder: str = '.crabs', *files) -> None:
    if osp.exists(crabs_folder):
        return

    files = (Path(crabs_folder, f) for f in files)

    for file in files:
        file
