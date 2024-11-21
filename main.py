from argument_parser import parse_args
# from display_tif import the gif function

import sys
import os

# Helper functions for the main function
def missing_files(path: str, args):
    # Get the list of files in the data directory
    file_in_dir_list = os.listdir(args.data)

    tif_list = [f[:-4] for f in file_in_dir_list if f.endswith('.tif')]
    zip_list = [f[:-4] for f in file_in_dir_list if f.endswith('.zip')]

    # Check if there are any missing tif files
    missing_tif_files = [file for file in zip_list if file not in tif_list]
    missing_zip_files = [file for file in tif_list if file not in zip_list]

    # Add corresponding extensions to the missing files
    missing_tif_files = [file + '.tif' for file in missing_tif_files]
    missing_zip_files = [file + '.zip' for file in missing_zip_files]

    missing_files = missing_tif_files + missing_zip_files

    return missing_files

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

    # Check if the data directory exists
    if not os.path.exists(args.data):
        print(f"Directory {args.data} does not exist")
        sys.exit(1)

    # Check if the data directory is empty
    if not os.listdir(args.data):
        print(f"Directory {args.data} is empty")
        sys.exit(1)
    
    
    # Check if there are any missing files
    missing_files_list = missing_files(args.data, args)

    if missing_files_list:
        print(f"Missing files: {missing_files_list}")
        sys.exit(1)
    else:
        print("All files are present")

    

   
if __name__ == '__main__':
    main(sys.argv[1:])