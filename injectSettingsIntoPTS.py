import json, os, math, subprocess
def getResolutionInfo(pts):
    # get information about resolution and geometry of panorama
    return_dict = dict()
    if 'pixels' in pts['project']['outputsize']:
        pano_resolution = pts['project']['outputsize']['pixels']
    else:
        print("Total pixels of panorama not found.")
        print("Please select \"Megapixels\" in the \"Create Panorama\" Menu of PTGui.")
    pano_hfov = pts['project']['panoramaparams']['hfov']
    pano_vfov = pts['project']['panoramaparams']['vfov']
    # specific to cylindrical projection
    pano_hraw = math.radians(pano_hfov) # side length on unit cylinder
    pano_vraw = 2*math.tan(math.radians(0.5*pano_vfov))
    crop = pts['project']['panoramaparams']['outputcrop']
    pano_hraw_c = pano_hraw*(crop[2]-crop[0]) # include cropping
    pano_vraw_c = pano_vraw*(crop[3]-crop[1])
    pano_aspectratio = pano_hraw_c/pano_vraw_c
    return_dict['h'] = round(math.sqrt(pano_aspectratio*pano_resolution))
    return_dict['v'] = round(math.sqrt(pano_resolution/pano_aspectratio))
    # having the optimum pixel density in terms of the crop ratios is useful
    return_dict['hopt'] = return_dict['h']/(crop[2]-crop[0])
    return_dict['vopt'] = return_dict['v']/(crop[3]-crop[1])
    return_dict['crop'] = crop
    return return_dict

def stitchPTGuiRegion(region, pts, path_out):
    # stitch region of panorama to file using PTGui
    # region: [left, top, width, height], all in px, all relative
    #   to current pano extent (including crop)
    # pts: dictionary read from .pts json
    # path_out: location to save final image (including filename)

    # TODO INPUT SANITIZATION

    # get geometry of panorama currently in pts
    resolutionInfo = getResolutionInfo(pts)
    crop = resolutionInfo['crop']
    hopt = resolutionInfo['hopt']
    vopt = resolutionInfo['vopt']
    # LOOKS LIKE THIS MIGHT BE WRONG!
    new_crop = [crop[0] + region[0]/hopt,
        crop[1] + region[1]/vopt,
        crop[0] + (region[0]+region[2])/hopt,
        crop[1] + (region[1]+region[3])/vopt]
    new_res = desired_output**2;
    # change json and save
    new_pts = pts
    new_pts['project']['panoramaparams']['outputcrop'] = new_crop
    new_pts['project']['outputsize']['pixels'] = new_res
    new_pts['project']['panoramaparams']['outputfile'] = path_out
    with open(pts_out, 'w') as outfile:
        json.dump(new_pts, outfile)
    # call PTGUI
    # command working: & 'C:\Program Files\PTGui\PTGui.exe' -stitchnogui [FILE]
    process = subprocess.Popen([PTGUI_EXE_PATH, "-stitchnogui", pts_out], stdout=subprocess.PIPE)
    #process = subprocess.Popen(["PTGui.exe", "-stitchnogui", pts_out], stdout=subprocess.PIPE)

PTGUI_EXE_PATH = os.path.join('c:',os.sep,'Program Files','PTGui','PTGui.exe')
pts_in = os.path.join('test','20210612_147megapixels','20210612_pano2.pts')
pts_out = os.path.join('test','20210612_147megapixels','20210612_pytonedit.pts')
image_out = os.path.join('test','20210612_147megapixels','outputtest.jpg')
# command working: & 'C:\Program Files\PTGui\PTGui.exe' -stitchnogui [FILE]
pts_path, pts_filename = os.path.split(pts_in)
with open(pts_in) as f:
    pts = json.load(f)

# filter out incompatible projections
if pts['project']['panoramaparams']['projection'] != 'cylindrical':
    print("Error: non-cylindrical projection")
    exit()
stitchPTGuiRegion([0, 0, 4096, 4096], pts, image_out)
