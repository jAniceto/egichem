// PhD / MSc toggle in Thesis Publications
function phdShow(){
    console.log('phd');
    $('#msc-btn').button('toggle');
    $('#phd-theses').collapse('show');
    $('#msc-theses').collapse('hide');
}

function mscShow(){
    console.log('msc');
    $('#phd-btn').button('toggle');
    $('#phd-theses').collapse('hide');
    $('#msc-theses').collapse('show');
}