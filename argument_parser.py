import argparse
import sys

'''
Flags:
    - gif generation 
    - multiple plots vs singular plots (w/ legend)
    - path to data directory 

    Recondsider based on Galati's need: 

    - normalization?
    - contrast?
    - downscaling?
    - cell detection?
'''


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Calcium Diffusion Fluorescence Video Analysis")

    # Path to the directory containing the video files
    parser.add_argument('-d', '--data', type=str, help='Absolute path to the directory containing the video files', required=True)

    # Gif of the video will be generated and saved with the same name as the video with the extension .gif
    parser.add_argument('-gif', '--gif', action='store_true', help='Generate and save gif of video')

    # Single dish vs multiple dish per plot
    parser.add_argument('-plot', '--plot_type', type=str, choices=['single', 'multiple'], help='Plot single/multiple dishes on the same plot')

    # Include line of best fit
    parser.add_argument('-line', '--line_of_best_fit', action='store_true', help='Include line of best fit')

    # Return data for each dish as csv
    parser.add_argument('-csv', '--csv', action='store_true', help='Return data for each dish as csv')

    return parser.parse_args(argv)


def main(argv):
    print(f"arguments passed: {argv}")
    args = parse_args(argv)
    print(args)

if __name__ == '__main__':
    main(sys.argv[1:])