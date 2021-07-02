//
// Created by karl on 6/29/2021.
//

#ifndef DZMERGE_DZIMOSAIC_H
#define DZMERGE_DZIMOSAIC_H

#include <cstdio>
#include <string>
#include <vector>
#include "dziSingle.h"
#include <filesystem>
#include <iostream>


class dziMosaic {
public:
    explicit dziMosaic(std::string path) {
        // load all DZI info into object and check it
    }
    dziSingle merge(std::string outPath);
    // members:
    // TODO CALCULATE ALL OF THESE IN CONSTRUCTOR
    size_t tileSize; // source tile size
    size_t mosaicSize;// source supertile size (spacing of mosaic tiles)
    size_t mosaicX, mosaicY; // number of mosaic tiles
    size_t totalXResolution, totalYResolution; // combined size of mosaic
    size_t inputLevels, outputLevels; // number of levels in input/output and their difference
    std::vector<std::vector<std::string>> sourcePaths; // paths to where individual DZI pyramids are stored
private:
    void lowerMerge(std::string outPath, size_t level)
    void higherMerge(std::string outPath);
};


#endif //DZMERGE_DZIMOSAIC_H
