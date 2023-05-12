# -*- coding: utf-8 -*-
"""

@author: DELINTE Nicolas
"""

from setuptools import setup

import utracto

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='utracto',
    version=utracto.__version__,
    description='Implementation of UTracto',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DelinteNicolas/UTracto',
    author='Nicolas Delinte',
    author_email='nicolas.delinte@uclouvain.be',
    license='GNU General Public License v3.0',
    packages=['utracto'],
    install_requires=['dipy',
                      'nibabel',
                      'numpy',
                      'tqdm',
			    'pilab-binama',
			    'unravel-python',
                      ],

    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Science/Research',
                 'Natural Language :: English',
                 'Programming Language :: Python'],
)
