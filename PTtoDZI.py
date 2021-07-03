import os, PTGUItools, DZItools, misctools, shutil
# USER PARAMETERS
DZI_TILE_SIZE = 256
DZI_TILE_OVERLAP = 0
STITCH_TILE_SIZE = 4096 # must be a power of 2 multiple of DZI tile size
pts_in = os.path.join('test','20210612_147megapixels','20210612_pano2.pts')
image_out = os.path.join('test','20210612_147megapixels','dzi_test','stitch.jpg')
final_dzi_out = os.path.join('test','20210612_147megapixels','dzi_test','4096_mosaic')

pts_path, pts_filename = os.path.split(pts_in)
pts = PTGUItools.load(pts_in)
temp_dir = os.path.join(pts_path, "dzi_temp")
os.mkdir(temp_dir)
res_info = PTGUItools.getResolutionInfo(pts)
stitch_regions, columns = misctools.getTilingRegions(res_info['h'],
    res_info['v'], STITCH_TILE_SIZE)
dzi_paths = []
for region in stitch_regions:
    image_out = os.path.join(temp_dir, "temp_stitch.jpg")
    PTGUItools.stitch(pts, pts_in, image_out, region)
    # UPDATE DZI FILENAME AND ADD DZIs TO ARRAY
    if len(stitch_regions) == 1: # no need to merge, write to final dir
        dzi_out = final_dzi_out
    else:
        dzi_out = os.path.join(pts_path,"dzi_temp",
            str(int(region[0]/STITCH_TILE_SIZE))+"_"
            +str(int(region[1]/STITCH_TILE_SIZE)))
    dzi_paths.append(dzi_out)
    # convert output to DZI using VIPS
    DZItools.convert(image_out, dzi_out, DZI_TILE_SIZE, DZI_TILE_OVERLAP)
    # delete image_out
    os.remove(image_out)
# MERGE DZI
if len(stitch_regions) != 1:
    DZItools.merge(dzi_paths, final_dzi_out)
shutil.rmtree(temp_dir)
