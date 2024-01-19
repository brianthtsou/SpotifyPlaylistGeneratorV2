const scope_slider = document.getElementById("scope-slider");
const slider_output = document.getElementById("slider-output");
const dict = {
    1 : "Short Term",
    2 : "Medium Term",
    3 : "Long Term"
}


slider_output.innerHTML = dict[scope_slider.value];

scope_slider.oninput = () => {
    slider_output.innerHTML = dict[scope_slider.value];
}