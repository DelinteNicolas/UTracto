# -*- coding: utf-8 -*-
"""

@author: DELINTE Nicolas
"""

import numpy as np
from scipy.ndimage import gaussian_filter
from binama.utils import erosion


def wmfod_to_angle(wmfod, max_value: int = 30, min_value: int = 15,
                   wm_edge: float = 0.1, interface: float = 0.08,
                   interface_thickness: int = 3, wm_deep=0.35,
                   smooth_factor: float = .85, float_type: bool = False,
                   only_WM: bool = False):
    """
    Creates an angular map based on the white matter FOD.

    Parameters
    ----------
    wmfod : 4-D array of shape (x,y,z,sh)
        Array containg the white matter FOD's spherical harmonics coefficients.
    max_value : int, optional
        Maximum value of the tractography angle. The default is 15.
    min_value : int, optional
        Minimum value of the tractography angle. The default is 30.
    wm_edge : float, optional
        Minimum value of wmfod[:,:,:,0] to be considered as white mater.
        The default is 0.1.
    interface : float, optional
        Value of wmfod[:,:,:,0] to be considered at the interface between grey
        and white mater. The default is 0.08.
    interface_thickness : int, optional
        Thickness of the grey/white matter interface. The default is 3.
    wm_deep : float, optional
        Value above which we are in deep white matter. The default is 0.35.
    smooth_factor : float, optional
        Gaussian filter factor. The default is .85.
    float_type : bool, optional
        If True then output is in float. The default is False.
    only_WM : bool, optional
        If True, the angular map is only in areas of white matter.
        The default is False.

    Returns
    -------
    angle_array : 3-D array of shape (x,y,z)
        Angular map containing the position-dependent maximum angles.
    params : dict
        Dictionnary of parameters used.

    """

    params = locals()
    del params['wmfod']
    angle_array = np.where(wmfod[:, :, :, 0] > wm_edge, min_value, max_value)
    mask = np.where(wmfod[:, :, :, 0] > interface, 1, 0)
    eroded_mask = erosion(mask.copy(), interface_thickness)
    tot_mask = mask-eroded_mask
    angle_array[tot_mask == 1] = max_value
    sumfod = np.max(abs(wmfod), axis=3)
    highmask = np.where(sumfod > wm_deep, 1, 0)
    angle_array[highmask == 1] = min_value
    if float_type:
        angle_array = gaussian_filter(angle_array.astype(float), smooth_factor)
    else:
        angle_array = gaussian_filter(angle_array, smooth_factor)
    if only_WM:
        angle_array[wmfod[:, :, :, 0] < wm_edge] = None

    return angle_array, params
