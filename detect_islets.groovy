setImageType('FLUORESCENCE');
resetSelection();
addPixelClassifierMeasurements("islet_class", "islet_class")
resetSelection();
createAnnotationsFromPixelClassifier("islet_class", 200.0, 0.0, "SPLIT", "DELETE_EXISTING")
classifyDetectionsByCentroid("islet_class")
selectObjects {
   return it.isAnnotation() && it.getPathClass() == getPathClass('islet')
}
runPlugin('qupath.imagej.detect.cells.WatershedCellDetection', '{"detectionImage": "DAPI",  "requestedPixelSizeMicrons": 0.5,  "backgroundRadiusMicrons": 8.0,  "medianRadiusMicrons": 0.0,  "sigmaMicrons": 1.0,  "minAreaMicrons": 5.0,  "maxAreaMicrons": 200.0,  "threshold": 15.0,  "watershedPostProcess": true,  "cellExpansionMicrons": 5.0,  "includeNuclei": true,  "smoothBoundaries": true,  "makeMeasurements": true}');