import os, PTGUItools, DZItools, misctools
STITCH_TILE_SIZE = 32768 # easy if power of 2
DZI_TILE_SIZE = 256
DZI_TILE_OVERLAP = 1
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

# stitch panorama segments using PTGUI
res_info = getResolutionInfo(pts)
stitch_regions = misctools.getTilingRegions(res_info.h, res_info.v, STITCH_TILE_SIZE)
for region in stitch_regions:
    # UPDATE DZI FILENAME AND ADD DZIs TO ARRAY
    PTGUItools.stitch(pts, pts_in, image_out, region)
    # convert output to DZI using VIPS
    DZItools.convert(image_out, dzi_out, 256, 0)
    # delete image_out

# MERGE DZI
# REMEMBER THAT LOWER RIGHT CORNER HAS TO BE TREATED SPECIAL
DZItools.merge(dzi_list, final_output_location)
