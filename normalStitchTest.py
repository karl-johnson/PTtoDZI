import json, os, math, subprocess
pts_path = os.path.join('test','20210612_147megapixels','20210612_pano2.pts')
#pts_path = 'C:/Users/k/Panorama_stitching/PTtoDZItesting/20210612/20210612_pano2.pts'
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
# this is only for cylindrical projection!
pano_aspectratio = math.radians(width_deg)/(2*math.tan(math.radians(0.5*height_deg)))
width_px = round(math.sqrt(pano_aspectratio*outputsize))
height_px = round(math.sqrt(outputsize/pano_aspectratio))
nona_script.write('w' + str(width_px) + ' ')
nona_script.write('h' + str(height_px) + ' ')
# now find and apply crop dimensions

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
# params to add: g t Eev Er Eb Vm Va-d
    lens = globallenses[image['globallens']]
    aspect_ratio = image['size'][1]/image['size'][0]
    sensorhoriz = lens['lens']['params']['sensordiagonal']*math.sqrt(1/(1+aspect_ratio**2));
    hfov = math.degrees(2*math.atan(sensorhoriz/(2*lens['lens']['params']['focallength'])))
    nona_script.write('v'+str(hfov)+' ')
    nona_script.write('y'+str(image['position']['params']['yaw'])+' ')
    nona_script.write('p'+str(image['position']['params']['pitch'])+' ')
    nona_script.write('r'+str(image['position']['params']['roll'])+' ')
    nona_script.write('a'+str(lens['lens']['params']['a'])+' ')
    nona_script.write('b'+str(lens['lens']['params']['b'])+' ')
    nona_script.write('c'+str(lens['lens']['params']['c'])+' ')
    if image['size'][0] > image['size'][1]:
        nona_script.write('d'+str(lens['lens']['shift']['longside'])+' ')
        nona_script.write('e'+str(lens['lens']['shift']['shortside'])+' ')
    else:
        nona_script.write('d'+str(lens['shift']['params']['shortside'])+' ')
        nona_script.write('e'+str(lens['shift']['params']['longside'])+' ')
    nona_script.write('Vm1 ') # DETECT OR DISABLE
    nona_script.write('Va'+str(lens['photometric']['vignettingcoefficients'][0])+' ')
    nona_script.write('Vb'+str(lens['photometric']['vignettingcoefficients'][1])+' ')
    nona_script.write('Vc'+str(lens['photometric']['vignettingcoefficients'][2])+' ')
    nona_script.write('Vd'+str(lens['photometric']['vignettingcoefficients'][3])+' ')
    nona_script.write('Ra'+str(lens['photometric']['emorparams'][0])+' ')
    nona_script.write('Rb'+str(lens['photometric']['emorparams'][1])+' ')
    nona_script.write('Rc'+str(lens['photometric']['emorparams'][2])+' ')
    nona_script.write('Rd'+str(lens['photometric']['emorparams'][3])+' ')
    nona_script.write('Re'+str(lens['photometric']['emorparams'][4])+' ')
    nona_script.write('n\"'+image['images'][0]['filename']+'\" \n')
nona_script.write('*')
nona_script.close()
# reference nona command
# nona -v -d -g -o nona_stitch_out nona_temp_script.txt
process = subprocess.Popen(
    ["nona", "-v", "-g", "--seam=blend", "-o",  os.path.join(output_path,"output_fixed_ratio"), nona_script_path],
     stdout=subprocess.PIPE)
while True:
    output = process.stdout.readline()
    if process.poll() is not None:
        break
    if output:
        print(output.strip)
# nona -o nona_stitch_out nona_stitch.txt
#
# enblend -o emblend.jpg emblend_temp\e*
# TODO DELETE TEMP
