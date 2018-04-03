#! /usr/bin/env python3

'''
Organise files in a directory into subdirectories.

Usage:
  cleanup [-d | -v] <dir>
  cleanup -h

Options:
  -d, --dry-run     Do not make any changes, just display them.
  -v, --verbose     Display information while performing operations.
  -h, --help        Display this help text.
'''

import os

from colored import stylize, fg, attr
from docopt import docopt

from file_types import FILE_TYPES


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


def print_cleaning(action):
    print(action + ' ' + stylize(root_dir, fg('light_blue') + attr('bold'))
          + ' ...')


def print_move(move_action, file, file_type):
    print(move_action + ' ' + stylize(file, attr('bold')) + ' under '
          + stylize(file_type, attr('bold')))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    dir_path = arguments['<dir>']   # path to the directory to be cleaned
    verbose = arguments['--verbose']
    dry_run = arguments['--dry-run']
    
    root_dir, dir_list, file_list = next(os.walk(dir_path), (None, [], []))
    if dry_run:
        print_cleaning('When cleaning up')
    elif verbose:
        print_cleaning('Cleaning up')
    for file in file_list:
        extension = get_longest_extension(file)
        if extension:
            original_name = os.path.join(root_dir, file)
            file_type = FILE_TYPES[extension]
            new_name = os.path.join(root_dir, file_type, file)
            if dry_run:
                print_move('Will move', file, file_type)
            else:
                os.renames(original_name, new_name)
                if verbose:
                    print_move('Moved', file, file_type)
    if not dry_run and verbose:
        print(stylize('Done', fg('green')) + '!')
