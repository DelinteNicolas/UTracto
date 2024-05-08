# -*- coding: utf-8 -*-
"""

@author: DELINTE Nicolas
"""

import numpy as np
from scipy.ndimage import gaussian_filter
from binama.utils import dilation


def wmfod_to_angle(wmfod, gmfod=None, csffod=None,
                   max_angle: int = 30, min_angle: int = 15,
                   wm_edge: float = 0.1, interface: float = 0.08,
                   interface_thickness: int = 2, wm_deep=0.35,
                   smooth_factor: float = .85, float_type: bool = False,
                   only_WM: bool = False, more_wm: bool = False):
    """
    Creates an angular map based on the white matter FOD.

    Parameters
    ----------
    wmfod : 4-D array of shape (x,y,z,sh)
        Array containg the white matter FOD's spherical harmonics coefficients.
    gmfod : 4-D array of shape (x,y,z,1)
        Array containg the grey matter FOD's spherical harmonics coefficients.
    csffod : 4-D array of shape (x,y,z,1)
        Array containg the csf FOD's spherical harmonics coefficients.
    max_angle : int, optional
        Maximum value of the tractography angle. The default is 15.
    min_angle : int, optional
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
    more_wm : bool, optional
        If true, adds back areas of deep white matter.

    Returns
    -------
    angle_array : 3-D array of shape (x,y,z)
        Angular map containing the position-dependent maximum angles.
    params : dict
        Dictionnary of parameters used.

    """

    params = locals()
    del params['wmfod']
    del params['gmfod']
    del params['csffod']
    if gmfod is not None and csffod is not None:
        seg = np.argmax(np.stack([wmfod[..., 0], gmfod[..., 0], csffod[..., 0]],
                                 axis=-1), axis=-1)
    else:
        seg = np.where(wmfod[..., 0] < interface, 1, 0)
    gm_mask = np.where(seg == 1, 1, 0)
    gm_ext = dilation(gm_mask, interface_thickness)
    angle = np.where(gm_ext == 1, max_angle, min_angle)
    if more_wm:
        angle = np.where(np.max(abs(wmfod), axis=3) > wm_deep, min_angle, angle)
    if float_type:
        angle = angle.astype(float)
    amap = gaussian_filter(angle, smooth_factor).astype(float)
    if only_WM:
        amap[wmfod[..., 0] < wm_edge] = None

    return amap, params
