import os, subprocess, time, math, copy
import xml.etree.ElementTree as ET
VIPS_EXE_PATH = os.path.join('c:',os.sep,'include','VIPS','bin','vips.exe')
vipshome = os.path.join('c:',os.sep,'include','VIPS','bin')
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips
def convert(image_in, dzi_out, tile_size, overlap):
    # TODO input sanitization
    print("Began DZI save")
    start = time.time()
    process = subprocess.Popen([VIPS_EXE_PATH, "dzsave", image_in, dzi_out,
        "--tile-size", str(tile_size), "--overlap", str(overlap)], stdout=subprocess.PIPE)
    process.wait()
    print("DZI save complete (" + str(time.time() - start) + " seconds)")

def read(DZIin):
    output = dict()
    tree = ET.parse(DZIin)
    root = tree.getroot()
    output['height'] = int(root[0].attrib['Height'])
    output['width'] = int(root[0].attrib['Width'])
    output['format'] = root.attrib['Format']
    output['overlap'] = int(root.attrib['Overlap'])
    output['tile_size'] = int(root.attrib['TileSize'])
    return output

def XMLwrite(dict_in, out_file, reference):
    ET.register_namespace('', "http://schemas.microsoft.com/deepzoom/2008")
    tree = ET.parse(reference)
    tree.getroot()[0].attrib['Height'] = str(dict_in['height'])
    tree.getroot()[0].attrib['Width'] = str(dict_in['width'])
    tree.getroot().attrib['Format'] = dict_in['format']
    tree.getroot().attrib['Overlap'] = str(dict_in['overlap'])
    tree.getroot().attrib['TileSize'] = str(dict_in['tile_size'])
    tree.write(out_file)

def merge_to_lower_level(path, level, overlap):
    if overlap != 0:
        print('Overlap is not yet supported in merge_to_lower_level!')
        exit()
    last_path = os.path.join(path, str(level+1))
    new_path = os.path.join(path, str(level))
    # TODO support overlap
    # populate the specified DZI level from the next higher numbered level
        # using only the tiles already in path
    # due to DZI format, we actually don't need any row/col a priori info!
    # we just need to merge until we run out of files
    # if this is too slow it can be changed but this is nice and elegant
    row = int(0)
    col = int(0)
    while os.path.isfile(os.path.join(last_path,"0_"+str(2*row)+".jpeg")):
        while os.path.isfile(os.path.join(last_path,str(2*col)+'_'+str(2*row)+".jpeg")):
            # load in images comprising single output tile
            images = []
            for y in range(2):
                for x in range(2):
                    image_path = os.path.join(last_path,str(2*col + x)+'_'+str(2*row + y)+".jpeg")
                    if os.path.isfile(image_path):
                        images.append(pyvips.Image.new_from_file(image_path))
            # join images
            if len(images) == 4:
                # arrayjoin
                out = pyvips.Image.arrayjoin(images, across = 2)
                # calculate crop and perform (only if necessary)
                out = out.crop(0,0,images[0].width+images[3].width,images[0].height+images[3].height)
            elif len(images) == 2: # literally an 'edge' case! hahahahahahahaha
                # imo most efficient way to check dir is to see if 1_0 exists
                dir = 'horizontal' if os.path.isfile(os.path.join(last_path,str(2*col + 1)+'_'+str(2*row + 0)+".jpeg")) else 'vertical'
                out = images[0].join(images[1], dir, expand = True)
                # simple join
            else: # single image
                out = images[0]
            # downscale
            out = out.resize(0.5)
            # save output
            out.write_to_file(os.path.join(new_path,str(col)+'_'+str(row)+".jpeg"))
            col += 1
        row += 1

