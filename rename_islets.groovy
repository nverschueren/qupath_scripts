resetSelection();
selectObjectsByClassification("islets");
allislets = getAnnotationObjects().findAll{it.getPathClass() == getPathClass("islets")}

allislets.eachWithIndex{islet, index ->

    islet.setName(index.toString())

}

