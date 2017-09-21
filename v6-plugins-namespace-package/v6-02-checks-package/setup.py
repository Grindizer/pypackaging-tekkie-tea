from setuptools import setup

# -- minimal packaging --
# Check metadata are correct.
# $ python setup.py check

# Generate source distribution, contains python source.
# should be enough if no binary module are needed.
# $ python setup.py sdist
# $ tar -tzvf dist/elbchecks-0.0.1.tar.gz              # << list source package content.

# To install
# $ pip install dist/elbchecks-0.0.1.tar.gz

setup(name='ec2checks', version='0.0.1',
      packages=['elbchecker.checks'],
      url='https://www.cloudreach.com',
      author='nacim',
      author_email='nassim.babaci@cloudreach.com',          # << detected by setup.py check command.
      description='ec2 checks function for aws elbchecker',
      install_requries=['botocore'],
      entry_points={'elbchecker.checks': ['subnets = ec2checks.lib:check_subnets',
                                          'instances = ec2checks.lib:check_instances']})

