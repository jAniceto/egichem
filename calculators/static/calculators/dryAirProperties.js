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

  return (-4.3274 + 4.1190e-2*temperature + 1.5556e-4*temperature**2) * 1e-6;
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