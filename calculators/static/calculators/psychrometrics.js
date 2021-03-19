// Psychrometric calculations


var inputForm = document.getElementById('inputForm');

function handleForm(event) { 
  event.preventDefault(); 
  calcPsychrometrics();
} 

inputForm.addEventListener('submit', handleForm);


function calcPsychrometrics() {

  // Define configuration variables
  const atmosphericPressure = 101325;  // Atmospheric pressure in Pa
  const storageTemp = 18;  // Desired storage temperature in Celsius

  // ------------------------------------------------------------
  // Get DOM Elements
  // ------------------------------------------------------------

  // Inputs
  const inputIntTemp = parseFloat(document.getElementById('inputIntTemp').value);
  const inputIntRelHum = parseFloat(document.getElementById('inputIntRelHum').value);
  const inputExtTemp = parseFloat(document.getElementById('inputExtTemp').value);
  const inputExtRelHum = parseFloat(document.getElementById('inputExtRelHum').value);
  const inputCoolingTemp = parseFloat(document.getElementById('inputCooling').value);
  const inputReheatingTemp = parseFloat(document.getElementById('inputReheating').value);

  // Outputs
  const outputIntAbsHum = document.getElementById('intAbsHum');
  const outputExtAbsHum = document.getElementById('extAbsHum');
  const outputRemovedWater = document.getElementById('removedWater');
  const outputTreatedAbsHum = document.getElementById('treatedAbsHum');
  const outputTreatedRelHum = document.getElementById('treatedRelHum');
  const outputTreatedVapPress = document.getElementById('treatedVapPress');
  const outputTreatedSpecVol = document.getElementById('treatedSpecVol');
  const outputTreatedSpecEnthal = document.getElementById('treatedSpecEnthal');
  const outputTreatedDewPoint = document.getElementById('treatedDewPoint');
  const outputTreatedWetBulbTemp = document.getElementById('treatedWetBulbTemp');

  // ------------------------------------------------------------
  // Calculations
  // ------------------------------------------------------------
  
  // Load psychrolib and set unit system
  let psychrolib = new Psychrometrics();
  psychrolib.SetUnitSystem(psychrolib.SI);

  // Interior Absolute Humidity
  let IntAbsHum = psychrolib.GetHumRatioFromRelHum(
    inputIntTemp, 
    inputIntRelHum/100, 
    atmosphericPressure
  ) * 1000;
  
  // Exterior Absolute Humidity
  let ExtAbsHum = psychrolib.GetHumRatioFromRelHum(
    inputExtTemp, 
    inputExtRelHum/100, 
    atmosphericPressure
  ) * 1000;
  
  // Relative Humidity after cooling
  let CoolRelHum = psychrolib.GetRelHumFromHumRatio(
    inputCoolingTemp, 
    ExtAbsHum/1000, 
    atmosphericPressure
  ) * 100;
  if (CoolRelHum > 100) {
    CoolRelHum = 100;
  }

  // Absolute Humidity after cooling
  let CoolAbsHum = psychrolib.GetHumRatioFromRelHum(
    inputCoolingTemp, 
    CoolRelHum/100, 
    atmosphericPressure
  ) * 1000;

  // Removed water
  let removedWater = ExtAbsHum - CoolAbsHum;

  // Treated Air Absolute Humidity (after reheating)
  let treatedAbsHum = CoolAbsHum;

  // Treated Air Relative Humidity (after reheating)
  let treatedRelHum = psychrolib.GetRelHumFromHumRatio(
    inputReheatingTemp, 
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
    inputReheatingTemp,
    treatedAbsHum/1000, 
    atmosphericPressure
  );

  // Treated air specific enthalpy (after reheating)
  let treatedSpecEnthal = psychrolib.GetMoistAirEnthalpy(
    inputReheatingTemp,
    treatedAbsHum/1000
  );

  // Treated air dew point (after reheating)
  let treatedDewPoint = psychrolib.GetTDewPointFromHumRatio(
    inputReheatingTemp,
    treatedAbsHum/1000, 
    atmosphericPressure
  );

  // Treated air wet bulb temperature (after reheating)
  let treatedWetBulbTemp = psychrolib.GetTWetBulbFromHumRatio(
    inputReheatingTemp,
    treatedAbsHum/1000, 
    atmosphericPressure
  );

  // ------------------------------------------------------------
  // Display results
  // ------------------------------------------------------------
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

}


