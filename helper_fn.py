import os
import sys

def dir_check(dir_path: str):
    # Check if the data directory exists
    if not os.path.exists(dir_path):
        print(f"Directory {dir_path} does not exist")
        sys.exit(1)

    # Check if the data directory is empty
    if not os.listdir(dir_path):
        print(f"Directory {dir_path} is empty")
        sys.exit(1)
        
    # Check if there are any missing files 
    file_in_dir_list = os.listdir(dir_path)

    tif_list = [f[:-4] for f in file_in_dir_list if f.endswith('.tif')]
    zip_list = [f[:-4] for f in file_in_dir_list if f.endswith('.zip')]

    # Check if there are any missing tif files
    missing_tif_files = [file for file in zip_list if file not in tif_list]
    missing_zip_files = [file for file in tif_list if file not in zip_list]

    # Add corresponding extensions to the missing files
    missing_tif_files = [file + '.tif' for file in missing_tif_files]
    missing_zip_files = [file + '.zip' for file in missing_zip_files]

    missing_files_list = missing_tif_files + missing_zip_files
    
    if missing_files_list:
        print(f"Missing files: {missing_files_list}")
        sys.exit(1)
    else:
        print("All files are present")
        
def create_dict(dir_path:str) -> dict:
    """
    Generate a dictionary key = dish_i, value = (tiff_path, roi_path)"""
    
    file_in_dir_list = os.listdir(dir_path)
    
    abs_dir_path = abs_dir_path = os.path.abspath(dir_path)
    
    file_in_dir_list = [f"{abs_dir_path}/{file}"for file in file_in_dir_list]
    
    file_list = [f[:-4] for f in file_in_dir_list if f.endswith('.tif')]

    plot_dic = {}

    for file in file_list:
        name = file.split('.')[0]
        dish_name = name.split('_')

        for word in dish_name:
            if "dish" in word.lower():
                dish_i = word
                plot_dic[dish_i] = (f"{file}.tif", f"{file}.zip")
            else:
                continue

    return plot_dic