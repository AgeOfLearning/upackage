#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup_requirements = ["pytest-runner"]
test_requirements = ["pytest"]

setup(
    author="Age of Learning",
    author_email='leonid.umanskiy@aofl.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'upackage=upackage.__main__:main',
        ],
    },
    description="Generate .unitypackage without Unity.",
    install_requires=required,
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={'upackage': ['metafile_template.yaml']},
    keywords='upackage',
    name='upackage',
    packages=['upackage'],
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    url='https://github.com/AgeOfLearning/upackage',
    version='0.2.5',
    zip_safe=False,
)