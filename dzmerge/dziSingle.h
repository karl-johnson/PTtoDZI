#include <utility>

//
// Created by karl on 6/29/2021.
//

#ifndef DZMERGE_DZISINGLE_H
#define DZMERGE_DZISINGLE_H


struct dziSingle {
    dziSingle(std::string path, size_t tileSize, size_t overlap, size_t width, size_t height)
        : path(std::move(path)), tileSize(tileSize), overlap(overlap), width(width), height(height) {}
/*
 * Struct to store info about a single dzi image pyramid
 *
 */
    void writeXML() {
        // write an XML describing this DZI image pyramid to the internal path
    }
    std::string path; // location on disk (folder that images and .dzi are contained in)
    size_t tileSize;
    size_t overlap;
    size_t width;
    size_t height;
};


#endif //DZMERGE_DZISINGLE_H
