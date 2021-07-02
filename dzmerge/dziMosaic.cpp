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

void dziMosaic::lowerMerge(std::string outPath, size_t level) {
/*
 * Merge single lower index DZI level, assuming all higher levels have already been merged
 * The tiles resulting from this merge span multiple input pyramids
 * As such generating these tiles always requires image manipulation
 * Fortunately even for the most extreme cases this will only produce a few hundred images
 *      and disk time will dominate over processing time
 */
    size_t row, rows, col, cols, adjustedTileSize, tilesPerMosaic;
    adjustedTileSize = tileSize << (outputLevels - level);
    // use truncation of casting to size_t + 1 for ceil
    rows = static_cast<size_t>(totalYResolution/adjustedTileSize) + 1;
    cols = static_cast<size_t>(totalXResolution/adjustedTileSize) + 1;
    tilesPerMosaic = mosaicSize/adjustedTileSize;
    std::string sourceTilePath, destTilePath;
    size_t pyrX, pyrY;
    for(row = 0; row < rows; row++) {
        // IF ROW IS TOP_BOTTOM EDGE
        // FIX TWO ROWS AT ONCE
        for(col = 0; col < cols; col++) {
            pyrX = col % tilesPerMosaic; pyrY = row % tilesPerMosaic;
            // TODO: fix details of path formatting
            sourceTilePath = sourcePaths[col/tilesPerMosaic][row/tilesPerMosaic] +
                    std::to_string(level - (outputLevels - inputLevels)) + '\\' +
                    std::to_string(pyrX) + '_' + std::to_string(pyrY) + ".jpeg";
            destTilePath = outPath + "_files\\" + std::to_string(level) +
                    std::to_string(col) + '_' + std::to_string(row) + ".jpeg";
            // TODO CHECK IF OVERLAP FIX IS NEEDED AND PERFORM IT
            // if(IS_LEFT_RIGHT_EDGE)
                // CALL EDGE MERGE TO FIX TWO TILES LEFT/RIGHT

            try {
                std::filesystem::rename(sourceTilePath, destTilePath);
            } catch (std::filesystem::filesystem_error& e) {
                std::cout << e.what() << '\n';
            }
        }
    }
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
