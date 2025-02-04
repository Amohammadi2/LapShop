# Project Overview

This is an online-shop simulator that has the ability to scrape real data about laptop brands, prices, ram, storage etc... and deal with cutomers through a simple terminal-based user interface, offering them a variety of filters to search for their desired type of products in the inventory.

## Project Setup

Important note: Make sure you already have **chrome** installed on your pc

clone this repository, open it in vs code and run the following commands in your terminal (assuming the active directory is the root folder of the project where `requirements.txt` file is located):

### Step 1 (Optional): Creating A Virtual Environment

It's better to install the dependencies of each project in its own virtual environment in order to avoid later version conflicts and dependency-chain inconsistencies
```ps
C:\example\path\to\LapShop> python -m venv venv
C:\example\path\to\LapShop> . .\venv\scripts\Activate
```

### Step 2: Installing The Requirements

Run this command to install all the packages and libraries required to run this project
```ps
C:\example\path\to\LapShop> python -m pip install -r requirements.txt
```

### Step 3: Initializing The Inventory

after requirements are installed, run the 'init_inventory.py' script to get it going:
```ps
C:\example\path\to\LapShop> python .\init_inventory.py
```

### Step 4 (Final): Run The App
Just run the following command:
```ps
C:\example\path\to\LapShop> python .\main.py
```


## Statistical Analysis And Visualization

To perform statistical analysis on the sales logs, run the 'plotter.py' script
```ps
C:\example\path\to\LapShop> python .\plotter.py
```

Then check the reports folder in the root of the project: `Lapshop\reports`. It contains the generated images of graphs.