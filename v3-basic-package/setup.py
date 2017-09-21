from distutils.core import setup

# -- minimal packaging --
# Check metadata are correct.
# $ python setup.py check

# Generate source distribution, contains python source.
# should be enough if no binary module are needed.
# $ python setup.py sdist
# $ tar -tzvf dist/elbchecker-0.0.1.tar.gz              # << list source package content.

# To install
# $ pip install dist/elbchecker-0.0.1.tar.gz

# To Run
# $ python -m elbchecker --help                         # << no console script yet.
# --

setup(name='elbchecker', version='0.0.1',
      packages=['elbchecker'],
      url='https://www.cloudreach.com',
      author='nacim',
      author_email='nassim.babaci@cloudreach.com',     # << detected by setup.py check command.
      description='Smoke tests for aws elb')
