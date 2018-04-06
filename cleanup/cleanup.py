#! /usr/bin/env python3

'''
Organise files in a directory into subdirectories based on their extensions.

Usage:
  cleanup [-d | -s] [-r] <dir>
  cleanup -h

Options:
  -d, --dry-run     Just display the changes that would be made, without
                    actually doing anything.
  -s, --silent      Do not display information while performing operations.
  -r, --revert      Revert previous cleanup of the directory.
  -h, --help        Display this help text.
'''

import io
import json
import os

from docopt import docopt
from huepy import *

from .file_types import FILE_TYPES

REVERT_INFO_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'revert_info.json')


def get_longest_extension(filename):
    '''
    Returns the longest known extension from the given filename
    '''
    parts = filename.split('.')
    if len(parts) > 3:
        # possible triple extension (.pkg.tar.xz)
        extension = '.'.join(parts[-3:]).upper()
        if FILE_TYPES.get(extension):
            return extension
    if len(parts) > 2:
        # possible double extension (.tar.gz)
        extension = '.'.join(parts[-2:]).upper()
        if FILE_TYPES.get(extension):
            return extension
    if len(parts) > 1:
        # possible single extension (.zip)
        extension = parts[-1].upper()
        if FILE_TYPES.get(extension):
            return extension
    return None


def save_revert_info(revert_info):
    with io.open(REVERT_INFO_FILE, 'w', encoding='utf8') as file:
        file.write(json.dumps(revert_info, ensure_ascii=False, sort_keys=True,
                              indent=4, separators=(',', ': ')))


def read_revert_info():
    with io.open(REVERT_INFO_FILE) as file:
        return json.load(file)


def print_cleaning(action, dir):
    print(action + ' ' + bold(lightblue(dir)) + ':')


def print_move(move_action, file, file_type, revert=False, dry_run=False):
    if revert:
        preposition = 'from'
    else:
        preposition = 'under'
    if dry_run:
        move_action = yellow(move_action)
    else:
        move_action = lightgreen(move_action)
    print(move_action + ' ' + bold(file) + ' ' + preposition + ' '
          + bold(file_type))


def print_file_error(error, file, file_type, dry_run=False):
    if dry_run:
        preposition = 'from'
    else:
        preposition = 'under'
    print(lightred(error) + ' ' + bold(file) + ' ' + preposition + ' '
          + bold(file_type))


def print_dir_error(error, dir):
    print(lightred(error) + ': ' + bold(lightblue(dir)))


def print_complete(operation):
    print(operation + ' ' + lightgreen('complete') + '!')


def revert(abs_path, dry_run=False, silent=False):
    '''
    Given the absolute path to a directory, it reverts the cleanup operation
    performed on it and moves back files to their original location, deleting
    empty folders that remain after files have been moved from them.
    '''
    try:
        revert_info = read_revert_info()
        if revert_info.get(abs_path):
            file_info_list = revert_info[abs_path]
        else:
            # revert info about the specified directory is not available
            raise Exception
    except:
        # revert info file doesn't exist, so cannot perform a revert
        print('Nothing to do.')
        return

    if dry_run:
        print_cleaning('When reverting cleanup of', abs_path)
    elif not silent:
        print_cleaning('Reverting cleanup of', abs_path)
    for file_info in file_info_list:
        file_type = file_info['type']
        file = file_info['name']
        prev_path = os.path.join(abs_path, file_type, file)
        new_path = os.path.join(abs_path, file)
        try:
            if dry_run:
                if os.path.exists(prev_path):
                    print_move('Will move back', file, file_type, revert=True, dry_run=True)
                else:
                    print_file_error('Will fail to move back', file, file_type, dry_run=True)
            else:
                os.renames(prev_path, new_path)
                if not silent:
                    print_move('Moved back', file, file_type, revert=True)
        except:
            print_file_error('Could not find', file, file_type)
    if not dry_run:
        if not silent:
            print_complete('Revert')
        revert_info.pop(abs_path)
        save_revert_info(revert_info)


def cleanup(abs_path, dry_run=False, silent=False):
    '''
    Given the absolute path to a directory, it organise files in that directory
    into subdirectories based on the files' extensions.
    '''
    root_dir, dir_list, file_list = next(os.walk(abs_path), (None, [], []))
    if not root_dir:
        print_dir_error('The specified directory does not exist', abs_path)
        return

    if len(file_list) == 0:
        print('Nothing to do.')
        return
    if dry_run:
        print_cleaning('When cleaning up', abs_path)
    elif not silent:
        print_cleaning('Cleaning up', abs_path)

    revert_list = []
    for file in file_list:
        extension = get_longest_extension(file)
        if extension:
            original_name = os.path.join(root_dir, file)
            file_type = FILE_TYPES[extension]
            new_name = os.path.join(root_dir, file_type, file)
            if dry_run:
                print_move('Will move', file, file_type, dry_run=True)
            else:
                revert_list.append({
                    'name': file,
                    'type': file_type
                })
                os.renames(original_name, new_name)
                if not silent:
                    print_move('Moved', file, file_type)
    if not dry_run:
        if not silent:
            print_complete('Cleanup')
        if os.path.exists(REVERT_INFO_FILE):
            revert_info = read_revert_info()
        else:
            revert_info = {}
        revert_info[os.path.abspath(root_dir)] = revert_list
        save_revert_info(revert_info)


def main():
    arguments = docopt(__doc__)
    dir_path = arguments['<dir>']   # path to the directory to be cleaned
    silent = arguments['--silent']
    dry_run = arguments['--dry-run']
    to_revert = arguments['--revert']

    abs_path = os.path.abspath(dir_path)
    if to_revert:
        revert(abs_path, dry_run, silent)
    else:
        cleanup(abs_path, dry_run, silent)


if __name__ == '__main__':
    main()
