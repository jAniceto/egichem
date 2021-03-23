// ---------------------------------------------- //
// PSYCHROMETRIC CALCULATIONS
// ---------------------------------------------- //


// Load psychrolib and set unit system
let psychrolib = new Psychrometrics();
psychrolib.SetUnitSystem(psychrolib.SI);

// Get DOM Elements
var psychrometricsForm = document.getElementById('psychrometricsForm');
var alert = document.getElementById('alert');
var refPressInput = document.getElementById('refPress');
var dryBulbTempInput = document.getElementById('dryBulbTemp');
var relHumInput = document.getElementById('relHum');
var absHumInput = document.getElementById('absHum');
var wetBulbTempInput = document.getElementById('wetBulbTemp');
var dewPointTempInput = document.getElementById('dewPointTemp');
var vapPressInput = document.getElementById('vapPress');
var specVolInput = document.getElementById('specVol');
var specEnthalInput = document.getElementById('specEnthal');


function handleForm(event) { 
  event.preventDefault(); 
  calculatePsychrometrics();
} 

psychrometricsForm.addEventListener('submit', handleForm);


function calculatePsychrometrics() {
  // Remove alert
  clearAlert();
  
  // Get input values
  var refPress = parseFloat(refPressInput.value);
  var dryBulbTemp = parseFloat(dryBulbTempInput.value);
  var relHum = parseFloat(relHumInput.value);
  var absHum = parseFloat(absHumInput.value);
  var wetBulbTemp = parseFloat(wetBulbTempInput.value);
  var dewPointTemp = parseFloat(dewPointTempInput.value);
  var vapPress = parseFloat(vapPressInput.value);
  var specVol = parseFloat(specVolInput.value);
  var specEnthal = parseFloat(specEnthalInput.value);

  try {
    // Calculate depending on the inputs provided
    if ((dryBulbTemp && wetBulbTemp && relHum) || (dryBulbTemp && wetBulbTemp && absHum) || (dryBulbTemp && relHum && absHum) || (wetBulbTemp && relHum && absHum) || (dryBulbTemp && wetBulbTemp && relHum && absHum)) {
      // More than 2 properties provided
      throw new Error("Only two variables can be defined in addition to the reference pressure");

    } else if (!dryBulbTemp && !wetBulbTemp && !relHum && !absHum) {
      throw new Error("Insufficient data provided");
      
    } else if (dryBulbTemp && relHum) {
      // dryBulbTemp and relHum provided
      absHum = psychrolib.GetHumRatioFromRelHum(
        dryBulbTemp, 
        relHum/100, 
        refPress
      ) * 1000;

      wetBulbTemp = psychrolib.GetTWetBulbFromHumRatio(
        dryBulbTemp,
        absHum/1000, 
        refPress
      );

      // Display Results
      absHumInput.value = absHum.toFixed(2);
      wetBulbTempInput.value = wetBulbTemp.toFixed(1);
      
    } else if (dryBulbTemp && absHum) {
      // dryBulbTemp and absHum provided
      relHum = psychrolib.GetRelHumFromHumRatio(
        dryBulbTemp, 
        absHum/1000, 
        refPress
      ) * 100;
      if (relHum > 100) {
        relHum = 100;
      }

      wetBulbTemp = psychrolib.GetTWetBulbFromHumRatio(
        dryBulbTemp,
        absHum/1000, 
        refPress
      );

      // Display Results
      relHumInput.value = relHum.toFixed(1);
      wetBulbTempInput.value = wetBulbTemp.toFixed(1);

    } else if (dryBulbTemp && wetBulbTemp) {
      // dryBulbTemp and wetBulbTemp provided
      relHum = psychrolib.GetRelHumFromTWetBulb(
        dryBulbTemp, 
        wetBulbTemp, 
        refPress
      ) * 100;
      if (relHum > 100) {
        relHum = 100;
      }

      absHum = psychrolib.GetHumRatioFromRelHum(
        dryBulbTemp, 
        relHum/100, 
        refPress
      ) * 1000;

      // Display Results
      relHumInput.value = relHum.toFixed(1);
      absHumInput.value = absHum.toFixed(2);

    } else {
      throw new Error("Insufficient data provided");
    }

    // Calculate remaining properties
    dewPointTemp = psychrolib.GetTDewPointFromHumRatio(
      dryBulbTemp,
      absHum/1000, 
      refPress
    );
    
    vapPress = psychrolib.GetVapPresFromHumRatio(
      absHum/1000, 
      refPress
    );

    specVol = psychrolib.GetMoistAirVolume(
      dryBulbTemp,
      absHum/1000, 
      refPress
    );

    specEnthal = psychrolib.GetMoistAirEnthalpy(
      dryBulbTemp,
      absHum/1000
    );

    // Display remaining results
    dewPointTempInput.value = dewPointTemp.toFixed(1);
    vapPressInput.value = vapPress.toFixed(0);
    specVolInput.value = specVol.toFixed(3);
    specEnthalInput.value = specEnthal.toFixed(0);

  } catch (e) {
    alert.style.display = 'block';
    alert.innerHTML = e;
  }

}

// Function to clear all inputs
function clearAlert() {
  alert.style.display = 'none';
}