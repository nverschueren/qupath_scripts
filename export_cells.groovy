resetSelection();
//selectObjectsByClassification("islet"); // This is not doing anything at the moment
selectCells();
//selectObjectsByClassification("islet", "alpha_cell");
// fix the directory and export

//path="/home/nverschueren/exeter_2nd_postdoc/diabetes_coll/human_islet/qu_path_projects/project_4_july_control_16/exported_data";
path="/home/nverschueren/exeter_2nd_postdoc/diabetes_coll/human_islet/qu_path_projects/jt_T1D_control/exported_data"
dire="cells/";
imname = getCurrentImageData();
fend="_cells.geojson"
exportSelectedObjectsToGeoJson(path+dire+imname+fend, "FEATURE_COLLECTION")

resetSelection();
selectObjectsByClassification("islet"); // This is not doing anything at the moment
dire="islet_border/";
imname = getCurrentImageData();
fend="_border.geojson"
exportSelectedObjectsToGeoJson(path+dire+imname+fend, "FEATURE_COLLECTION")



// it works and it is kind of OK.  The names are too long and cause problems with python. This is why I wrote the script rena.bash,
// which will rename the files as 1,2,3,... etc.
// I am not happy with just exporting a bunch of cells with zero awareness of their parent object. 