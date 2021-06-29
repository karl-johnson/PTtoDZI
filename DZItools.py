import os, subprocess, time
VIPS_EXE_PATH = os.path.join('c:',os.sep,'Program Files','VIPS','bin','vips.exe')
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

def merge(files, columns):
    # simple abstraction to invoke merger, written in C++ for speed
    # read all inputs to determine format
    # determine number of levels in final output
    # for each dzi level... (from most detailed to first detail with 1 tile)
    # for each row
    # for each column
    # if corner or edge, append pixels to edge
    # rename tile to proper name
    # REMEMBER THAT LOWER RIGHT CORNER HAS TO BE TREATED SPECIAL
