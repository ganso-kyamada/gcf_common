import setuptools
import os

def load_requires_from_file(fname):
    if not os.path.exists(fname):
        raise IOError(fname)
    return [pkg.strip() for pkg in open(fname, 'r')]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup()
