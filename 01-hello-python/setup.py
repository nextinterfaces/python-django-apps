import sys
from setuptools import setup

setup(
    name = "nextinterfaces",        # what you want to call the archive/egg
    version = "0.1",
    packages=["nextinterfaces"],    # top-level python modules you can import like
                                #   'import foo'
    dependency_links = [],      # custom links to a specific project
    install_requires=[],
    extras_require={},      # optional features that other packages can require
                            #   like 'nextinterfaces[foo]'
    package_data = {},
    author="Atanas Roussev",
    author_email = "someone@nextinterfaces.com",
    description = "The familiar example program in Python",
    license = "BSD",
    keywords= "example documentation tutorial",
    url = "git@github.com:nextinterfaces/python-sample-project.git",
    entry_points = {
        "console_scripts": [        # command-line executables to expose
            "nextinterfaces_in_python = nextinterfaces.main:main",
        ],
        "gui_scripts": []       # GUI executables (creates pyw on Windows)
    }
)
