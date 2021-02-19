# -*- coding: utf-8 -*-
import io

from setuptools import find_packages, setup
from Semi_ATE.STIL import __version__

# =============================================================================
# Use README.md for long description
# =============================================================================
with io.open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

# https://setuptools.readthedocs.io/en/latest/
# PEP-314 (Metadata for Python Software Packages) : https://www.python.org/dev/peps/pep-0314/
# https://pypi.org/classifiers/

setup(
    name="Semi-ATE-STIL",
    version=__version__,
    description="Standard Tester Interface Library [IEEE1450] with python",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Tom Hören",
    maintainer="Semi-ATE",
    maintainer_email="info@Semi-ATE.com",
    url="https://github.com/Semi-ATE/STIL",
    license="GPLv2",
    keywords="Semiconductor ATE Automatic Test Equipment STIL IEEE1450",
    platforms=["Windows", "Linux", "Mac OS-X"],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
