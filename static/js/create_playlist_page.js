function descriptionCheck(that) {
    if (that.value == "discovery") {
        document.getElementById("discovery-description").style.display = "block";
        document.getElementById("blank-description").style.display = "none";
        document.getElementById("surprise-description").style.display = "none";
    }
    else if (that.value == "blank"){
        document.getElementById("blank-description").style.display = "block";
        document.getElementById("discovery-description").style.display = "none";
        document.getElementById("surprise-description").style.display = "none";
    }
    else {
        document.getElementById("surprise-description").style.display = "block";
        document.getElementById("blank-description").style.display = "none";
        document.getElementById("discovery-description").style.display = "none";
    }
}