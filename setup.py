from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-see-profile',
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='1.1',
    description='Django middleware for logging profiling data',
    long_description=long_description,
    # The project's main homepage.
    url='https://github.com/sdelements/django-see-profile',
    # Author details
    author='Security Compass',
    author_email='jeff@securitycompass.com',
    # Choose your license
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    # What does your project relate to?
    keywords='django middleware profiling',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['see_profile'],
    install_requires=[
        "django>=1.10",
        "django-security>=0.9.0"
    ],
)
