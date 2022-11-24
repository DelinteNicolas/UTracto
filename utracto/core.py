def wmfod_to_angle(wmfod, max_value=15, min_value=30, wm_edge=0.1,
                   interface=0.08, interface_thickness=3, wm_deep=0.35,
                   smooth_factor=.85, float_type=False):

    params = locals()
    del params['wmfod']

    from scipy.ndimage import gaussian_filter

    angle_array = np.where(wmfod[:, :, :, 0] > wm_edge, min_value, max_value)
    mask = np.where(wmfod[:, :, :, 0] > interface, 1, 0)
    eroded_mask = erode3D(mask.copy(), interface_thickness)
    tot_mask = mask-eroded_mask
    angle_array[tot_mask == 1] = max_value
    sumfod = np.max(abs(wmfod), axis=3)
    highmask = np.where(sumfod > wm_deep, 1, 0)
    angle_array[highmask == 1] = min_value
    if float_type:
        angle_array = gaussian_filter(angle_array.astype(float), smooth_factor)
    else:
        angle_array = gaussian_filter(angle_array, smooth_factor)
    # angle_array[wmfod[:, :, :, 0] < 0.1] = None

    return angle_array, params