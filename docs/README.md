# U-fiber tractography

Welcome to the UTracto's Github repository! 

## Description

This repository contains a package facilitating the tracking of sub-cortical U-Fibers. The main function of this package is the creation of angular maps, enabling a tractography with a position-dependent maximum angle between tractography steps. The function creating these angular maps is `wmfod_to_angle` in the `core.py` file.

<p align="center">
  <img src="https://user-images.githubusercontent.com/70629561/207111838-6ec3ba60-fd52-47ad-a469-17a29df74513.png" width="600" />
</p>

This angular map is to be used with a forked version of [DIPY](https://github.com/DelinteNicolas/dipy).

## Installing & importing

### Local install

If you want to download the latest version directly from GitHub, you can clone this repository
```
git clone https://github.com/DelinteNicolas/UTracto.git
```

## Example data and code

An example use of the main methods and outputs of UTracto is written in the `example.py` file. 
