from nose.tools import assert_true, assert_equal, assert_almost_equal
import os
import numpy as np
import matplotlib.pyplot as plt
import thunderfish.bestwindow as bw


def test_best_window():
    # generate data:
    rate = 100000.0
    clip = 1.3
    time = np.arange(0.0, 1.0, 1.0 / rate)
    snippets = []
    f = 600.0
    amf = 20.0
    for ampl in [0.2, 0.5, 0.8]:
        for am_ampl in [0.0, 0.3, 0.9]:
            data = ampl * np.sin(2.0 * np.pi * f * time) * (1.0 + am_ampl * np.sin(2.0 * np.pi * amf * time))
            data[data > clip] = clip
            data[data < -clip] = -clip
            snippets.extend(data)
    data = np.asarray(snippets)

    # compute best window:
    print("call bestwindow() function...")
    idx0, idx1, clipped = bw.best_window_indices(data, rate, expand=False,
                                                 win_size=1.0, win_shift=0.1,
                                                 min_clip=-clip, max_clip=clip,
                                                 w_cv_ampl=10.0, tolerance=0.5)

    assert_equal(idx0, 6 * len(time), 'bestwindow() did not correctly detect start of best window')
    assert_equal(idx1, 7 * len(time), 'bestwindow() did not correctly detect end of best window')
    assert_almost_equal(clipped, 0.0, 'bestwindow() did not correctly detect clipped fraction')

    # clipping:
    clip_win_size = 0.5
    min_clip, max_clip = bw.clip_amplitudes(data, int(clip_win_size * rate),
                                            min_ampl=-1.3, max_ampl=1.3,
                                            min_fac=2.0, nbins=40)

    assert_true(min_clip <= -0.8 * clip and min_clip >= -clip,
                'clip_amplitudes() failed to detect minimum clip amplitude')
    assert_true(max_clip >= 0.8 * clip and max_clip <= clip,
                'clip_amplitudes() failed to detect maximum clip amplitude')

    # plotting 1:
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    bw.plot_data_window(ax, data, rate, 'a.u.', idx0, idx1, clipped)
    fig.savefig('bestwindow.png')
    assert_true(os.path.exists('bestwindow.png'), 'plotting failed')
    os.remove('bestwindow.png')

    # plotting 2:
    fig, ax = plt.subplots(5, sharex=True)
    bw.best_window_indices(data, rate, expand=False,
                           win_size=1.0, win_shift=0.1,
                           min_clip=-clip, max_clip=clip,
                           w_cv_ampl=10.0, tolerance=0.5,
                           plot_data_func=bw.plot_best_window, ax=ax)
    fig.savefig('bestdata.png')
    assert_true(os.path.exists('bestdata.png'), 'plotting failed')
    os.remove('bestdata.png')
    
