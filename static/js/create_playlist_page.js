const discovery_desc = document.getElementById("discovery-description");
const blank_desc = document.getElementById("blank-description");
const surprise_desc = document.getElementById("surprise-description");
const discovery_slider = document.getElementById("playlist-scope-slider");

const discovery_slider_output = document.getElementById("playlist-scope-slider-output")
const dict = {
    1 : "Short Term",
    2 : "Medium Term",
    3 : "Long Term"
}

function sliderOutput(that) {
    discovery_slider_output.innerHTML = dict[Number(that.value)];
}

function descriptionCheck(that) {
    if (that.value == "discovery") {
        discovery_desc.style.display = "block";
        discovery_slider.style.display = "block";
        discovery_slider_output.style.display = "block";
        blank_desc.style.display = "none";
        surprise_desc.style.display = "none";
    }
    else if (that.value == "blank"){
        blank_desc.style.display = "block";
        discovery_desc.style.display = "none";
        discovery_slider.style.display = "none";
        discovery_slider_output.style.display = "none";
        surprise_desc.style.display = "none";
    }
    else {
        surprise_desc.style.display = "block";
        blank_desc.style.display = "none";
        discovery_desc.style.display = "none";
        discovery_slider.style.display = "none";
        discovery_slider_output.style.display = "none";
    }
}