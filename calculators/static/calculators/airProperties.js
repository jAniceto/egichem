// dryAirProperties.js

// DRY AIR PROPERTIES
// Javascript functions to calculated several properties of dry air at atmospheric pressure
// Valid for the following temperature range: 200 - 400 K

// Code by:
// José Aniceto
// EgiChem Group
// CICECO - Aveiro Institute of Materials
// University of Aveiro
// Portugal


function dryAirDensity(temperature) {
  // Calculate dry air density at atmospheric pressure
  // Ref: Marquardt (1963)

  // Parameters:
  //     temperature : float : Temperature in kelvin (K)
  // Returns:
  //     float : Density in kg/m3

  return 351.99/temperature + 344.84/temperature**2;
}


function dryAirViscosity(temperature) {
  // Calculate dry air (dynamic) viscosity at atmospheric pressure
  // Ref: Sutherland's equation, Reid (1966)

  // Parameters:
  //     temperature : float : Temperature in kelvin (K)
  // Returns:
  //     float : Viscosity in N.s/m2 (Pa s)

  return 1.4592*temperature**1.5 / (109.10 + temperature) * 1e-6;
}


function dryAirKinematicViscosity(temperature) {
  // Calculate dry air kinematic viscosity at atmospheric pressure

  // Parameters:
  //     temperature : float : Temperature in kelvin (K)
  // Returns:
  //     float : Kinematic viscosity in m2/s

  return dryAirViscosity(temperature)/dryAirDensity(temperature);
}


function dryAirThermalConductivity(temperature) {
  // Calculate dry air thermal conductivity at atmospheric pressure
  // Ref: Sutherland's equation, Reid (1966)

  // Parameters:
  //     temperature : float : Temperature in kelvin (K)
  // Returns:
  //     float : Thermal conductivity in W/(m K)

  return 2.3340e-3*temperature**1.5 / (164.54 + temperature);
}


function dryAirSpecificHeat(temperature) {
  // Calculate dry air specific heat at atmospheric pressure

  // Parameters:
  //     temperature : float : Temperature in kelvin (K)
  // Returns:
  //     float : Specific heat in J/(kg K)

  return 1030.5 - 0.19975*temperature + 3.9734e-4*temperature**2;
}


function dryAirThermalDiffusivity(temperature) {
  // Calculate dry air thermal diffusivity at atmospheric pressure

  // Parameters:
  //     temperature : float : Temperature in kelvin (K)
  // Returns:
  //     float : Thermal diffusivity in m2/s

  // return (-4.3274 + 4.1190e-2*temperature + 1.5556e-4*temperature**2) * 1e-6;
  return dryAirThermalConductivity(temperature) / dryAirDensity(temperature) / dryAirSpecificHeat(temperature)
}


function dryAirPrandtlNumber(temperature) {
  // Calculate dry air Prandtl number at atmospheric pressure

  // Parameters:
  //     temperature : float : Temperature in kelvin (K)
  // Returns:
  //     float : Prandtl number (dimensionless)

  let specHeat = dryAirSpecificHeat(temperature);
  let visc = dryAirViscosity(temperature);
  let thermCond = dryAirThermalConductivity(temperature);
  return specHeat*visc/thermCond;
}


function dryAirThermalExpansionCoefficient(temperature) {
  // Calculate dry air thermal expansion coefficient at atmospheric pressure

  // Parameters:
  //     temperature : float : Temperature in kelvin (K)
  // Returns:
  //     float : Thermal expansion coefficient (1/K)

  return 1/temperature;
}


// Get DOM elements
var airPropertiesForm = document.getElementById('airPropertiesForm');
var airPropertiesAlert = document.getElementById('airPropertiesAlert');
var temperature = document.getElementById('temperature');
var density = document.getElementById('density');
var viscosity = document.getElementById('viscosity');
var kinematicViscosity = document.getElementById('kinematicViscosity');
var thermalConductivity = document.getElementById('thermalConductivity');
var specificHeat = document.getElementById('specificHeat');
var thermalDiffusivity = document.getElementById('thermalDiffusivity');
var prandtlNumber = document.getElementById('prandtlNumber');


// Listener for Form submit
airPropertiesForm.addEventListener('submit', function (event) {
  event.preventDefault(); 
  calculateAirProperties();
})


// Validity Warning
function validityWarning() {
  airPropertiesAlert.style.display = 'block';
  airPropertiesAlert.innerHTML = 'Warning: Temperature is outside correlation range of 200 - 400 K.';
}


// Calculate Properties and display results
function calculateAirProperties() {

  // Clear old warnings
  airPropertiesAlert.style.display = 'none';
  
  // Check input
  let temp = parseFloat(temperature.value) + 273.15;
  if ((temp < 200) || (temp > 400)) {
    validityWarning();
  }
  
  let dens = dryAirDensity(temp);
  let visc = dryAirViscosity(temp);
  let kinVisc = dryAirKinematicViscosity(temp);
  let conduct = dryAirThermalConductivity(temp);
  let specHeat = dryAirSpecificHeat(temp);
  let diffusiv = dryAirThermalDiffusivity(temp);
  let Pr = dryAirPrandtlNumber(temp);

  // Display results
  density.value = dens.toPrecision(5);
  viscosity.value = visc.toExponential(5);
  kinematicViscosity.value = kinVisc.toExponential(5);
  thermalConductivity.value = conduct.toPrecision(5);
  specificHeat.value = specHeat.toPrecision(5);
  thermalDiffusivity.value = diffusiv.toExponential(5);
  prandtlNumber.value = Pr.toPrecision(5);

}