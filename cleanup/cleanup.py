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

from colored import stylize, fg, attr
from docopt import docopt

from .file_types import FILE_TYPES

REVERT_INFO_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'revert_info.json')


def get_longest_extension(filename):
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
    print(action + ' ' + stylize(dir, fg('light_blue') + attr('bold'))
          + ':')


def print_move(move_action, file, file_type, revert=False, dry_run=False):
    if revert:
        preposition = 'from'
    else:
        preposition = 'under'
    if dry_run:
        move_action = stylize(move_action, fg('yellow'))
    else:
        move_action = stylize(move_action, fg('green'))
    print(move_action + ' ' + stylize(file, attr('bold')) + ' ' + preposition + ' '
          + stylize(file_type, attr('bold')))


def print_file_error(error, file, file_type, dry_run=False):
    if dry_run:
        preposition = 'from'
    else:
        preposition = 'under'
    print(stylize(error, fg('red')) + ' ' + stylize(file, attr('bold')) + ' '
          + preposition + ' ' + stylize(file_type, attr('bold')))


def print_dir_error(error, dir):
    print(stylize(error, fg('red')) + ': ' + stylize(dir, fg('light_blue')
                                                          + attr('bold')))


def print_complete(operation):
    print(operation + ' ' + stylize('complete', fg('green')) + '!')


def revert(dir_path, dry_run, silent):
    abs_dir = os.path.abspath(dir_path)
    try:
        revert_info = read_revert_info()
        if revert_info.get(abs_dir):
            file_info_list = revert_info[abs_dir]
        else:
            # revert info about the specified directory is not available
            raise Exception
    except:
        # revert info file doesn't exist, so cannot perform a revert
        print('Nothing to do.')
        exit()
    
    if dry_run:
        print_cleaning('When reverting cleanup of', abs_dir)
    elif not silent:
        print_cleaning('Reverting cleanup of', abs_dir)
    for file_info in file_info_list:
        file_type = file_info['type']
        file = file_info['name']
        prev_path = os.path.join(abs_dir, file_type, file)
        new_path = os.path.join(abs_dir, file)
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
        revert_info.pop(abs_dir)
        save_revert_info(revert_info)


def main():
    arguments = docopt(__doc__)
    dir_path = arguments['<dir>']   # path to the directory to be cleaned
    silent = arguments['--silent']
    dry_run = arguments['--dry-run']
    to_revert = arguments['--revert']

    if to_revert:
        revert(dir_path, dry_run, silent)
    else:
        root_dir, dir_list, file_list = next(os.walk(dir_path), (None, [], []))
        if not root_dir:
            print_dir_error('The specified directory does not exist',
                            os.path.abspath(dir_path))
            exit()
        abs_path = os.path.abspath(root_dir)
        if len(file_list) == 0:
            print('Nothing to do.')
            exit()
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


if __name__ == '__main__':
    main()