def merge(dzi_paths, destination):
    files_dir = destination + '_files';
    print("Files dir " + files_dir)
    if len(dzi_paths) == 1:
        print("Input is already a single DZI!")
        return # nothing to do, already in a single DZI
    print("Beginning DZI merge: loading in files")
    # get info about first DZI to use as a reference for lots of things
    dzi_info = read(dzi_paths[0] + '.dzi')
    mosaic_size = max(dzi_info['height'], dzi_info['width'])
    tile_size = dzi_info['tile_size']
    # last DZI should encode number of DZI's in X and Y
    source_path, last_name = os.path.split(dzi_paths[-1])
    num_x, num_y = last_name.split('_')
    num_x = int(num_x) + 1
    num_y = int(num_y) + 1
    # read all paths into more convenient data structure and check validity
    sorted_paths = [[None for i in range(num_y)] for j in range(num_x)]
    dzi_num = 0
    for dzi_path in dzi_paths:
        this_info = read(dzi_path + '.dzi')
        if(this_info['tile_size'] != dzi_info['tile_size'] or
            this_info['overlap'] != dzi_info['overlap'] or
            this_info['format'] != dzi_info['format']):
            print(dzi_path + ".dzi does not match first .dzi!")
            exit()
        split_name = os.path.basename(dzi_path).split('_')
        if len(split_name) != 2:
            print("Bad DZI filename")
            exit()
        print(int(split_name[0]),int(split_name[1]))
        sorted_paths[int(split_name[0])][int(split_name[1])] = dzi_path
        dzi_num += 1
    # now that we've checked all the inputs, consolidate info about full image
    # we want to do as few calculations as possible when iterating through tiles
    if num_x * num_y != dzi_num:
        print("DZI inputs don't nicely fill rectangle!")
        exit()
    subdirnames = [os.path.basename(x[0]) for x in os.walk(dzi_paths[0] + '_files')]
    subdirnames.pop(0)
    source_levels = max(int(x) for x in subdirnames)
    res_x = 0
    res_y = 0
    for col_paths in sorted_paths:
        print(col_paths)
        res_x += read(col_paths[0] + '.dzi')['width']
    for first_col_dzi in sorted_paths[0]:
        res_y += read(first_col_dzi + '.dzi')['height']
    # determine number of levels in final output
    level_shift = int(math.ceil(math.log(max(num_x,num_y),2)))
    tot_levels = source_levels + level_shift
    cross_level = tot_levels - int(math.log(mosaic_size/tile_size,2))

    # higher order levels with mostly rename operations
    print("Starting " + str(num_x) + "x" + str(num_y) + "DZI merge of total size"
        + str(res_x) + "x" + str(res_y) + "px")
    start = time.time()
    # first create directories
    if not os.path.isdir(files_dir):
        os.mkdir(files_dir)
    for level in range(tot_levels + 1):
        new_dir = os.path.join(files_dir, str(level))
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)
    level = tot_levels
    files_operations = 0
    while level >= cross_level:
        print("Level " + str(level))
        adjusted_tile_size = tile_size*(2**(tot_levels-level))
        rows = int(math.ceil(res_y/adjusted_tile_size))
        cols = int(math.ceil(res_x/adjusted_tile_size))
        tiles_per_mosaic = mosaic_size/adjusted_tile_size
        for row in range(rows):
            for col in range(cols):
                # TODO handle overlap
                old_tile = os.path.join(source_path,
                    str(int(math.floor(col/tiles_per_mosaic)))+'_'+
                    str(int(math.floor(row/tiles_per_mosaic)))+'_files',
                    str(level - level_shift),
                    str(int(col % tiles_per_mosaic))+'_'+str(int(row % tiles_per_mosaic))+'.jpeg')
                new_tile = os.path.join(files_dir, str(level),
                    str(col)+'_'+str(row))+'.jpeg'
                # print(old_tile,new_tile)
                # rename tile to proper name
                os.rename(old_tile, new_tile)
                files_operations += 1
        level -= 1
    elapsed = time.time() - start
    print("Higher level conversion complete: " +
        str(files_operations) + " moves in " + str(elapsed) + " seconds = " +
        str(files_operations/elapsed) + " files/sec")
    # for the rest of the levels, use VIPS to stitch together next lower level from higher levels
    start = time.time()
    while level >= 0:
        print("Level " + str(level))
        merge_to_lower_level(files_dir, level, 0)
        level -= 1
    elapsed = time.time() - start
    print("Lower level conversion complete in " + str(elapsed) + " seconds")
    # save .dzi XML file
    dzi_info_out = copy.deepcopy(dzi_info)
    dzi_info_out['width'] = res_x
    dzi_info_out['height'] = res_y
    XMLwrite(dzi_info_out, destination + '.dzi', dzi_paths[0] + '.dzi')
#dzi_filenames = ['test\\20210612_147megapixels\\dzi_temp\\0_0', 'test\\20210612_147megapixels\\dzi_temp\\1_0', 'test\\20210612_147megapixels\\dzi_temp\\2_0']
#merge(dzi_filenames, dzi_out)
