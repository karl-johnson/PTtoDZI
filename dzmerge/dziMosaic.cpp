//
// Created by karl on 6/29/2021.
//

#include "dziMosaic.h"

dziSingle dziMosaic::merge(std::string outPath) {
    dziSingle outputDzi = dziSingle(outPath);
/*
 * Merge this dziMosaic object into a single pyramid and save at outPath
 */
    // generate levels of output mosaic one at a time

    // write XML
}

void dziMosaic::lowerMerge(std::string outPath) {
/*
 * Merge single lower index DZI level, assuming all higher levels have already been merged
 * The tiles resulting from this merge span multiple input pyramids
 * As such generating these tiles always requires image manipulation
 * Fortunately even for the most extreme cases this will only produce a few hundred images
 *      and disk time will dominate over processing time
 */
    // FOR EACH ROW (OF OUTPUT)
        // FOR EACH COLUMN
            // GET IMAGES COMPRISING CORE OF TILE FROM ALREADY MERGED HIGHER LEVELS
            // CONCATENATE
            // CHECK WHAT EDGES/CORNERS NEED OVERLAP
            // APPLY OVERLAP (either from edges or from simple extension)
            // SAVE RESULT
}

void dziMosaic::higherMerge(std::string outPath) {
/*
 * Merge single higher index DZI level
 * These tiles are fully contained in the individual pyramids (except for overlap on edges)
 * As such merging consists of file renaming and occasional padding of images to fix overlap
 */
    // FOR EACH ROW
        // FOR EACH COLUMN
            // GET PATH TO TILE FROM APPROPRIATE PYRAMID
            // IF EDGE/CORNER, LOAD IN AND PERFORM PADDING
            // SAVE TO RESULT FOLDER
}
