# PTtoDZI
Tool to generate DZI format panoramas directly from source images and a PTGUI project file. This allows creation of DZI panoramas for web viewing without having to stitch a single giant image and then break it up into DZI tiles, as is normal for smaller panoramas. It also makes this process require less manual effort.

## Motivation

When stitching extremely large panoramas (>10 gigapixels) to a single output file, the JPEG file format is not an option due to its 65535 pixel per side limit. As such, the output is generally stitched to a BigTIFF file, resulting in very large output files (e.g. 40 GB for a 12 gigapixel panorama). When PTGUI stitches these panoramas, it also uses a very large amount of temp space (~10x the size of the output file). If there is insufficient space for these temp files, the panorama will not stitch. Aside from having enough hard drive space to store the original image tiles and the final panorama, this is the only limitation preventing PTGUI from creating infinitely large panoramas, making it an important limitation to overcome for those looking to stitch extremely large panoramas on fairly normal hardware.

However, for me, this bottleneck is avoidable because I never use the massive singular panorama file itself - I always convert it to a DZI image tile pyramid, containing thousands of small jpegs for dynamic web viewing. By stitching the source camera images straight to the DZI format instead of a single output, I can avoid being limited by the size of my SSD and instead only be limited by the size of the final storage medium. This limit is unavoidable (useful information will always take up nonzero hard drive space) but is also hard to reach in practice. A 1 terapixel panorama's DZI would only take ~5-6 TB of disk space, which is large but totally reasonable on modern HDD's.

## Installation

Need to have Hugin installed and have nona added to your PATH
