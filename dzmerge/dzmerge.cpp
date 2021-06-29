/*
 * Program to merge multiple DZI image pyramids into a single DZI pyramid
 * This is intended to be used with image pyramids that mosaic a single gigantic image
 * Usage:
 *  dzmerge [OPTIONS] /path/to/dzis /path/to/output
 *
 * The input directory must
 *  - contain a composite number of DZI image pyramids
 *  - all pyramids must have matching tile size and overlap
 *  - excluding those cut off by super-image edge, all pyramids must be the same square size
 *  - combined, the pyramids must completely cover a rectangular region without overlapping
 *  -
 *  -
*/
#include <iostream>
#include "dziMosaic.h"

int main(int argc, const char *argv[]) {
    if(argc != 2) {
        std::cout << "generic bad args message here" << std::endl;
    }
    // TODO add options: overlap handling (extend or true)
    // TODO basic check of argv[1]
    try {
        dziMosaic inputMosaic = dziMosaic(std::string(argv[1]));
    }
    catch (std::invalid_argument&) {
        // some error message iunno
        exit(1);
    }

    exit(0);
}