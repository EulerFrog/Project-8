from argument_parser import parse_args
from helper_functions import missing_files
# from display_tif import the gif function

import sys
import os


def main(argv):
    '''
    1. Call argparse
    2. Call selected functions


    - gif generation 
    - multiple plots vs singular plots (w/ legend)
    - path to data directory 
    - line of best fit
    - return data for each dish as csv

    '''

    # Parse the arguments
    args = parse_args(argv)

    ################### Check if the data directory exists (do we want this as a helper function?) ###################
    if not os.path.exists(args.data):
        print(f"Directory {args.data} does not exist")
        sys.exit(1)

    # Check if the data directory is empty
    if not os.listdir(args.data):
        print(f"Directory {args.data} is empty")
        sys.exit(1)
    
    
    ################### Check if there are any missing files ###################
    missing_files_list = missing_files(args.data, args)

    if missing_files_list:
        print(f"Missing files: {missing_files_list}")
        sys.exit(1)
    else:
        print("All files are present")


    ################### Gif ###################
    if args.gif:
        print("Generating gif")
        # the gif function

    ################### Plots ###################
    if args.plot_type == 'single':
        print(f"Plot type: {args.plot_type}")
        # the single plot function
    elif args.plot_type == 'multiple':
        print(f"Plot type: {args.plot_type}")
        # the multiple plot function

    ################### Line of best fit ###################
    if args.plot_type == None:
        print("Please specify plot type")
        sys.exit(1)
    elif args.line_of_best_fit:
        print("Including line of best fit")
        # the line of best fit function

    ################### Return data for each dish as csv ###################
    if args.csv:
        print("Returning data for each dish as csv")
        # the csv function
    

    

        


   
if __name__ == '__main__':
    main(sys.argv[1:])