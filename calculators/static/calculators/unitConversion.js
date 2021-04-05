// ---------------------------------------------- //
// Unit Conversions
// ---------------------------------------------- //

// Get DOM Elements
var quickConversionForm = document.getElementById('quickConversionForm');
var quickConversionAlert = document.getElementById('quickConversionAlert');
var quickFrom = document.getElementById('quickFrom');
var quickTo = document.getElementById('quickTo');
var quickResult = document.getElementById('quickResult');

// Function to clear alert
function clearAlert(alert) {
  alert.style.display = 'none';
}

// Listener for Quich Form submit
quickConversionForm.addEventListener('submit', function (event) {
  event.preventDefault(); 
  quickConvert();
})

// Quick convert calculation
function quickConvert() {
  // Remove alert is exists
  clearAlert(quickConversionAlert);

  try {
    fromQty = Qty.parse(quickFrom.value);
    toQty = Qty.parse(quickTo.value);
    
    if (fromQty && toQty) {
      result = fromQty.to(toQty);
    
    } else if (!fromQty && toQty) {
      throw new Error("Can not parse the inputted value for FROM.");
    
    }  else if (fromQty && !toQty) {
      throw new Error("Can not parse the inputted value for TO.");
    
    } else {
      throw new Error("Can't parse the inputted values for FROM and TO.");
    }
    
    quickResult.value = result.toString();

  } catch (error) {
    quickConversionAlert.style.display = 'block';
    quickConversionAlert.innerHTML = error;
  }

}

