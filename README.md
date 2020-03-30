# aq_main_telemetry
Originally composed by Huanxin Xu circa 2017, this code generates an html file to display realtime bottom temperature observations by fishermen.  It uses the Python "Folium" package.  

Modified by Lei Zhao in June 2019 to add models and climatology
Modified by JiM late 2019 & early 2020 to improve readability for NERACOOS transfer

This program conducts multiple tasks including:
1. Download raw csv files which have been uploaded by 'wifi.py' to studentdrifters.org ("SD" machine)
2. Look for good csv files and makes plot a graph for each good one
3. Create "telemetry.html" using Folium
4. Upload this html and the pngs to the new studentdrifters ftp location

As of this writing, in addition to Folium, it imports  multiple homegrown modules including:
from func_aq import plot_aq
import read_functions as rf
import upload_modules as up
import create_modules_dictionary as cmd

We have a flowchart created using drawio at:
https://www.draw.io/?state=%7B%22ids%22:%5B%221DO7_jVsZ_9ED0jwREfE5BsMzVYsc5gRM%22%5D,%22action%22:%22open%22,%22userId%22:%22100669986945318687835%22%7D#G1OBtQ7KO3neJWH1EkouwoO4_S5DfTXE5g


