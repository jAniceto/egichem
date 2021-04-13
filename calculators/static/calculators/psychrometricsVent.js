// psychrometricsVent.js

// PSYCHROMETRIC VENTILATION SIMULATION
// Javascript functions to calculate psychrometrics of the air/water mixture and
// simulate ventilation operation of a storage room

// Requires:
// psychrolib.js - https://github.com/psychrometrics/psychrolib

// Code by:
// José Aniceto
// EgiChem Group
// CICECO - Aveiro Institute of Materials
// University of Aveiro
// Portugal


// Load psychrolib and set unit system
let psychrolib = new Psychrometrics();
psychrolib.SetUnitSystem(psychrolib.SI);

// Function to clear alert
function clearAlert(alert) {
  alert.style.display = 'none';
}


// --------------------------------------------------- //
// Heating or Cooling
// --------------------------------------------------- //

// Get DOM Elements
var heatCoolForm = document.getElementById('heatCoolForm');
var alertHeatCool = document.getElementById('alertHeatCool');
var refPressInput = document.getElementById('refPress');
var currentTempInput = document.getElementById('currentTemp');
var currentRelHumInput = document.getElementById('currentRelHum');
var currentAbsHumInput = document.getElementById('currentAbsHum');
var finalTempInput = document.getElementById('finalTemp');
var finalRelHumInput = document.getElementById('finalRelHum');
var finalAbsHumInput = document.getElementById('finalAbsHum');
var removWaterInput = document.getElementById('removWater');

heatCoolForm.addEventListener('submit', function (event) { 
  event.preventDefault(); 
  calcPsychrometricsHeatCool();
});


function calcPsychrometricsHeatCool() {
  // Remove alert
  clearAlert(alertHeatCool);
  
  // Get input values
  var refPress = parseFloat(refPressInput.value);
  var currentTemp = parseFloat(currentTempInput.value);
  var currentRelHum = parseFloat(currentRelHumInput.value);
  var finalTemp = parseFloat(finalTempInput.value);
  
  try { 
    // Calculations
    currentAbsHum = psychrolib.GetHumRatioFromRelHum(currentTemp, currentRelHum/100, refPress) * 1000;
    finalRelHum = psychrolib.GetRelHumFromHumRatio(finalTemp, currentAbsHum/1000, refPress) * 100;
    if (finalRelHum > 100) {
      finalRelHum = 100;
    }
    finalAbsHum = psychrolib.GetHumRatioFromRelHum(finalTemp, finalRelHum/100, refPress) * 1000;
    removWater = currentAbsHum - finalAbsHum;
    if (removWater < 0) {
      removWater = 0;
    }
    
    // Display Results
    currentAbsHumInput.value = currentAbsHum.toFixed(2);
    finalRelHumInput.value = finalRelHum.toFixed(1);
    finalAbsHumInput.value = finalAbsHum.toFixed(2);
    removWaterInput.value = removWater.toFixed(2);

  } catch(e) {
    alertHeatCool.style.display = 'block';
    alertHeatCool.innerHTML = e;
  }

}


// --------------------------------------------------- //
// Ventilation system
// --------------------------------------------------- //

var ventForm = document.getElementById('ventForm');
var alertVent = document.getElementById('alertVent');
var inputIntTemp = document.getElementById('inputIntTemp');
var inputIntRelHum = document.getElementById('inputIntRelHum');
var inputExtTemp = document.getElementById('inputExtTemp');
var inputExtRelHum = document.getElementById('inputExtRelHum');
var inputCoolingTemp = document.getElementById('inputCooling');
var inputReheatingTemp = document.getElementById('inputReheating');
var outputIntAbsHum = document.getElementById('intAbsHum');
var outputExtAbsHum = document.getElementById('extAbsHum');
var outputRemovedWater = document.getElementById('removedWater');
var outputTreatedAbsHum = document.getElementById('treatedAbsHum');
var outputTreatedRelHum = document.getElementById('treatedRelHum');
var outputTreatedVapPress = document.getElementById('treatedVapPress');
var outputTreatedSpecVol = document.getElementById('treatedSpecVol');
var outputTreatedSpecEnthal = document.getElementById('treatedSpecEnthal');
var outputTreatedDewPoint = document.getElementById('treatedDewPoint');
var outputTreatedWetBulbTemp = document.getElementById('treatedWetBulbTemp');

ventForm.addEventListener('submit', function (event) { 
  event.preventDefault(); 
  calcPsychrometricsVent();
});


