import math
def getTilingRegions(x_size, y_size, tile_size):
    # first get no. of tiles in x and y
    num_x = math.ceil(x_size/tile_size)
    num_y = math.ceil(y_size/tile_size)
    output = []
    for row in range(num_y):
        for col in range(num_x):
            x_start = col*tile_size
            y_start = row*tile_size
            x_end = min((col+1)*tile_size, x_size) # limit to region
            y_end = min((row+1)*tile_size, y_size)
            output.append([x_start, y_start, x_end-x_start, y_end-y_start])
    return output
