#!/bin/bash
set -e -u


cp -r 0.orig 0
blockMesh
surfaceFeatureExtract
snappyHexMesh -overwrite
setWaveParameters
setFields
setWaveField
