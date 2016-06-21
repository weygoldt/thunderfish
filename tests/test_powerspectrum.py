from nose.tools import assert_true, assert_equal, assert_almost_equal
import numpy as np
import thunderfish.powerspectrum as ps

def test_powerspectrum():
    # generate data
    fundamental = 300.  # Hz
    samplerate = 100000
    time = np.linspace(0, 8 - 1 / samplerate, 8 * samplerate)
    data = np.sin(time * 2 * np.pi * fundamental)

    # run multi_resolution_psd with 2 fresolutions (list)
    psd_data = ps.multi_resolution_psd(data, samplerate, fresolution=[0.5, 1], verbose=1)

    # test the results
    assert_equal(round(psd_data[0][1][psd_data[0][0].argsort()[-1]]), fundamental, 'peak in PSD is not the fundamental '
                                                                                   'frequency given.')
    assert_equal(round(psd_data[1][1][psd_data[1][0].argsort()[-1]]), fundamental, 'peak in PSD is not the fundamental '
                                                                                   'frequency given.')
    # run multi_resolution_psd with 1 fresolutions (float)
    psd_data = ps.multi_resolution_psd(data, samplerate, fresolution=0.5, verbose=0)

    # test the result
    assert_equal(round(psd_data[1][psd_data[0].argsort()[-1]]), fundamental, 'peak in PSD is not the fundamental '
                                                                             'frequency given.')