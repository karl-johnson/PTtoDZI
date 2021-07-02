import os, PTGUItools, DZItools, misctools
DZI_TILE_SIZE = 256
DZI_TILE_OVERLAP = 0
STITCH_TILE_SIZE = 8192 # must be a power of 2 multiple of DZI tile size
pts_in = os.path.join('test','20210612_147megapixels','20210612_pano2.pts')
image_out = os.path.join('test','20210612_147megapixels','dzi_test','stitch.jpg')
final_dzi_out = os.path.join('test','20210612_147megapixels','dzi_test','stitch_dzi')
# command working: & 'C:\Program Files\PTGui\PTGui.exe' -stitchnogui [FILE]
pts_path, pts_filename = os.path.split(pts_in)
pts = PTGUItools.load(pts_in)
temp_dir = os.path.join(pts_path, "dzi_temp")
os.mkdir(temp_dir)
# filter out incompatible projections
if pts['project']['panoramaparams']['projection'] != 'cylindrical':
    print("Error: non-cylindrical projection")
    exit()

# stitch panorama segments using PTGUI
res_info = PTGUItools.getResolutionInfo(pts)
stitch_regions, columns = misctools.getTilingRegions(res_info['h'],
    res_info['v'], STITCH_TILE_SIZE)
dzi_paths = []
for region in stitch_regions:
    image_out = os.path.join(temp_dir, "temp_stitch.jpg")
    PTGUItools.stitch(pts, pts_in, image_out, region)
    # UPDATE DZI FILENAME AND ADD DZIs TO ARRAY
    dzi_out = os.path.join(pts_path,"dzi_temp",
        str(int(region[0]/STITCH_TILE_SIZE))+"_"
        +str(int(region[1]/STITCH_TILE_SIZE)))
    dzi_paths.append(dzi_out)
    # convert output to DZI using VIPS
    DZItools.convert(image_out, dzi_out, 256, 0)
    # delete image_out
    os.remove(image_out)
# MERGE DZI
DZItools.merge(dzi_paths, final_dzi_out)
os.remove(temp_dir)
