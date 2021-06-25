import json
import os
import math
pts_path = 'test/20210612_147megapixels/20210612_pano2.pts'
output_path, pts_filename = os.path.split(pts_path)
#print(output_path)
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
# todo: E parameter
# for some reason PTGUI does not store x and y resolution in the files
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
nona_script.write('f1 ') # TODO MAKE THIS AUTOMATICALLY SWITCH
nona_script.write('v' + str(data['panoramaparams']['hfov']) + ' ')
nona_script.write('u50 ')
nona_script.write('nJPEG \n')
# Shortcut to lens database
globallenses = data['globallenses']
# Iterate through imagegroups and write "i" lines
imagegroups = data['imagegroups']
for image in imagegroups:
    nona_script.write('i f0 ') # TODO fix projection
# params to add: d e g t Eev Er Eb Vm Va-d
    lens = globallenses[image['globallens']]
    #print(lens)

    diagfov = math.degrees(2*math.atan(lens['lens']['params']['sensordiagonal']/(2*lens['lens']['params']['focallength'])))
    aspect_ratio = image['size'][1]/image['size'][0]
    hfov = diagfov*math.sqrt(1/(1+aspect_ratio**2))
    #hfov = 20
    nona_script.write('v'+str(hfov)+' ')
    nona_script.write('y'+str(image['position']['params']['yaw'])+' ')
    nona_script.write('p'+str(image['position']['params']['pitch'])+' ')
    nona_script.write('r'+str(image['position']['params']['roll'])+' ')
    nona_script.write('a'+str(lens['lens']['params']['a'])+' ')
    nona_script.write('b'+str(lens['lens']['params']['b'])+' ')
    nona_script.write('c'+str(lens['lens']['params']['c'])+' ')

    nona_script.write('n\"'+image['images'][0]['filename']+'\" \n')
# reference nona command
# nona -v -d -g -o nona_stitch_out nona_temp_script.txt
nona_script.write('*')
# nona -o nona_stitch_out nona_stitch.txt
# TODO DELETE TEMP SCRIPT
