from setuptools import setup, find_packages
from codecs import open
from os import path

# Get the long description from README.md
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cleanup',
    version='1.0.3',
    description='A simple command line utility that organises files in a '
                'directory into subdirectories.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/faheel/cleanup',
    author='Syed Faheel Ahmad',
    author_email='faheel@live.in',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='cleanup file-organiser file-organisation file-management hue docopt',
    packages=find_packages(exclude=['test']),
    install_requires=['docopt', 'huepy'],
    extras_require={
        'dev': ['pylint'],
    },
    entry_points={
        'console_scripts': [
            'cleanup=cleanup.cleanup:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/faheel/cleanup/issues',
        'Source': 'https://github.com/faheel/cleanup',
    },
)
