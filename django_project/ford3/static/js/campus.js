$(document).ready(function () {
    setPostalAddressEnabled();
})


function setPostalAddressEnabled() {
    let postal_line_1_element = document.getElementById('id_campus-location-postal_address_line_1');
    
    let postal_line_2_element = document.getElementById('id_campus-location-postal_address_line_2');
    let postal_city_element = document.getElementById('id_campus-location-postal_address_city');
    let postal_code_element = document.getElementById('id_campus-location-postal_address_postal_code');
    let postal_address_does_differ = document.getElementById("id_campus-location-postal_address_differs").checked;
    if (postal_address_does_differ) {
        postal_line_1_element.required = true;
        postal_line_2_element.required = true;
        postal_city_element.required = true;
        postal_code_element.required = true;
        postal_line_1_element.disabled = false;
        postal_line_2_element.disabled = false;
        postal_city_element.disabled = false;
        postal_code_element.disabled = false;
    }
    else {
        postal_line_1_element.required = false;
        postal_line_2_element.required = false;
        postal_city_element.required = false;
        postal_code_element.required = false;
        postal_line_1_element.disabled = true;
        postal_line_2_element.disabled = true;
        postal_city_element.disabled = true;
        postal_code_element.disabled = true;
    }
}

$('#id_campus-location-postal_address_differs').click(function(e) {
    setPostalAddressEnabled()
});
