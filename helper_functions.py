import os
import sys

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
    pass

if __name__ == '__main__':
    main(sys.argv[1:])