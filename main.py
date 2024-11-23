import sys
import os

from plots import Plotter
from argument_parser import parse_args
from helper_functions import missing_files

# from display_tif import the gif function



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
        
    # Get full path of the directory
    abs_dir_path = os.path.abspath(args.data)
    
    ################### Check if there are any missing files ###################
    missing_files_list = missing_files(args.data, args)

    if missing_files_list:
        print(f"Missing files: {missing_files_list}")
        sys.exit(1)
    else:
        print("All files are present")


    # Generate a dictionary key = plot/gif_number, value = (tiff_path, roi_path)
    file_in_dir_list = os.listdir(args.data)
    file_in_dir_list = [f"{abs_dir_path}/{file}"for file in file_in_dir_list]
    
    file_list = [f[:-4] for f in file_in_dir_list if f.endswith('.tif')]

    plot_dic = {f"plot_{i}":(f"{file}.tif", f"{file}.zip") for (i, file) in enumerate(file_list)}

    ################### GIF ###################
    if args.gif:
        for plot_i in plot_dic:
            plotter = Plotter(plot_dic[plot_i][0], plot_dic[plot_i][1], 'katielane', desired_contrast=5.0)
            print("Creating GIF")
            plotter.display_gif()
            

    ################### Plots ###################
    
    if args.plot_type is not None:
        if 'single' in args.plot_type:
            for plot_i in plot_dic:
                plotter = Plotter(plot_dic[plot_i][0], plot_dic[plot_i][1], 'katielane', desired_contrast=5.0)
                
                if args.plot_type == 'single_fluor':
                    print("Creating Single Fluoresence Over Time Plot")
                    plotter.plot_fluor_over_time()
                elif args.plot_type == 'single_decay':
                    print("Creating Single Decay Over Time Plot")
                    plotter.plot_decay_over_time()
                elif args.gif:
                    print("Creating GIF")
                    plotter.display_gif
                
            
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