// PhD / MSc toggle in Thesis Publications ////////////////////////////////////////////
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

// People Read More button ////////////////////////////////////////////////////////////
function toggleDisplay(element) {
  // Toggles display property
  if (element.style.display === "none") {
    element.style.display = "block";
  } else {
    element.style.display = "none";
  }
}

function checkOverflow(el) {
// Determines if the element is overflowing its bounds, either vertically or horizontally.
// Will temporarily modify the "overflow" style to detect this if necessary.
  var curOverflow = el.style.overflow;
   
  if ( !curOverflow || curOverflow === "visible" )
    el.style.overflow = "hidden";
   
  var isOverflowing = el.clientWidth < el.scrollWidth || el.clientHeight < el.scrollHeight;
  el.style.overflow = curOverflow;
  return isOverflowing;
}

function expandElement(el) {
  el.classList.remove("truncate");
}

let expandableCards = document.querySelectorAll('.expandable-card');
expandableCards.forEach(card => {
  let truncateDiv = card.querySelector('.truncate');
  if (checkOverflow(truncateDiv)) {
    let readMoreButton = card.querySelector('.read-more');
    toggleDisplay(readMoreButton);
  }
});
