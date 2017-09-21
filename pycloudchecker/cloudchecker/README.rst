elb checker
-----------

Project to illustrate packaging capability for python project.

* Use -e to install the project in dev mode.

* Using __main__.py to allow:
    $ python -m elbchecker

* Using pbr that allows:
    version from git
    no need to repeat requirements.txt
    no need to repeat project description with readme.
    automatic changelog from git.
    automatic AUTHOR from git.
    automatic lookup for packages.
    etc.

* Usage of conditional dependencies with <extra> (setuptools?).
* Console script to declare cli.

Usage
-----

$ git tag -a <TAG>                            # << use this tag in finding the package version.
$ python setup.py [ sdist | bdist | ... ]     # << generate source/binary package.
