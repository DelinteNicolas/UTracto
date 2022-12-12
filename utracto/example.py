# -*- coding: utf-8 -*-
"""

@author: DELINTE Nicolas
"""

import os
import nibabel as nib
from core import *


if __name__ == '__main__':

    os.chdir('..')

    wmfod_file = 'data/sampleSubject_wmfod.nii.gz'

    img = nib.load(wmfod_file)
    wmfod = img.get_fdata()

    angle_array, params = wmfod_to_angle(wmfod, float_type=True, only_WM=True)

    out = nib.Nifti1Image(angle_array, img.affine)
    out.to_filename(wmfod_file[:-7]+'_angle.nii.gz')
