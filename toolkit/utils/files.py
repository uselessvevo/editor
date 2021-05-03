#   Copyright @ Crab Dudes Developers
#   Licensed under the terms of the MIT license
#   File files.py - 04.03.2021, 0:23

import os
import json
from pathlib import Path


def read_json(file, hang_on_error=True, default=None):
    """
    Read json file

    Args:
        file (str) - file path
        hang_on_error (bool) - set false if you need to skip the error
        default (Any) - default value if error occurred
    Returns:
        decoded data
    """
    try:
        with open(file, encoding='utf-8') as output:
            return json.load(output)

    except (OSError, FileNotFoundError, json.decoder.JSONDecodeError) as err:
        if not hang_on_error:
            return default
        else:
            raise err


def read_json_files(files, skip_error=True):
    """
    Args:
        files (List[str]): list of files
        skip_error (bool): set True if you need to skip error
    """
    # Clear duplicates
    files = set(files)
    collect = {}

    for file in files:
        # Get file without path and extension
        key = os.path.basename(file)
        key = os.path.splitext(key)[0]

        try:
            with open(file, encoding='utf-8') as output:
                collect[key] = json.load(output)

        except (OSError, FileNotFoundError, json.decoder.JSONDecodeError) as err:
            if skip_error:
                collect[key] = {}
            else:
                raise err

    return collect


def write_json(file, data, mode='w'):
    """
    Args:
        data (dict): data to save
        file (str): file path
        mode (str): write mode
    """
    try:
        data = json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False)
        with open(file, mode, encoding='utf-8') as output:
            output.write(data)

    except (OSError, FileNotFoundError, json.decoder.JSONDecodeError) as err:
        raise err


def update_json(file, data):
    copy = read_json(file)
    copy.update(data)
    write_json(file, copy)


# Managers

def write_folder_info(folder: str) -> (float, float):
    """
    Get current folder size
    Args:
        folder (str) - folder name
    Returns:
        current folder size and written in file folder size
    """
    written_folder_size = current_folder_size = 0
    folder_info_file = Path(folder, 'size.json')

    # Create folder size entry
    for file in Path(folder).rglob('*.*'):
        if file.is_file():
            current_folder_size += file.stat().st_size

    # Update file if exists
    if folder_info_file.exists():
        written_folder_size = int(folder_info_file.read_text())
    else:
        folder_info_file.write_text(str(current_folder_size))

    return current_folder_size, written_folder_size


def make_assets_manifest(prefix, root, folder, file_formats=None, path_slice=-2):
    """
    Collect files from folder and restore manifest.json files

    Args:
        prefix (str): prefix to file (f.e. "shared/icons/icon.svg")
        folder (str): folder path
        path_slice (int): path slice
        file_formats (list|tuple): list of file formats

    Returns:
        hash table of formatted file paths (str)
    """
    folder = Path(folder)
    if not folder.exists():
        raise OSError('Path doesn\'t exit')

    file = folder.joinpath('assets.json')

    if not file_formats:
        file_formats = []

    collect = {}

    file_formats = set(f'*.{i}' for i in file_formats)
    for file_format in file_formats:
        for file in folder.rglob(file_format):
            key = f'{prefix}/{"/".join(file.parts[path_slice:])}'
            collect.update({
                key: str(file).replace(root + '\\', '').replace('\\', '/')
            })

    if not file.exists():
        write_json(file, collect)

    return collect


readJson = read_json
readJsonFiles = read_json_files
