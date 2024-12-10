# Automated Analysis of Calcium Diffusion Dynamics

## Overview
This project focuses on automating the analysis of calcium diffusion dynamics in mouse embryo fibroblast cells. By introducing ATP to trigger calcium release, fluorescence microscopy data is captured and processed to quantify calcium movement. The tool automates the generation of fluorescence decay plots and GIFs, providing an efficient alternative to manual data processing.

The program, written in Python, is designed to be user-friendly for biology students with minimal programming experience. It processes video files (TIFF) and corresponding region of interest (ROI) data, performing error checks and outputting visualizations and data files for further analysis.

---

## Features
1. **Command Line Interface (CLI):**
   - Simplifies user interaction with commands for different functionalities.
   - Validates input files and directories.
   - Provides detailed help messages for each command.

2. **Plotting Options:**
   - Generates fluorescence over time plots.
   - Creates fluorescence decay plots for individual or multiple dishes.
   - Visualizes data with optional line-of-best-fit and cell-specific coloring.

3. **Additional Functionalities:**
   - Converts TIFF video frames into GIFs for easier visualization.
   - Exports processed data as CSV files for additional analysis.

---

## Installation
### Prerequisites
- Python 3.7 or higher
- Required Python libraries:
  - `click`
  - `PIL`
  - `matplotlib`
  - `seaborn`
  - `scipy`
  - `roifile`
  - `tifffile`
  - `argparse`
  - `numpy`
  - `cv2`
  - `pandas`

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/EulerFrog/Project-8.git
   cd Project-8
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
---
## Usage
### General Syntax
  ```bash
  python cli.py <command> [options]
  ```
Commands
1. plot
   ```bash
   python cli.py plot --input <directory> --contrast <value> --type <fluorescence|decay>
   ```
   Options:
   - --input: Directory containing TIFF files and ROI data
   - --contrast: Adjust image contrast for processing
   - --type: Specify plot type (fluorescence or decay)
3. gif
   ```bash
   python cli.py gif -d path/to/dir
5. export_csv
   ```bash
   python cli.py export_csv -d path/to/dir
7. --help
   ```bash
   python cli.py --help
---
## Examples
### Generate a Fluorescence Plot Over Time
```bash
python cli.py plot fluo-plot -d path/to/dir
```
### Generate a Fluorescence Decay Plot (black and white)
```bash
python cli.py plot decay-plot -d path/to/dir {True, False}
```
### Generate a Fluorescence Decay Plot (colored by each cell)
```bash
python cli.py plot decay-plot -d path/to/dir -c {True, False}
```
### Generate a Fluorescence Decay Plot w/ Line of Best Fit (black and white)
```bash
python cli.py plot decay-plot -d path/to/dir -bf True {True, False}
```
### Generate a Fluorescence Decay Plot w/ Line of Best Fit (colored by each cell)
```bash
python cli.py plot decay-plot -d path/to/dir -bf True -c {True, False}
```
---
## Output 
1. Plots:
   - Fluorescence over time
   - Fluorescence decay with optional customization
2. GIFs:
   - Animated visualizations of calcium diffusion
4. CSV Files:
   - Normalized and processed fluorescence data
---
## Contributors
Michelle Fast, Hidemi Mitani Shen, Stella Brown, Joe Ewert, Evan Asche

Affiliations: Computer Science Department, Western Washington University 
