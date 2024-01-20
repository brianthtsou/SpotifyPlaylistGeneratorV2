const scope_slider = document.getElementById("scope-slider");
const scope_slider_output = document.getElementById("scope-slider-output");
const dict = {
    1 : "Short Term",
    2 : "Medium Term",
    3 : "Long Term"
}

const num_slider = document.getElementById("num-slider");
const num_slider_output = document.getElementById("num-slider-output");

scope_slider_output.innerHTML = dict[scope_slider.value];
num_slider_output.innerHTML = num_slider.value;

scope_slider.oninput = () => {
    scope_slider_output.innerHTML = dict[scope_slider.value];
}

num_slider.oninput = () => {
    num_slider_output.innerHTML = num_slider.value;
}