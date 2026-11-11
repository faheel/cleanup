#! /usr/bin/env python3

import json
import sys
from os.path import dirname, join, realpath

sys.path.append(join(dirname(realpath(__file__)), '..', 'cleanup'))

import cleanup.cleanup as cleanup_mod
from cleanup.cleanup import cleanup


def test_cleanup_survives_corrupt_revert_info(tmp_path, monkeypatch):
    target = tmp_path / 'docs'
    target.mkdir()
    (target / 'note.txt').write_text('hi')
    bad = tmp_path / 'revert_info.json'
    bad.write_text('{not valid json')
    monkeypatch.setattr(cleanup_mod, 'REVERT_INFO_FILE', str(bad))

    cleanup(str(target), silent=True)

    assert not (target / 'note.txt').exists()
    data = json.loads(bad.read_text())
    assert data[str(target)][0]['name'] == 'note.txt'
