# -*- coding: utf-8 -*-
"""
Created on Wed May 10 14:46:56 2023

@author: DELINTE Nicolas
"""

import numpy as np
from dipy.segment.mask import median_otsu
from dipy.tracking.stopping_criterion import ThresholdStoppingCriterion
from dipy.tracking.streamline import Streamlines
from dipy.tracking.utils import target
from dipy.tracking.local_tracking import LocalTracking
from dipy.tracking import utils
from dipy.core.gradients import gradient_table
from dipy.io import read_bvals_bvecs
from dipy.io.image import load_nifti, load_nifti_data
from dipy.data import get_sphere
from dipy.reconst.csdeconv import (ConstrainedSphericalDeconvModel,
                                   auto_response_ssst)
from binama.utils import dilation
from utracto.utils import mrtrix_fod_to_dipy


def brainTracking(Patient_files, params, seed_files=None, target_files=None,
                  all_seed=False, dilate=[0, 0], in_fod=None,
                  in_fod_from_mrtrix=False, angle_var=None,
                  wmfod=None, ptt: bool = False):
    '''


    Parameters
    ----------
    Patient_files : path to diffusion files + filename (without extension)
    params : parameters dictionary (ex: {'fa_thr':.6,'gfa_thresh':.35,
                                         'max_angle':15,'step_size':1,'density':2})
    seed_file : path to seed mask
    target_files : path to target (logical AND) ROI
    all_seed: bool
        forces all pixels to be seed candidates

    Returns
    -------
    tract : whole brain tractogram

    '''

    data, affine, img = load_nifti(Patient_files+'.nii.gz', return_img=True)
    bvals, bvecs = read_bvals_bvecs(
        Patient_files+'.bval', Patient_files+'.bvec')
    gtab = gradient_table(bvals, bvecs, atol=1)

    if all_seed:
        seed_mask = np.ones(data.shape[:-1])
        white_matter = seed_mask.copy()

    else:

        mask_data, white_matter = median_otsu(data, vol_idx=[0, 1], median_radius=4, numpass=2,
                                              autocrop=False, dilate=1)
        # white_matter=load_nifti_data(root+Patient+mas_dir+Patient+'_wm_mask'+'.nii.gz')

        seed_mask = white_matter

    if seed_files != None:
        if type(seed_files[0]) == str:
            seed_mask = load_nifti_data(seed_files[0]+'.nii.gz')
            for i in range(1, len(seed_files)):
                seed_mask += load_nifti_data(seed_files[i]+'.nii.gz')
                seed_mask[seed_mask > 1] = 1
        else:
            seed_mask = seed_files[0]
        seed_mask = dilation(seed_mask, dilate[0])

    seeds = utils.seeds_from_mask(seed_mask, affine, density=params['density'])

    if in_fod is None:
        response, ratio = auto_response_ssst(
            gtab, data, roi_radii=10, fa_thr=params['fa_thr'])
        csd_model = ConstrainedSphericalDeconvModel(gtab, response, sh_order=8)
        csd_fit = csd_model.fit(data, mask=white_matter)
        fod = csd_fit.shm_coeff

        # # Temp
        # out = nib.Nifti1Image(csd_fit.shm_coeff, img.affine, img.header)
        # out.to_filename('C:/users/nicol/Desktop/disco_dipy_fod.nii.gz')

    else:
        fod = in_fod

    if wmfod is None:

        from dipy.reconst.shm import CsaOdfModel

        csa_model = CsaOdfModel(gtab, sh_order=6)
        gfa = csa_model.fit(data, mask=white_matter).gfa
        stopping_criterion = ThresholdStoppingCriterion(
            gfa, params['gfa_thresh'])

    else:

        stopping_criterion = ThresholdStoppingCriterion(wmfod,
                                                        params['wmfod_thresh'])

    from dipy.direction import ProbabilisticDirectionGetter, PTTDirectionGetter
    from dipy.io.stateful_tractogram import Space, StatefulTractogram

    # SH
    default_sphere = get_sphere('repulsion724')

    if in_fod_from_mrtrix:
        print('Tournier convention used for SH')

        # # Temp
        # out = nib.Nifti1Image(fod, img.affine, img.header)
        # out.to_filename('C:/users/nicol/Desktop/disco_mrtrix_dipy_fod.nii.gz')

        fod = mrtrix_fod_to_dipy(fod)

    if ptt:

        fod = csd_fit.odf(default_sphere)
        pmf = fod.clip(min=0)
        prob_dg = PTTDirectionGetter.from_pmf(pmf, max_angle=params['max_angle'],
                                              probe_length=0.5,
                                              sphere=default_sphere)

    elif angle_var is None:
        prob_dg = ProbabilisticDirectionGetter.from_shcoeff(fod,
                                                            max_angle=params['max_angle'],
                                                            sphere=default_sphere)

    else:

        # Modified dipy
        prob_dg = ProbabilisticDirectionGetter.from_shcoeff(fod,
                                                            max_angle=params['max_angle'],
                                                            sphere=default_sphere,
                                                            angle_var=angle_var,
                                                            )
        print('launching with modified DIPY')

    streamline_generator = LocalTracking(prob_dg, stopping_criterion, seeds,
                                         affine, step_size=params['step_size'])
    streamlines = Streamlines(streamline_generator)

    if target_files != None:
        for i, target_file in enumerate(target_files):
            if len(dilate[1]) > 1:
                dilat = dilate[1][i]
            else:
                dilat = dilate[1][0]
            target_roi = load_nifti_data(target_file+'.nii.gz')
            target_roi = dilation(target_roi, dilat)
            streamlines = target(streamlines, affine, target_roi, include=True)

    tract = StatefulTractogram(streamlines, img, Space.RASMM)

    return tract
