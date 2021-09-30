// d12GasLowPressure.js

// DIFFUSIVITIES GAS LOW PRESSURE
// Javascript functions to calculated the diffusion coefficients of binary gas systems at low pressure
// Chapman and Enskog

// Code by:
// José Aniceto
// EgiChem Group
// CICECO - Aveiro Institute of Materials
// University of Aveiro
// Portugal


function D12GasWilkeLee(temperature, pressure, molarMass1, molarMass2, molarVolumeBoil1, molarVolumeBoil2, normalTempBoil1, normalTempBoil2) {
    // Calculate diffusion coefficient using Wilke-Lee equation
    // Ref: B.E. Poling, J.M. Prausnitz, J.P. O'Connell. Properties of Gases and Liquids, 5th Edition, McGraw-Hill, 2001.
  
    // Parameters:
    //     temperature : float : Temperature in kelvin (K)
    //     pressure : float : Pressure in bar (bar)
    //     molarMass1 : float : molar mass of component 1 (g/mol)
    //     molarMass2 : float : molar mass of component 2 (g/mol)
    //     molarVolumeBoil1 : float : Liquid molar volume at the normal boiling temperature for component 1 (cm3/mol)
    //     molarVolumeBoil2 : float : Liquid molar volume at the normal boiling temperature for component 2 (cm3/mol)
    //     normalTempBoil1 : float : Normal boiling point (at 1 atm) for component 1 (K)
    //     normalTempBoil2 : float : Normal boiling point (at 1 atm) for component 2 (K)
    // Returns:
    //     float : Binary diffusion coefficient in (cm2/s)
    const A = 1.06036;
    const B = 0.15610;
    const C = 0.19300;
    const D = 0.47635;
    const E = 1.03587;
    const F = 1.52996;
    const G = 1.76474;
    const H = 3.89411;

    let molarMass12 = 2 / ((1 / molarMass1) + (1 / molarMass2));
    let sigma1 = 1.18 * molarVolumeBoil1**(1/3);
    let sigma2 = 1.18 * molarVolumeBoil2**(1/3);
    let epsilon1k = 1.15 * normalTempBoil1;
    let epsilon2k = 1.15 * normalTempBoil2;
    let sigma12 = (sigma1 + sigma2)/2;
    let epsilon12k = (epsilon1k * epsilon2k)**0.5;
    let tempStar = temperature/epsilon12k;
    let omegaD = A/tempStar**B + C/Math.exp(D*tempStar) + E/Math.exp(F*tempStar) + G/Math.exp(H*tempStar);
    return ((3.03 - (0.98 / molarMass12**0.5)) * 1e-3 * temperature**1.5) / (pressure * molarMass12**0.5 * sigma12**2 * omegaD);
}
    

  // Get DOM elements
  var WilkeLeeForm = document.getElementById('WilkeLeeForm');
  var WilkeLeeAlert = document.getElementById('WilkeLeeAlert');
  var temperature = document.getElementById('temperature');
  var pressure = document.getElementById('pressure');
  var molarMass1 = document.getElementById('molarMass1');
  var molarMass2 = document.getElementById('molarMass2');
  var molarVolumeBoil1 = document.getElementById('molarVolumeBoil1');
  var molarVolumeBoil2 = document.getElementById('molarVolumeBoil2');
  var normalTempBoil1 = document.getElementById('normalTempBoil1');
  var normalTempBoil2 = document.getElementById('normalTempBoil2');
  var diffusionCoeffWilkeLee = document.getElementById('diffusionCoeffWilkeLee');
  
  
  // Listener for Form submit
  WilkeLeeForm.addEventListener('submit', function (event) {
    event.preventDefault(); 
    calculateD12WilkeLee();
  })
  
  
  // Validity Warning
  function validityWarning() {
    WilkeLeeAlert.style.display = 'block';
    WilkeLeeAlert.innerHTML = 'Warning: ';
  }
  
  
  // Calculate Properties and display results
  function calculateD12WilkeLee() {
  
    // Clear old warnings
    WilkeLeeAlert.style.display = 'none';

    let temp = parseFloat(temperature.value);
    let press = parseFloat(pressure.value);
    let Mw1 = parseFloat(molarMass1.value);
    let Mw2 = parseFloat(molarMass2.value);
    let Vm1 = parseFloat(molarVolumeBoil1.value);
    let Vm2 = parseFloat(molarVolumeBoil2.value);
    let Tbp1 = parseFloat(normalTempBoil1.value);
    let Tbp2 = parseFloat(normalTempBoil2.value);
    
    let D12WilkeLee = D12GasWilkeLee(temp, press, Mw1, Mw2, Vm1, Vm2, Tbp1, Tbp2);
  
    // Display results
    diffusionCoeffWilkeLee.value = D12WilkeLee.toPrecision(5);
  }


// TESTS
// Example 11-3 - B.E. Poling, J.M. Prausnitz, J.P. O'Connell. Properties of Gases and Liquids, 5th Edition, McGraw-Hill, 2001.
console.log(D12GasWilkeLee(298, 1, 76.5, 29.0, 84.7, 125000/205379*3.62**3, 318.3, 97.0/1.15))  // Solution: 0.10 cm2/s