const discovery_desc = document.getElementById("discovery-description");
const blank_desc = document.getElementById("blank-description");
const surprise_desc = document.getElementById("surprise-description");
const discovery_slider = document.getElementById("playlist-scope-slider");
const genre_select_list = document.getElementById("genre-select");

const discovery_slider_output = document.getElementById(
  "playlist-scope-slider-output"
);
const dict = {
  1: "Short Term",
  2: "Medium Term",
  3: "Long Term",
};

function sliderOutput(that) {
  discovery_slider_output.innerHTML = dict[Number(that.value)];
}

function descriptionCheck(that) {
  if (that.value == "discovery") {
    discovery_desc.style.display = "block";
    discovery_slider.style.display = "block";
    discovery_slider_output.style.display = "block";
    discovery_slider.style.textAlign = "center";
    blank_desc.style.display = "none";
    surprise_desc.style.display = "none";
    genre_select_list.style.display = "none";
  } else if (that.value == "blank") {
    blank_desc.style.display = "block";
    discovery_desc.style.display = "none";
    discovery_slider.style.display = "none";
    discovery_slider_output.style.display = "none";
    surprise_desc.style.display = "none";
    genre_select_list.style.display = "none";
  } else {
    surprise_desc.style.display = "block";
    genre_select_list.style.display = "block";
    blank_desc.style.display = "none";
    discovery_desc.style.display = "none";
    discovery_slider.style.display = "none";
    discovery_slider_output.style.display = "none";
  }
}

// const verified = [];
// genre_select_list.onchange = function(e) {
//   if (genre_select_list.querySelectorAll("option:checked").length <= 5) {
//     verified = Array.apply(null, genre_select_list.querySelectorAll('option:checked'));
//   }
//   else {
//     Array.apply(null, genre_select_list.querySelectorAll('option')).forEach(function(e)) {
//       e.selected = verified.indexOf(e) > -1;
//     }
//   }
// };
