import json, os, math, subprocess
PTGUI_EXE_PATH = os.path.join('c:',os.sep,'Program Files','PTGui','PTGui.exe')
print(PTGUI_EXE_PATH)
pts_in = os.path.join('test','20210612_147megapixels','20210612_pano2.pts')
pts_out = os.path.join('test','20210612_147megapixels','20210612_pytonedit.pts')
# command working: & 'C:\Program Files\PTGui\PTGui.exe' -stitchnogui [FILE]
pts_path, pts_filename = os.path.split(pts_in)
with open(pts_in) as f:
    pts = json.load(f)
data = pts['project']

# filter out incompatible projections
if data['panoramaparams']['projection'] != 'cylindrical':
    print("Error: non-cylindrical projection")
    exit()

# get panorama resolution
if 'pixels' in data['outputsize']:
    pano_resolution = data['outputsize']['pixels']
else:
    print("Total pixels of panorama not found.")
    print("Please select \"Megapixels\" in the \"Create Panorama\" Menu of PTGui.")
pano_hfov = data['panoramaparams']['hfov']
pano_vfov = data['panoramaparams']['vfov']
# specific to cylindrical projection
pano_hraw = math.radians(pano_hfov) # side length on unit cylinder
pano_vraw = 2*math.tan(math.radians(0.5*pano_vfov))
crop = data['panoramaparams']['outputcrop']
pano_hraw_c = pano_hraw*(crop[2]-crop[0]) # include cropping
pano_vraw_c = pano_vraw*(crop[3]-crop[1])
pano_aspectratio = pano_hraw_c/pano_vraw_c
pano_hres = round(math.sqrt(pano_aspectratio*pano_resolution))
pano_vres = round(math.sqrt(pano_resolution/pano_aspectratio))
print(str(pano_hres) + "x" + str(pano_vres))
# test: calculate needed crop values to result in square at NW
# this has to be of the right size to maintain pixel density, even through
# we will be changing the forced # of megapixels
# this amounts to us extracting the optimum max resolution
# for ease best unit for this is # of pixels per side length in uncropped fov
opt_hres = pano_hres/(crop[2]-crop[0])
opt_vres = pano_vres/(crop[3]-crop[1])
desired_output = 4096
new_crop = [crop[0], crop[1],
    crop[0] + (desired_output/opt_hres),
    crop[1] + (desired_output/opt_vres)]
new_res = desired_output**2;

# change json and save
new_pts = pts
new_pts['project']['panoramaparams']['outputcrop'] = new_crop
new_pts['project']['outputsize']['pixels'] = new_res
with open(pts_out, 'w') as outfile:
    json.dump(new_pts, outfile)

# call PTGUI
# command working: & 'C:\Program Files\PTGui\PTGui.exe' -stitchnogui [FILE]
process = subprocess.Popen([PTGUI_EXE_PATH, "-stitchnogui", pts_out],
     stdout=subprocess.PIPE)
while True:
    output = process.stdout.readline()
    if process.poll() is not None:
        break
    if output:
        print(output.strip)
