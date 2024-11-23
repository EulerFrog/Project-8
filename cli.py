import os
import sys
import click

from plots import Plotter
from helper_fn import dir_check, create_dict

@click.group()
def cli():
    """
    This program will assist you with generating visuals from tif files with their corresponding roi (zip) files.
    Please make sure that the directory (folder path) passed contain tif files with roi files with the same name, except for the extension.
    For example test1.tiff, test1.zip would be a pair of matching files
    Please ensure that in the .zip files, the last roi is the background.
    

    ADD ANY OTHER THING WE MIGHT CONSIDER RELEVANT
    
    This is an example of how to run a command and get more details of the parameters for each command:
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
    """
    print('gif')
    gif_dic = create_dict(dir_path, 'gif')

    for plot_i in gif_dic:
        plotter = Plotter(gif_dic[plot_i][0], gif_dic[plot_i][1], 'katielane', desired_contrast=5.0)
        print("Creating GIF")
        plotter.display_gif(save=save)
        # need to fix save function, not working


@click.command()
@click.option('--dir_path', '-d',
              help='Path to the directory with the tiff files.')
@click.option('--save', '-s',
              help='Save the plot.It will be saved with the same name in the directory passed, with a .gif extension',
              default=False)
@click.option('--title', '-t',
              help='Change title of plot. This only works if the folder only has one pair of tiff:roi files')
@click.option('--type', '-tp', type=click.Choice(['fluo', 'decay']),
              help='fluorecence or decay plots')
def single_plot(dir_path, save, title, type):
    print('gr')
    
        
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
                


cli.add_command(gif)
cli.add_command(single_plot)



if __name__ == "__main__":
    cli()