function calcPsychrometricsVent() {
  // Remove alert
  clearAlert(alertVent);

  // Define configuration variables
  const atmosphericPressure = 101325;  // Atmospheric pressure in Pa

  // Inputs
  var intTemp = parseFloat(inputIntTemp.value);
  var intRelHum = parseFloat(inputIntRelHum.value);
  var extTemp = parseFloat(inputExtTemp.value);
  var extRelHum = parseFloat(inputExtRelHum.value);
  var coolingTemp = parseFloat(inputCoolingTemp.value);
  var reheatingTemp = parseFloat(inputReheatingTemp.value);

  try {
    // Validate inputs
    if (reheatingTemp <= coolingTemp) {
      throw new Error("Reheating temperature must be above cooling temperature");
    }

    // Interior Absolute Humidity
    let IntAbsHum = psychrolib.GetHumRatioFromRelHum(
      intTemp, 
      intRelHum/100, 
      atmosphericPressure
    ) * 1000;
    
    // Exterior Absolute Humidity
    let ExtAbsHum = psychrolib.GetHumRatioFromRelHum(
      extTemp, 
      extRelHum/100, 
      atmosphericPressure
    ) * 1000;
    
    // Relative Humidity after cooling
    let CoolRelHum = psychrolib.GetRelHumFromHumRatio(
      coolingTemp, 
      ExtAbsHum/1000, 
      atmosphericPressure
    ) * 100;
    if (CoolRelHum > 100) {
      CoolRelHum = 100;
    }

    // Absolute Humidity after cooling
    let CoolAbsHum = psychrolib.GetHumRatioFromRelHum(
      coolingTemp, 
      CoolRelHum/100, 
      atmosphericPressure
    ) * 1000;

    // Removed water
    let removedWater = ExtAbsHum - CoolAbsHum;

    // Treated Air Absolute Humidity (after reheating)
    let treatedAbsHum = CoolAbsHum;

    // Treated Air Relative Humidity (after reheating)
    let treatedRelHum = psychrolib.GetRelHumFromHumRatio(
      reheatingTemp, 
      treatedAbsHum/1000, 
      atmosphericPressure
    ) * 100;

    // Treated air vapor pressure (after reheating)
    let treatedVapPress = psychrolib.GetVapPresFromHumRatio(
      treatedAbsHum/1000, 
      atmosphericPressure
    );

    // Treated air specific volume (after reheating)
    let treatedSpecVol = psychrolib.GetMoistAirVolume(
      reheatingTemp,
      treatedAbsHum/1000, 
      atmosphericPressure
    );

    // Treated air specific enthalpy (after reheating)
    let treatedSpecEnthal = psychrolib.GetMoistAirEnthalpy(
      reheatingTemp,
      treatedAbsHum/1000
    );

    // Treated air dew point (after reheating)
    let treatedDewPoint = psychrolib.GetTDewPointFromHumRatio(
      reheatingTemp,
      treatedAbsHum/1000, 
      atmosphericPressure
    );

    // Treated air wet bulb temperature (after reheating)
    let treatedWetBulbTemp = psychrolib.GetTWetBulbFromHumRatio(
      reheatingTemp,
      treatedAbsHum/1000, 
      atmosphericPressure
    );

    // Display results
    outputIntAbsHum.value = IntAbsHum.toFixed(1);
    outputExtAbsHum.value = ExtAbsHum.toFixed(1);
    outputRemovedWater.value = removedWater.toFixed(1);
    outputTreatedAbsHum.value = treatedAbsHum.toFixed(1);
    outputTreatedRelHum.value = treatedRelHum.toFixed(0);
    outputTreatedVapPress.value = treatedVapPress.toFixed(1);
    outputTreatedSpecVol.value = treatedSpecVol.toFixed(3);
    outputTreatedSpecEnthal.value = treatedSpecEnthal.toFixed(0);
    outputTreatedDewPoint.value = treatedDewPoint.toFixed(1);
    outputTreatedWetBulbTemp.value = treatedWetBulbTemp.toFixed(1);

  } catch (e) {
    alertVent.style.display = 'block';
    alertVent.innerHTML = e;
  }
}


// --------------------------------------------------- //
// Chart
// --------------------------------------------------- //

// Create Psychrometric Chart
createPsychrometricChart('psychrometricChartVent', 101325);

// Update Psychrometric Chart for Heating/Cooling
function updatePsychrometricChartHeatCool(chartID) {
  let currentTempVal = document.getElementById('currentTemp').value;
  let currentAbsHumVal = document.getElementById('currentAbsHum').value;
  let finalTempVal = document.getElementById('finalTemp').value;
  let finalAbsHumVal = document.getElementById('finalAbsHum').value;

  Plotly.addTraces(chartID, {
    x: [currentTempVal],
    y: [currentAbsHumVal],
    mode: 'markers',
    type: 'scatter',
    marker: {
      size: 10
    },
    hoverinfo: 'name+x+y',
    hoverlabel: {namelength: -1},
    name: 'Current conditions'
  });

  Plotly.addTraces(chartID, {
    x: [finalTempVal],
    y: [finalAbsHumVal],
    mode: 'markers',
    type: 'scatter',
    marker: {
      size: 10
    },
    hoverinfo: 'name+x+y',
    hoverlabel: {namelength: -1},
    name: 'After heating/cooling'
  });
}

heatCoolForm.addEventListener('submit', function(event) { 
  event.preventDefault(); 
  createPsychrometricChart('psychrometricChartVent', 101325);
  updatePsychrometricChartHeatCool('psychrometricChartVent');
});


// Update Psychrometric Chart for Vent
function updatePsychrometricChartVent(chartID) {
  let intTemp = document.getElementById('inputIntTemp').value;
  let intAbsHum = document.getElementById('intAbsHum').value;
  let treatedTemp = document.getElementById('inputReheating').value;
  let treatedAbsHum = document.getElementById('treatedAbsHum').value;
  
  Plotly.addTraces(chartID, {
    x: [intTemp],
    y: [intAbsHum],
    mode: 'markers',
    type: 'scatter',
    marker: {
      size: 10
    },
    hoverinfo: 'name+x+y',
    hoverlabel: {namelength: -1},
    name: 'Before ventilation'
  });

  Plotly.addTraces(chartID, {
    x: [treatedTemp],
    y: [treatedAbsHum],
    mode: 'markers',
    type: 'scatter',
    marker: {
      size: 10
    },
    hoverinfo: 'name+x+y',
    hoverlabel: {namelength: -1},
    name: 'After ventilation (treatment)'
  });
}

ventForm.addEventListener('submit', function(event) { 
  event.preventDefault(); 
  createPsychrometricChart('psychrometricChartVent', 101325);
  updatePsychrometricChartVent('psychrometricChartVent');
});
