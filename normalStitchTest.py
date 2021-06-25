import json
with open('test/20210612_147megapixels/20210612_pano2.pts') as f:
    data = json.load(f)
print(len(data["project"]["imagegroups"]))

# reference nona command
# nona -o nona_stitch_out nona_stitch.txt
