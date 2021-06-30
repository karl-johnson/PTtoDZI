import os, subprocess, time
VIPS_EXE_PATH = os.path.join('c:',os.sep,'include','VIPS','bin','vips.exe')
#vipshome = os.path.join('c:',os.sep,'Program Files','VIPS','bin')
#os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
#import pyvips
def convert(image_in, dzi_out, tile_size, overlap):
    # TODO input sanitization
    print("Began DZI save")
    start = time.time()
    process = subprocess.Popen([VIPS_EXE_PATH, "dzsave", image_in, dzi_out,
        "--tile-size", str(tile_size), "--overlap", str(overlap)], stdout=subprocess.PIPE)
    process.wait()
    print("DZI save complete (" + str(time.time() - start) + " seconds)")

def merge(dzi_filenames, destination):
    files_dir = destination + '_files';
    if len(dzi_filenames) == 1:
        # nothing to do
        return
    # read all inputs to determine format
    #for file in dzi_filenames:
        # info to get: num_x, num_y, tile_size, mosiac_size, res_x, res_y, source_levels
    # determine number of levels in final output
    level_shift = int(math.ceil(math.log(math.max(num_x,num_y),2)))
    tot_levels = source_levels + level_shift
    cross_level = tot_levels - int(math.log(mosaic_size/tile_size,2))
    level = tot_levels[:]
    # higher order levels with mostly rename operations
    while level >= cross_level:
        adjusted_tile_size = tile_size*(2**(tot_levels-level))
        rows = int(math.ceil(res_y/adjusted_tile_size))
        cols = int(math.ceil(res_x/adjusted_tile_size))
        tiles_per_mosaic = mosaic_size/adjusted_tile_size
        for row in range(rows):
            for col in range(cols):
                # TODO handle overlap
                old_tile = os.path.join(str(int(math.floor(col/tiles_per_mosaic)))+'_'
                    +str(int(math.floor(row/tiles_per_mosaic)))+'_files',
                    str(level - level_shift),
                    str(col % tiles_per_mosaic)+'_'+str(row % tiles_per_mosaic)+'.jpeg')
                new_tile = os.path.join(files_dir, str(level),
                    str(col)+'_'+str(row))
                # rename tile to proper name
                os.rename(old_tile, new_tile)
        level -= 1
    # cross over level - always has to append overlap but no merging


    #while level >= 0:
        # use VIPS to stitch together next higher level
