// utilities.js

// UTILITIES
// A collection of Javascript functions to perform several math operations

// Requires:
// math.js

// Code by:
// José Aniceto
// EgiChem Group
// CICECO - Aveiro Institute of Materials
// University of Aveiro
// Portugal



/* -------------------------------------------------------------------------- */
/*                              Error functions                               */
/* -------------------------------------------------------------------------- */
function calcErrorFunctions() {
  let x = document.getElementById('errorX').value;
  let erf = math.erf(x);
  let erfc = 1 - erf;

  document.getElementById('erf').value = erf.toFixed(8);
  document.getElementById('erfc').value = erfc.toFixed(8);
}


/* -------------------------------------------------------------------------- */
/*                          Trigonometric functions                           */
/* -------------------------------------------------------------------------- */
function calcTrigonometricFunctions() {
  // Inputs
  let isRad = document.getElementById('radioRad').checked;
  let x = document.getElementById('trigTheta').value;

  // Safety check to avoid running large JS
  if (x.length > 15) {
    return;
  }

  // Convert to radians
  let xRad;
  if (document.getElementById('radioRad').checked) {
    xRad = math.evaluate(x);
  } else if (document.getElementById('radioDeg').checked) {
    xRad = math.evaluate(x) * (math.PI/180);
  }

  // Calculations
  let sin = math.sin(xRad);
  let cos = math.cos(xRad);
  let tan = math.tan(xRad);
  let cotan = math.cot(xRad);
  let sec = math.sec(xRad);
  let cosec = math.csc(xRad);
  
  // Trigonometric functions results
  let sinValue = document.getElementById('sin')
  if (sin < 1e-10 && sin > -1e-10) {
    sinValue.value = 0;
  } else {
    sinValue.value = sin.toFixed(8);
  }

  let cosValue = document.getElementById('cos')
  if (cos < 1e-10 && cos > -1e-10) {
    cosValue.value = 0;
  } else {
    cosValue.value = cos.toFixed(8);
  }

  let tanValue = document.getElementById('tan')
  if (tan < 1e-10 && tan > -1e-10) {
    tanValue.value = 0;
  } else if (tan > 1e10 || tan < -1e10) {
    tanValue.value = 'undefined';
  } else if (tan > 0.99999 && tan < 1.00001) {
    tanValue.value = 1;
  } else if (tan < -0.99999 && tan > -1.00001) {
    tanValue.value = -1;
  } else {
    tanValue.value = tan.toFixed(8);
  }

  let cotanValue = document.getElementById('cotan')
  if (cotan < 1e-10  && cotan > -1e-10) {
    cotanValue.value = 0;
  } else if (cotan > 1e10 || cotan < -1e10) {
    cotanValue.value = 'undefined';
  } else if (cotan > 0.99999 && cotan < 1.00001) {
    cotanValue.value = 1;
  } else if (cotan < -0.99999 && cotan > -1.00001) {
    cotanValue.value = -1;
  } else {
    cotanValue.value = cotan.toFixed(8);
  }

  let secValue = document.getElementById('sec')
  if (sec < 1e-10 && sec > -1e-10) {
    secValue.value = 0;
  } else if (sec > 1e10 || sec < -1e10) {
    secValue.value = 'undefined';
  } else {
    secValue.value = sec.toFixed(8);
  }

  let cosecValue = document.getElementById('cosec')
  if (cosec < 1e-10  && cosec > -1e-10) {
    cosecValue.value = 0;
  } else if (cosec > 1e10 || cosec < -1e10) {
    cosecValue.value = 'undefined';
  } else {
    cosecValue.value = cosec.toFixed(8);
  }
}

// Listener for trigForm submit
document.getElementById('trigForm').addEventListener('submit', function (event) {
  event.preventDefault(); 
  calcTrigonometricFunctions();
})


/* -------------------------------------------------------------------------- */
/*                           Hyperbolic functions                             */
/* -------------------------------------------------------------------------- */
function calcHyperbolicFunctions() {
  // Inputs
  let x = parseFloat(document.getElementById('hyperbX').value);

  // Calculations
  let sinh = math.sinh(x);
  let cosh = math.cosh(x);
  let tanh = math.tanh(x);
  let cotanh = math.coth(x);
  let sech = math.sech(x);
  let cosech = math.csch(x);
  
  // Hyperbolic functions results
  let sinhValue = document.getElementById('sinh')
  sinhValue.value = sinh.toFixed(8);

  let coshValue = document.getElementById('cosh')
  coshValue.value = cosh.toFixed(8);
  
  let tanhValue = document.getElementById('tanh')
  tanhValue.value = tanh.toFixed(8);

  let cotanhValue = document.getElementById('cotanh')
  cotanhValue.value = cotanh.toFixed(8);

  let sechValue = document.getElementById('sech')
  if (sech < 1e-10 && sech > -1e-10) {
    sechValue.value = 0;
  // } else if (sech > 1e10 || sech < -1e10) {
  //   sechValue.value = 'undefined';
  } else {
    sechValue.value = sech.toFixed(8);
  }

  let cosechValue = document.getElementById('cosech')
  if (cosech < 1e-10  && cosech > -1e-10) {
    cosechValue.value = 0;
  // } else if (cosech > 1e10 || cosech < -1e10) {
  //   cosechValue.value = 'undefined';
  } else {
    cosechValue.value = cosech.toFixed(8);
  }
}

// Listener for hyperbForm submit
document.getElementById('hyperbForm').addEventListener('submit', function (event) {
  event.preventDefault(); 
  calcHyperbolicFunctions();
})


/* -------------------------------------------------------------------------- */
/*                             Bessel functions                               */
/* -------------------------------------------------------------------------- */
function calcBesselFunctions() {
  // Inputs
  let x = parseFloat(document.getElementById('besselX').value);
  let n = parseFloat(document.getElementById('besselOrder').value);

  // Calculations
  let Jn = BESSEL.besselj(x, n);
  let Yn = BESSEL.bessely(x, n);
  let In = BESSEL.besseli(x, n);
  let Kn = BESSEL.besselk(x, n);

  // Results
  document.getElementById('bessel1Kind').value = Jn;
  document.getElementById('bessel2Kind').value = Yn;
  document.getElementById('modifiedBessel1Kind').value = In;
  document.getElementById('modifiedBessel2Kind').value = Kn;
}

// Listener for besselForm submit
document.getElementById('besselForm').addEventListener('submit', function (event) {
  event.preventDefault(); 
  calcBesselFunctions();
})