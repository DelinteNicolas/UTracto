# U-fiber tractography

Welcome to the UTracto's Github repository!

[![PyPI](https://img.shields.io/pypi/v/utracto?label=pypi%20package)](https://pypi.org/project/utracto/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/utracto)](https://pypi.org/project/utracto/)
![GitHub repo size](https://img.shields.io/github/repo-size/DelinteNicolas/UTracto)

## Description

This repository contains a package facilitating the tracking of sub-cortical U-Fibers. The main function of this package is the creation of angular maps, enabling a tractography with a position-dependent maximum angle between tractography steps. The function creating these angular maps is `wmfod_to_angle` in the [`core.py`](https://github.com/DelinteNicolas/UTracto/blob/main/utracto/core.py) file.

<p align="center">
  <img src="https://user-images.githubusercontent.com/70629561/207111838-6ec3ba60-fd52-47ad-a469-17a29df74513.png" width="600" />
</p>

This angular map is to be used with a forked version of [DIPY](https://github.com/DelinteNicolas/dipy).

## Installing & importing

### Online install

The UNRAVEL package is available through ```pip install``` under the name ```utracto```. Note that the online version might not always be up to date with the latest changes.

```
pip install utracto
```
To upgrade the current version : ```pip install utracto --upgrade```.

To install a specific version of the package use
```
pip install utracto==0.0.8
```
All available versions are listed in [PyPI](https://pypi.org/project/utracto/). The package names follow the rules of [semantic versioning](https://semver.org/).

### Local install

If you want to download the latest version directly from GitHub, you can clone this repository
```
git clone https://github.com/DelinteNicolas/UTracto.git
```
For a more frequent use of the library, you may wish to permanently add the package to your current Python environment. Navigate to the folder where this repository was cloned or downloaded (the folder containing the ```setup.py``` file) and install the package as follows
```
cd UTracto
pip install .
```

If you have an existing install, and want to ensure package and dependencies are updated use --upgrade
```
pip install --upgrade .
```
### Importing
At the top of your Python scripts, import the library as
```
import utracto
```

### Checking current version installed

The version of the UNRAVEL package installed can be displayed by typing the following command in your python environment
```
utracto.__version__
``` 

### Uninstalling
```
pip uninstall utracto
```

## Example data and code

An example use of the main methods and outputs of UTracto is written in the `example.py` file. 
