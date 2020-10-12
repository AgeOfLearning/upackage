# upackage

[pypi-build-status]: https://img.shields.io/pypi/v/upackage.svg
[travis-ci-status]: https://img.shields.io/travis/AgeOfLearning/upackage.svg

[![pypi][pypi-build-status]](https://pypi.python.org/pypi/upackage)
[![travis][travis-ci-status]](https://travis-ci.org/AgeOfLearning/upackage)

## About

upackage is a python module for generating *.unitypackage from source assets without unity.

## Install

```python
pip install upackage
```

## How to use
Given the following setup:
```
some/path/to/my/content/
some/path/to/my/content/code.dll
some/path/to/my/content/object.prefab
some/path/to/my/content/code.dll.mbd
```

The command will generate a package that installs the content of "some/path/to/my/content/" into "Assets/content/".
It uses the last folder name in the path as the containing folder for the assets.

```python
UPackage.preprocess_assets("some/path/to/my/content")
UPackage.generate_package("some/path/to/my/content", "output.unitypackage")
```

## Command Line Access
The tool also supports CLI access:
```bash
upackage some/path/to/my/content output.unitypackage
```


## MetaFiles
*.meta files will be generated if they do not exist for files & folders.