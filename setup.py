from setuptools import setup


setup(
    name='cleanup',
    packages=['cleanup'],
    version='1.0.0',
    description='A simple command line utility that organises files in a '
                'directory into subdirectories.',
    author='Faheel Ahmad',
    author_email='faheel@live.in',
    url='https://github.com/faheel/cleanup',
    download_url='https://github.com/faheel/cleanup/archive/v1.0.0.tar.gz',
    keywords=['cleanup', 'file-organiser', 'file-organisation',
              'file-management', 'cli', 'command-line', 'command-line-tool'],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
