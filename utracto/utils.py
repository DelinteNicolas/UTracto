def mrtrix_fod_to_dipy(sh):
    '''
    Does not work with full basis, only symmetrical SH

    Parameters
    ----------
    sh : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''

    sh_order = (np.sqrt(sh.shape[3]*8+1)-3)/2

    default_sphere = get_sphere('repulsion724')

    temp = sh_to_sf(sh, sphere=default_sphere, sh_order=sh_order,
                    basis_type='tournier07', legacy=False)
    sh = sf_to_sh(temp, sphere=default_sphere, sh_order=sh_order,
                  basis_type='descoteaux07', legacy=False)

    counter = 0
    for l in range(sh_order.astype(int)):
        n = 1+2*l
        m_list = np.linspace((n-1)/2, -(n-1)/2, n)
        for m in m_list:
            if l % 2 == 0 and m % 2 == 0 and m < 0:
                sh[:, :, :, counter] *= -1
            if l % 2 == 0:
                counter += 1

    return sh

def angle_difference(v1, v2) -> float:
    '''
    Computes the angle difference between two vectors.
    Parameters
    ----------
    v1 : 1-D array
        Vector. Ex: [1,1,1]
    v2 : 1-D array
        Vector. Ex: [1,1,1]
    Returns
    -------
    ang : float
        Angle difference (in degrees).
    '''

    v1n = v1/np.linalg.norm(v1)
    v2n = v2/np.linalg.norm(v2)

    if (v1n == v2n).all():
        return 0

    if sum(v1n*v2n) > 1:
        return 0

    if sum(v1n*v2n) < -1:
        return 180

    ang = np.arccos(sum(v1n*v2n))*180/np.pi

    return ang


def find_low_nearest(array, value):
    vals = array-value
    vals[vals > 0] = np.min(vals)
    idx = vals.argmax()
    return idx


if __name__ == '__main__':

    trk_file = "C:/Users/nicol/Documents/Doctorat/Data/disco_phantom/DiSCo1/low_resolution_20x20x20/output/lowRes_DiSCo1_DWI_tract_mrtrix_30.trk"

    trk = load_tractogram(trk_file, 'same')
    trk.to_vox()
    trk.to_corner()

    # -------------------------------------------------

    streams = trk.streamlines
    streams_data = trk.streamlines.get_data()

    for p in tqdm(range(1, streams_data.shape[0]-1)):
        # for p in tqdm(range(1, 1000)):

        if p in streams._offsets or p+1 in streams._offsets:
            continue

        point = streams_data[p]
        previous_point = streams_data[p-1]
        next_point = streams_data[p+1]

        v1 = (point-previous_point)
        v2 = (next_point-point)

        ang = angle_difference(v1, v2)

        if ang > 30:

            stream_num = find_low_nearest(streams._offsets, p+1)

            streams._offsets = np.insert(streams._offsets, stream_num+1, p+1)

            old_value = streams._lengths[stream_num]
            new_value = p+1-streams._offsets[stream_num]
            streams._lengths[stream_num] = new_value

            streams._lengths = np.insert(streams._lengths, stream_num+1,
                                         old_value-new_value)

    save_tractogram(
        trk, "C:/Users/nicol/Documents/Doctorat/Data/disco_phantom/DiSCo1/low_resolution_20x20x20/output/lowRes_DiSCo1_DWI_tract_mrtrix_30.trk")
