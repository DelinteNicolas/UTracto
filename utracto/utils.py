# -*- coding: utf-8 -*-
"""

@author: DELINTE Nicolas
"""

import numpy as np
from tqdm import tqdm
from dipy.data import get_sphere
from dipy.reconst.shm import sh_to_sf, sf_to_sh
from dipy.io.streamline import load_tractogram, save_tractogram
from TIME.core import angle_difference


def _flip_m_neg(sh, sh_order: int, full_basis: bool = False):
    '''


    Parameters
    ----------
    sh : 4-D array
        Spherical harmonics coefficient array of shape (x,y,z,coeff).
    sh_order : int
        Order of the spherical harmonics.
    full_basis : bool, optional
        If True, takes a full basis as input. The default is False.

    Returns
    -------
    sh : 4-D array
        Spherical harmonics coefficient array of shape (x,y,z,coeff).

    '''

    counter = 0
    for l in range(sh_order.astype(int)):
        n = 1+2*l
        m_list = np.linspace((n-1)/2, -(n-1)/2, n)
        for m in m_list:
            if full_basis:
                if m % 2 == 0 and m < 0:
                    sh[:, :, :, counter] *= -1
                counter += 1
            else:
                if l % 2 == 0:
                    if m % 2 == 0 and m < 0:
                        sh[:, :, :, counter] *= -1
                    counter += 1

    return sh


def dipy_fod_to_mrtrix(sh):
    '''
    Converts spherical harmonics (sh) file from dipy format to mrtrix format.
    Does not work with full basis, only symmetrical SH.

    Parameters
    ----------
    sh : 4-D array
        Spherical harmonics coefficient array of shape (x,y,z,coeff).

    Returns
    -------
    sh : 4-D array
        Spherical harmonics coefficient array of shape (x,y,z,coeff).

    '''

    sh_order = (np.sqrt(sh.shape[3]*8+1)-3)/2

    sh = _flip_m_neg(sh, sh_order)

    default_sphere = get_sphere('repulsion724')

    temp = sh_to_sf(sh, sphere=default_sphere, sh_order=sh_order,
                    basis_type='descoteaux07', legacy=False)
    sh = sf_to_sh(temp, sphere=default_sphere, sh_order=sh_order,
                  basis_type='tournier07', legacy=False)

    return sh


def mrtrix_fod_to_dipy(sh):
    '''
    Converts spherical harmonics (sh) file from mrtrix format to dipy format.
    Does not work with full basis, only symmetrical SH.

    Parameters
    ----------
    sh : 4-D array
        Spherical harmonics coefficient array of shape (x,y,z,coeff).

    Returns
    -------
    sh : 4-D array
        Spherical harmonics coefficient array of shape (x,y,z,coeff).

    '''

    sh_order = (np.sqrt(sh.shape[3]*8+1)-3)/2

    default_sphere = get_sphere('repulsion724')

    temp = sh_to_sf(sh, sphere=default_sphere, sh_order=sh_order,
                    basis_type='tournier07', legacy=False)
    sh = sf_to_sh(temp, sphere=default_sphere, sh_order=sh_order,
                  basis_type='descoteaux07', legacy=False)

    sh = _flip_m_neg(sh, sh_order)

    return sh


def _find_low_nearest(array, value: int) -> int:
    '''
    Finds the index of the array element closest to value but not above value.

    Parameters
    ----------
    array : 1-D array
        1-D array
    value : int
        Value

    Returns
    -------
    idx : int
        Index

    '''
    vals = array-value
    vals[vals > 0] = np.min(vals)
    idx = vals.argmax()
    return idx


def fix_angle(trk_file: str, out_file: str = None, max_angle: int = 30):
    """
    Maxes sure no angle between two tractography steps are higher than
    max_angle. Angles greater than the specified value are cut into two
    separate streamlines.

    Parameters
    ----------
    trk_file : str
        File path to .trk file.
    out_file : str, optional
        If specified, output path. If not specified, overwrites input file.
        The default is None.
    max_angle : int, optional
        Maximum angle between two tractography steps. The default is 30.

    Returns
    -------
    None.

    """

    trk = load_tractogram(trk_file, 'same')
    trk.to_vox()
    trk.to_corner()

    streams = trk.streamlines
    streams_data = trk.streamlines.get_data()

    for p in tqdm(range(1, streams_data.shape[0]-1)):

        if p in streams._offsets or p+1 in streams._offsets:
            continue

        point = streams_data[p]
        previous_point = streams_data[p-1]
        next_point = streams_data[p+1]

        v1 = (point-previous_point)
        v2 = (next_point-point)

        ang = angle_difference(v1, v2)

        if ang > max_angle:

            stream_num = _find_low_nearest(streams._offsets, p+1)

            streams._offsets = np.insert(streams._offsets, stream_num+1, p+1)

            old_value = streams._lengths[stream_num]
            new_value = p+1-streams._offsets[stream_num]
            streams._lengths[stream_num] = new_value

            streams._lengths = np.insert(streams._lengths, stream_num+1,
                                         old_value-new_value)

    if out_file is None:
        out_file = trk_file

    save_tractogram(trk, out_file)
