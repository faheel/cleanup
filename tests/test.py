#! /usr/bin/env python3

import sys
from os.path import join, dirname, realpath

from huepy import *

sys.path.append(join(dirname(realpath(__file__)), '..', 'cleanup'))
# import from cleanup after adding it's path to the system path
from cleanup.cleanup import cleanup, revert, read_revert_info

TEST_FILES_DIR = join(dirname(realpath(__file__)), 'files')


def test_cleanup():
    print(bold(yellow('Testing cleanup:')))
    cleanup(TEST_FILES_DIR)


def test_revert():
    print()
    print(bold(yellow('Testing cleanup revert:')))
    revert(TEST_FILES_DIR)


if __name__ == '__main__':
    test_cleanup()
    test_revert()
