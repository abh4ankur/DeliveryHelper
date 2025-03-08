INPUT : 
1.Create APIKEY for google map account using google credentials. Very basic step so no additional info provided here.Replace YOUR_API_KEY in main.py with your key.
2.Addresses.xls is provided as sample input .Update this sheet with actual names and addresses in sheet .Keep this xls in same path where main.py is kept so it can be accessed.

OUTPUT:
1.It would give a scatter plot with red cross as current location and all other blue crosses as provided addresses .
2.Addtional info is shown when you hover over any point.
3.There is option to zoom in and out to cluster of points to get more clear view.

PRE-REQUISITES: 
Below python libraries needs to be installed using pip or brew .

import googlemaps
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import numpy as np 
import pandas as pd
import os 
import requests 

EXECUTE:
Execute main.py and it should open a new window with scatterplot.
