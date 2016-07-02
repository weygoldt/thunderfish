import numpy as np
import argparse
import config_tools as ct
import dataloader as dl
import bestwindow as bw
import checkpulse as chp
import powerspectrum as ps
import harmonicgroups as hg
import consistentfishes as cf
import eodanalysis as ea
import matplotlib.pyplot as plt


def main(audio_file, channel=0, output_folder='', beat_plot=False, verbose=0):
    # create figure and axis for the outputplot
    fig = plt.figure(facecolor='white', figsize=(12., 8.))
    ax1 = fig.add_subplot(2, 2, (3, 4))  # axis for the psd
    ax2 = fig.add_subplot(2, 2, 2)  # axis for the mean eod

    # get config dictionary
    cfg = ct.get_config_dict()

    if verbose is not None:  # ToDo: Need to document the whole cfg-dict thing.
        cfg['verboseLevel'][0] = verbose
    channel = channel

    # load data using dataloader module
    raw_data, samplerate, unit = dl.load_data(audio_file)

    # calculate best_window
    data, clip = bw.best_window(raw_data, samplerate)

    # sort fish-type
    sugg_type, pta_value = chp.check_pulse_width(data, samplerate)  # pta = peak-trough-analysis

    # calculate powerspectrums with different frequency resolutions
    psd_data = ps.multi_resolution_psd(data, samplerate, fresolution=[0.5, 2 * 0.5, 4 * 0.5])
    ps.plot_decibel_psd(psd_data[0][0], psd_data[0][1], ax1, fs=12)

    # find the fishes in the different powerspectrums
    fishlists = []
    for i in range(len(psd_data)):
        fishlist = hg.harmonic_groups(psd_data[i][1], psd_data[i][0], cfg)[0]
        fishlists.append(fishlist)

    # find the psd_type
    pulse_psd, proportion = chp.check_pulse_psd(psd_data[0][0], psd_data[0][1])

    # filter the different fishlists to get a fishlist with consistent fishes
    if sugg_type is 'wave' and not pulse_psd:
        filtered_fishlist = cf.consistent_fishes(fishlists)
        cf.consistent_fishes_psd_plot(filtered_fishlist, ax=ax1)

    # analyse the eod
    eod_idx_diff = ea.eod_analysis(data, samplerate, plot_data_func=ea.eod_analysis_plot, ax=ax2)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # command line arguments:
    parser = argparse.ArgumentParser(
        description='Analyse short EOD recordings of weakly electric fish.',
        epilog='by bendalab (2015-2016)')
    parser.add_argument('--version', action='version', version='1.0')
    parser.add_argument('-v', action='count', dest='verbose')
    parser.add_argument('file', nargs='?', default='', type=str, help='name of the file wih the time series data')
    parser.add_argument('channel', nargs='?', default=0, type=int, help='channel to be displayed')
    parser.add_argument('output_folder', nargs='?', default=".", type=str, help="location to store results, figures")
    args = parser.parse_args()

    main(args.file, args.channel, args.output_folder, verbose=args.verbose)
