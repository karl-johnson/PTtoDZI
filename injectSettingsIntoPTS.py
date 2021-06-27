import json, os, math, subprocess, time
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

def stitchPTGuiRegion(region, pts, file, PTGUI_EXE_PATH):
    # stitch region of panorama to file using PTGui
    # region: [left, top, width, height], all in px, all relative
    #   to current pano extent in pts (including crop)
    # pts: dictionary read from .pts json
    # file: location to save final image (including file)
    # TODO INPUT SANITIZATION
    if region[2] > 65535 || region[3] > 65535:
        print("Error: JPEG does not support region size greater than 65535 ("
            +str(region[2])+"x"+str(region[3]) + ")")
        exit() # TODO throw exception instead
    # get geometry of panorama currently in pts
    resolutionInfo = getResolutionInfo(pts)
    if region[2] > resolutionInfo['h']:
        print("Warning: region width ("+str(region[2])+
            ") greater than panorama width ("+resolutionInfo['h']+")")
    if region[3] > resolutionInfo['v']:
        print("Warning: region height ("+str(region[3])+
            ") greater than panorama height ("+resolutionInfo['v']+")")
    crop = resolutionInfo['crop']
    hopt = resolutionInfo['hopt']
    vopt = resolutionInfo['vopt']
    # calculate crop values to yield specified region
    new_crop = [crop[0] + region[0]/hopt,
        crop[1] + region[1]/vopt,
        crop[0] + (region[0]+region[2])/hopt,
        crop[1] + (region[1]+region[3])/vopt]
    new_res = region[2]*region[3];
    # change json and save
    new_pts = pts
    new_pts['project']['panoramaparams']['outputcrop'] = new_crop
    new_pts['project']['outputsize']['pixels'] = new_res
    new_pts['project']['panoramaparams']['fileformat'] = "jpeg" # TODO make opt
    new_pts['project']['panoramaparams']['outputfile'] = os.path.abspath(file)
    pts_file = os.path.splitext(file)[0]+"_temp_"+str(region[2])+"x"\
        +str(region[3])+"at"+str(region[0])+"_"+str(region[1])+".pts"
    with open(pts_file, 'w') as pts_file_handle:
        json.dump(new_pts, pts_file_handle)
    # call PTGUI
    # command working: & 'C:\Program Files\PTGui\PTGui.exe' -stitchnogui [FILE]
    print("Began stitching "+str(region[2])+"x"+str(region[3])+" region at (" \
        +str(region[0])+", "+str(region[1])+")")
    start = time.time()
    process = subprocess.Popen([PTGUI_EXE_PATH, "-stitchnogui", pts_file], stdout=subprocess.PIPE)
    process.wait()
    print("Stitching complete (" + str(time.time() - start) + " seconds)")
    os.remove(pts_file) # remove PTGui file

PTGUI_EXE_PATH = os.path.join('c:',os.sep,'Program Files','PTGui','PTGui.exe')
pts_in = os.path.join('test','20210612_147megapixels','20210612_pano2.pts')
image_out = os.path.join('test','20210612_147megapixels','outputtest.jpg')
# command working: & 'C:\Program Files\PTGui\PTGui.exe' -stitchnogui [FILE]
pts_path, pts_filename = os.path.split(pts_in)
with open(pts_in) as f:
    pts = json.load(f)
# filter out incompatible projections
if pts['project']['panoramaparams']['projection'] != 'cylindrical':
    print("Error: non-cylindrical projection")
    exit()
stitchPTGuiRegion([0, 0, 4096, 4096], pts, image_out, PTGUI_EXE_PATH)
