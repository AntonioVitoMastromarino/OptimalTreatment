#
# setuptools script
#
from setuptools import setup, find_packages


def get_version():
    """
    Get version number from the OptimalTreatment module.

    The easiest way would be to just ``import OptimalTreatment``, but note that this may
    fail if the dependencies have not been installed yet. Instead, we've put
    the version number in a simple version_info module, that we'll import here
    by temporarily adding the oxrse directory to the pythonpath using sys.path.
    """
    import os
    import sys

    sys.path.append(os.path.abspath('OptimalTreatment'))
    from version_info import VERSION as version
    sys.path.pop()

    return version


def get_readme():
    """
    Load README.md text for use as description.
    """
    with open('README.md') as f:
        return f.read()


# Go!
setup(
    # Module name (lowercase)
    name='OptimalTreatment',

    # Version
    version=get_version(),

    description='Optimal control on a system of two ODEs describing Cancer therapies',

    long_description=get_readme(),

    # Packages to include
    packages=find_packages(include=('OptimalTreatment', 'OptimalTreatment.*')),

    # List of dependencies
    install_requires=[
        # Dependencies go here!
        'numpy',
        'matplotlib',
    	'pandas',
        'scipy',
        'control',
    ],
)
