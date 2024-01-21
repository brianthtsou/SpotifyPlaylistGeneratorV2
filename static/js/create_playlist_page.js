const discovery_desc = document.getElementById("discovery-description");
const blank_desc = document.getElementById("blank-description");
const surprise_desc = document.getElementById("surprise-description");
const discovery_slider = document.getElementById("playlist-scope-slider");

function descriptionCheck(that) {
    if (that.value == "discovery") {
        discovery_desc.style.display = "block";
        discovery_slider.style.display = "block";
        blank_desc.style.display = "none";
        surprise_desc.style.display = "none";
    }
    else if (that.value == "blank"){
        blank_desc.style.display = "block";
        discovery_desc.style.display = "none";
        discovery_slider.style.display = "none";
        surprise_desc.style.display = "none";
    }
    else {
        surprise_desc.style.display = "block";
        blank_desc.style.display = "none";
        discovery_desc.style.display = "none";
        discovery_slider.style.display = "none";
    }
}