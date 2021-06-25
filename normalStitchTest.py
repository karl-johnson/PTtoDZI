import json
import os
import math
pts_path = 'test/20210612_147megapixels/20210612_pano2.pts'
output_path, pts_filename = os.path.split(pts_path)
print(output_path)
with open(pts_path) as f:
    pts = json.load(f)
data = pts['project']
#print(len(data["project"]["imagegroups"]))
nona_script_path = os.path.join(output_path, 'nona_temp_script.txt')
if os.path.exists(nona_script_path):
    os.remove(nona_script_path)
nona_script = open(nona_script_path, 'x')
# Get panorama parameters and write "p" line to script
nona_script.write('p ')
# Prior to setting image params, copy lens database
# todo: E parameters
# for some reason PTGUI does not store resolution in the files
# it only (sometimes) stores the # of pixels in image + X&Y panorama extent
if 'pixels' in data['outputsize']:
    outputsize = data['outputsize']['pixels']
else:
    print("Total pixels of panorama not found.")
    print("Please select \"Megapixels\" in the \"Create Panorama\" Menu of PTGui.")
width_deg = data['panoramaparams']['hfov']
height_deg = data['panoramaparams']['vfov']
width_px = round(math.sqrt((width_deg/height_deg)*outputsize))
height_px = round(math.sqrt((height_deg/width_deg)*outputsize))
nona_script.write('w' + str(width_px) + ' ')
nona_script.write('h' + str(height_px) + ' ')
nona_script.write('f0 ') # TODO MAKE THIS AUTOMATICALLY SWITCH

nona_script.write('v' + str(data['panoramaparams']['hfov']) + ' ')
nona_script.write('nJPEG \n')
# Iterate through imagegroups and write "i" lines
imagegroups = data['imagegroups']

# reference nona command
# nona -o nona_stitch_out nona_stitch.txt
# TODO DELETE TEMP SCRIPT
