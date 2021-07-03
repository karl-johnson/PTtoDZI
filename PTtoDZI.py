import os, PTGUItools, DZItools, misctools, shutil, math
# USER PARAMETERS
DZI_TILE_SIZE = 256
DZI_TILE_OVERLAP = 0
STITCH_TILE_SIZE = 32768 # must be a power of 2 multiple of DZI tile size
#pts_in = os.path.join('test','20210612_147megapixels','corner_test.pts')
pts_in = os.path.join('c:', os.sep, 'Users','k','Panorama_Stitching',
    '20210618','20210618_lincolnlake_copy.pts')
#final_dzi_out = os.path.join('test','20210612_147megapixels','dzi_test','gigapixel_test')
final_dzi_out = os.path.join('c:', os.sep, 'Users','k','Panorama_Stitching',
    '20210618','PTtoDZI','LincolnLakeAuto')
# TODO WARNING IF ON ANOTHER DRIVE
# FUTURE TODO: ALLOW FINAL SAVE TO ANOTHER DRIVE

pts_path, pts_filename = os.path.split(pts_in)
pts = PTGUItools.load(pts_in)
temp_dir = os.path.join(pts_path, "dzi_temp")
os.mkdirs(temp_dir)
res_info = PTGUItools.getResolutionInfo(pts)
stitch_regions = misctools.getTilingRegions(res_info['h'],
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
    # very last DZI a very tiny corner rectangle, which messes up folder numbering
    # ratio max side length on first tile / max length on corner determines this
    corner_size_ratio = STITCH_TILE_SIZE/max(stitch_regions[-1][2],stitch_regions[-1][3])
    if corner_size_ratio > 2:
        DZItools.shift_folders(dzi_paths[-1],
            math.floor(math.log(corner_size_ratio,2)))
    DZItools.merge(dzi_paths, final_dzi_out)
shutil.rmtree(temp_dir)
