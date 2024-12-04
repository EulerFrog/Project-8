import os
import sys
import click

from plots import Plotter
from helper_fn import dir_check, create_dict
from compute_regions import compute_regions, save_csv

# notes:
# save functionality for gif, nor for fluo or decay plots working.
# can we make sure they are named the same with exception of the extension and also just go back into the
# path they pass.
# make sure that line of best fit default is the same whether we want to do color by cell or not.

@click.group()
def cli():
    """
    This program will assist you with generating visuals from tif files with their corresponding roi (zip) files.
    Please make sure that the directory (folder path) passed contain tif files with roi files with the same name, except for the extension.
    For example test1.tiff, test1.zip would be a pair of matching files
    Please ensure that in the .zip files, the last roi is the background.
    

    ADD ANY OTHER THING WE MIGHT CONSIDER RELEVANT
    
    This is an example of how to run a command and get more details of the parameters for each command:\n
    python cli.py gif --help
    """
    pass

@click.command()
@click.option('--dir_path', '-d',
              help='Path to the directory with the tiff files.')
@click.option('--save', '-s',
              help='Save the GIF.It will be saved with the same name in the directory passed, with a .gif extension',
              default=False)
def gif(dir_path, save):
    """ 
    This command will generate GIFs for all the tiff files in the directory passed.
    If you do not specify to save, it will display the GIFs instead.
    
    Here is an example of how to save:\n
    python cli.py gif --dir_path path/to/folder --save True
    """

    dir_check(dir_path)

    gif_dic = create_dict(dir_path)

    for plot_i in gif_dic:
        plotter = Plotter(gif_dic[plot_i][0], gif_dic[plot_i][1], 'katielane', desired_contrast=5.0)
        print("Creating GIF")
        plotter.display_gif(save=save)
        # need to fix save function, not working


@click.command()
@click.option('--dir_path', '-d',
              help='Path to the directory with the tiff files.')
@click.option('--save', '-s',
              help='Save the plot.It will be saved with the same name in the directory passed, with a .png extension',
              default=False)
@click.option('--type', '-t', type=click.Choice(['single', 'multiple']),
              help='single or multiple dishes per plot')
# add new option -- dish or whatever, list of integers specifying the actualy dish number.[1, 2, 3]
# for either single or multiple, have options of what dishes
# fix creat_dict in helper function to split on _ and identify the dish number, so its {dish#: (tif, roi)}

def fluo_plot(dir_path, save, type):
    """
    This command will generate a fluorecense plot for each of the tiff:roi pairs in the folder passed.
    If you do not specify to save it will only display the image.
    You can also choose whether you want to plot one dish or multiple dishes per plot.
    
    Here is an example of how to create and save a fluorecense plot with one dish per plot:\n
    python cli.py fluo-plot --dir_path path/to/folder --type single --save True

    """
    dir_check(dir_path)
    plot_dic = create_dict(dir_path)
    
    if type == 'single':
        for plot_i in plot_dic:
            plotter = Plotter(plot_dic[plot_i][0], plot_dic[plot_i][1], 'katielane', desired_contrast=1.0)
            print("Creating Single Fluoresence Over Time Plot")
            plotter.plot_fluor_over_time(save=save)
    elif type == 'multiple':
        pass 


@click.command()
@click.option('--dir_path', '-d',
              help='Path to the directory with the tiff files.')
@click.option('--save', '-s',
              help='Save the plot.It will be saved with the same name in the directory passed, with a .png extension',
              default=False)
@click.option('--type', '-t', type=click.Choice(['single', 'multiple']),
              help='single or multiple dishes per plot')
@click.option('--best_fit', '-bf', 
              help= "Plot the line of best fit onto the decay plot")
@click.option('--color_cell', '-c', 
              help='Will make each cell in the plot a different color')
def decay_plot(dir_path, save, type, best_fit, color_cell):    
    """
    This command will generate a decay plot for each of the tiff:roi pairs in the folder passed.
    If you do not specify to save it will only display the image.
    You can also choose whether you want to plot one dish or multiple dishes per plot.
    Additionally, you can decide whether you want to include the line of best fit onto the plot, 
    and if you want to make each cell in the plot a different color.
    
    Here is an example of how to create and save a fluorecense plot with one dish per plot with each cell being a different color:\n
    python cli.py decay-plot --dir_path path/to/folder --type single --save True --color_cell True

    """
    dir_check(dir_path)
    plot_dic = create_dict(dir_path)
    
    if type == 'single':
        for plot_i in plot_dic:
            plotter = Plotter(plot_dic[plot_i][0], plot_dic[plot_i][1], 'katielane', desired_contrast=1.0)
            print("Creating Single Fluoresence Over Time Plot")
            plotter.plot_decay_over_time(save=save,want_best_fit=best_fit, color_by_cell=color_cell)
    elif type == 'multiple':
        pass 


@click.command()
@click.option('--dir_path', '-d',
              help='Path to the directory with the tiff and roi files.')
def export_csv(dir_path):

    dir_check(dir_path)
    plot_dic = create_dict(dir_path)

    for k, v in plot_dic.items():
        compute_regions(v[0], v[1])
        save_csv(f'{dir_path}/{k}.csv')
        
    print('CSV files have been saved in the directory')

cli.add_command(gif)
cli.add_command(fluo_plot)
cli.add_command(decay_plot)
cli.add_command(export_csv)


if __name__ == "__main__":
    cli()
