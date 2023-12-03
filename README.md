# CleanUp

[![GitHub Actions][gh-actions-shield]][gh-actions-link]
[![PyPI][pypi-shield]][pypi-link]
[![License][license-shield]][license-link]

A simple command line utility that organises files in a directory into subdirectories based on the files' extensions.

## Usage

![Usage](https://i.imgur.com/iATfu3Y.png)

When run without any option, it organises the files in the specified directory into subdirectories based on the files' extensions.

### Options

* #### `-d`, `--dry-run`
  
  Just displays the changes that would be made, without actually doing anything.
  
  ```bash
  cleanup -d path/to/dir        # dry run the cleanup
  cleanup -dr path/to/dir       # dry run the reverting a cleanup
  ```

* #### `-s`, `--silent`
  
  Prevents displaying any information while performing operations. Errors, however, are displayed irrespective of whether this option is enabled or not.

  ```bash
  cleanup -s path/to/dir        # silently cleanup
  cleanup -sr path/to/dir       # silently revert a cleanup
  ```

* #### `-r`, `--revert`
  
  Reverts the cleanup of a directory. Note that for this to work, the specified directory should have been cleaned up before.

  ```bash
  cleanup -r path/to/dir        # revert the cleanup of a directory
  ```

* #### `-h`, `--help`
  
  Displays the help text.

  ```bash
  cleanup -h
  ```

## Development

### Setup

1. Clone the repo and `cd` into it.

2. Set up a Python 3 virtual environment using [pipenv](https://docs.pipenv.org):
   ```bash
   pipenv --three         # create Python 3 virtual environment
   pipenv install --dev   # install all dependencies
   pipenv shell           # activate virtual environment shell
   ```

3. The cleanup script can now be run from the root directory of the project:
   ```bash
   python3 -m cleanup.cleanup -h
   ```

### Test

Make sure you're in the root directory of the project. You can then run the test using:
```bash
python3 -m tests.test
```

## License

This project is licensed under the terms of the [MIT license][license-link].


[gh-actions-shield]: https://img.shields.io/github/actions/workflow/status/faheel/cleanup/ci.yml?style=for-the-badge&logo=github
[gh-actions-link]: https://github.com/faheel/cleanup/actions/workflows/ci.yml
[pypi-shield]: https://img.shields.io/pypi/v/cleanup.svg?style=for-the-badge
[pypi-link]: https://pypi.org/project/cleanup
[license-shield]: https://img.shields.io/github/license/faheel/cleanup.svg?style=for-the-badge
[license-link]: https://github.com/faheel/cleanup/blob/master/LICENSE
