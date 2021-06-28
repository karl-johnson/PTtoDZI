import os, PTGUItools, DZItools
pts_in = os.path.join('test','20210612_147megapixels','20210612_pano2.pts')
image_out = os.path.join('test','20210612_147megapixels','dzi_test','stitch.jpg')
dzi_out = os.path.join('test','20210612_147megapixels','dzi_test','stitch_dzi.zip')
# command working: & 'C:\Program Files\PTGui\PTGui.exe' -stitchnogui [FILE]
pts_path, pts_filename = os.path.split(pts_in)
pts = PTGUItools.load(pts_in)
# filter out incompatible projections
if pts['project']['panoramaparams']['projection'] != 'cylindrical':
    print("Error: non-cylindrical projection")
    exit()

# stitch panorama using PTGUI
PTGUItools.stitch(pts, pts_in, image_out)

# convert output to DZI using VIPS
DZItools.convert(image_out, dzi_out, 256, 0)
