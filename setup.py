# -*- coding: utf-8 -*-

import os, re
from setuptools import setup

readme = open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r').read()

module_file = open(os.path.join(os.path.dirname(__file__), 'plans',
                                '__init__.py'), 'r').read()
version_match = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", module_file,
                          re.M)
if not version_match:
    raise Exception("couldn't find version number")
version = version_match.group(1)

setup(
    name='plan',
    author='Wael BEN ZID ELGUEBSI',
    author_email='benzid.wael@hotmail.fr',
    version=version,
    url='https://github.com/benzid_wael/django-plans',
    packages=['plans'],
    description='Dajngo application to manage plans and features',
    long_description=readme,
    install_requires=[
        "six>=1.7.3",
    ],
    zip_safe=False,
    tests_require='nose',
    test_suite='nose.collector',
    classifiers=[
        'License :: OSI Approved :: GPL-V3 License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3',
    ]
)
