//
// Created by karl on 6/29/2021.
//

#ifndef DZMERGE_DZIMOSAIC_H
#define DZMERGE_DZIMOSAIC_H

#include <cstdio>
#include <string>
#include "dziSingle.h"

class dziMosaic {
public:
    explicit dziMosaic(std::string path) {
        // load all DZI info into object and check it
    }
    dziSingle merge(std::string outPath);
    // members:
    // source tile size
    // source supertile size
    // source mosaic size
    // path to root of mosaic
private:
    void lowerMerge(std::string outPath);
    void higherMerge(std::string outPath);
};


#endif //DZMERGE_DZIMOSAIC_H
