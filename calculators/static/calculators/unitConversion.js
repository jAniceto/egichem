// unitConversion.js

// UNIT CONVERSIONS
// Javascript functions to perform unit conversions

// Requires:
// quatities.js - https://github.com/gentooboontoo/js-quantities

// Code by:
// José Aniceto
// EgiChem Group
// CICECO - Aveiro Institute of Materials
// University of Aveiro
// Portugal


// Quick Conversion
// ----------------

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

// Listener for Quick Form submit
quickConversionForm.addEventListener('submit', function (event) {
  event.preventDefault(); 
  quickConvert();
})

// Quick convert calculation
function quickConvert() {
  // Remove alert is exists
  clearAlert(quickConversionAlert);

  let fromVal = quickFrom.value;
  let toVal = quickTo.value;

  // Help parsing temperature units
  if (fromVal.endsWith('C')) {
    fromVal = fromVal.replace('C', 'tempC');
  }

  if (fromVal.endsWith('F')) {
    fromVal = fromVal.replace('F', 'tempF');
  }

  if (fromVal.endsWith('K')) {
    fromVal = fromVal.replace('K', 'tempK');
  }

  if (fromVal.endsWith('R')) {
    fromVal = fromVal.replace('R', 'tempR');
  }

  if (toVal.endsWith('C')) {
    toVal = toVal.replace('C', 'tempC');
  }

  if (toVal.endsWith('F')) {
    toVal = toVal.replace('F', 'tempF');
  }

  if (toVal.endsWith('K')) {
    toVal = toVal.replace('K', 'tempK');
  }

  if (toVal.endsWith('R')) {
    toVal = toVal.replace('R', 'tempR');
  }

  try {
    fromQty = Qty.parse(fromVal);
    toQty = Qty.parse(toVal);
    
    if (fromQty && toQty) {
      result = fromQty.to(toQty);
    
    } else if (!fromQty && toQty) {
      throw new Error("Can not parse the inputted value for FROM.");
    
    }  else if (fromQty && !toQty) {
      throw new Error("Can not parse the inputted value for TO.");
    
    } else {
      throw new Error("Can't parse the inputted values for FROM and TO.");
    }
    
    quickResult.value = result.scalar.toPrecision(6);

  } catch (error) {
    quickConversionAlert.style.display = 'block';
    quickConversionAlert.innerHTML = error;
  }

}


// Detailed Conversion
// -------------------
var unitsByKind = [
  {
    "kind": "area",
    "units": [
      {
        "id": "cm2",
        "str": "square centimeter (cm2)",
        "factor": 1e-4
      },
      {
        "id": "m2",
        "str": "square meter (m2)",
        "factor": 1
      },
      {
        "id": "km2",
        "str": "square kilometer (km2)",
        "factor": 1000000
      },
      {
        "id": "acre",
        "str": "acre",
        "factor": 4046.85642
      },
      {
        "id": "hectare",
        "str": "hectare (ha)",
        "factor": 10000
      },
    ]
  },
  {
    "kind": "concentration",
    "units": [
      {
        "id": "mmol/ml",
        "str": "milimol per mililiter (mmol/ml)",
        "factor": 1000
      },
      {
        "id": "mol/l",
        "str": "mol per liter (mol/l)",
        "factor": 1000
      },
      {
        "id": "mol/cm3",
        "str": "mol per cubic centimeter (mol/cm3)",
        "factor": 1e6
      },
      {
        "id": "mol/dm3",
        "str": "mol per cubic decimeter (mol/dm3)",
        "factor": 1000
      },
      {
        "id": "mol/m3",
        "str": "mol per cubic meter (mol/m3)",
        "factor": 1
      }
    ]
  },
  {
    "kind": "density",
    "units": [
      {
        "id": "g/ml",
        "str": "gram per mililiter (g/ml)",
        "factor": 1000
      },
      {
        "id": "g/l",
        "str": "gram per liter (g/l)",
        "factor": 1
      },
      {
        "id": "kg/l",
        "str": "kilogram per liter (kg/l)",
        "factor": 1000
      },
      {
        "id": "g/cm3",
        "str": "gram per cubic centimeter (g/cm3)",
        "factor": 1000
      },
      {
        "id": "kg/dm3",
        "str": "kilogram per cubic decimeter (kg/dm3)",
        "factor": 1000
      },
      {
        "id": "kg/m3",
        "str": "kilogram per cubic meter (kg/m3)",
        "factor": 1
      },
    ]
  },
  {
    "kind": "diffusivity",
    "units": [
      {
        "id": "cm2/s",
        "str": "centimeter square per second (cm2/s)",
        "factor": 1e-4
      },
      {
        "id": "m2/s",
        "str": "meter square per second (m2/s)",
        "factor": 1
      },
      {
        "id": "cm2/min",
        "str": "centimeter square per minute (cm2/min)",
        "factor": 1/600000
      },
      {
        "id": "m2/min",
        "str": "meter square per minute (m2/min)",
        "factor": 1/60
      },
    ]
  },
  {
    "kind": "energy",
    "units": [
      {
        "id": "joule",
        "str": "joule (J)",
        "factor": 1
      },
      {
        "id": "kJ",
        "str": "kilojoule (kJ)",
        "factor": 1000
      },
      {
        "id": "MJ",
        "str": "megajoule (MJ)",
        "factor": 1e6
      },
      {
        "id": "GJ",
        "str": "gigajoule (GJ)",
        "factor": 1e9
      },
      {
        "id": "calorie",
        "str": "calorie (cal)",
        "factor": 4.184
      },
      {
        "id": "kilocalorie",
        "str": "kilocalorie (kcal)",
        "factor": 4184
      },
      {
        "id": "btu",
        "str": "british thermal unit (BTU)",
        "factor": 1055.05585
      },
      {
        "id": "erg",
        "str": "erg",
        "factor": 1e-7
      },
    ]
  },
  {
    "kind": "specific heat capacity",
    "units": [
      {
        "id": "J/(kg K)",
        "str": "joule per kilogram-Kelvin (J/(kg K))",
        "factor": 1
      },
      {
        "id": "J/(g °C)",
        "str": "joule per gram-Celsius (J/(g °C))",
        "factor": 1000
      },
      {
        "id": "cal/(g °C)",
        "str": "calorie per gram-Celsius (cal/(g °C))",
        "factor": 4186.8
      },
      {
        "id": "BTU/(lb °F)",
        "str": "BTU per pound-Fahrenheit (BTU/(lb °F))",
        "factor": 4186.8
      },
    ]
  },
  {
    "kind": "length",
    "units": [
      {
        "id": "angstrom",
        "str": "Ångström (Å)",
        "factor": 1e-10
      },
      {
        "id": "foot",
        "str": "foot (ft)",
        "factor": 0.3048
      },
      {
        "id": "inch",
        "str": "inch (in)",
        "factor": 0.0254
      },
      {
        "id": "yard",
        "str": "yard (yd)",
        "factor": 0.9144
      },
      {
        "id": "mile",
        "str": "mile (mi)",
        "factor": 1609.344
      },
      {
        "id": "nm",
        "str": "nanometer (nm)",
        "factor": 1e-9
      },
      {
        "id": "um",
        "str": "micrometer (um)",
        "factor": 1e-6
      },
      {
        "id": "mm",
        "str": "milimeter (mm)",
        "factor": 0.001
      },
      {
        "id": "cm",
        "str": "centimeter (cm)",
        "factor": 0.01
      },
      {
        "id": "dm",
        "str": "decimeter (dm)",
        "factor": 0.1
      },
      {
        "id": "m",
        "str": "meter (m)",
        "factor": 1
      },
      {
        "id": "km",
        "str": "kilometer (km)",
        "factor": 1000
      },
    ]
  },
  {
    "kind": "mass",
    "units": [
      {
        "id": "mg",
        "str": "miligram (mg)",
        "factor": 1e-6
      },
      {
        "id": "gram",
        "str": "gram (g)",
        "factor": 0.001
      },
      {
        "id": "kg",
        "str": "kilogram (kg)",
        "factor": 1
      },
      {
        "id": "metric-ton",
        "str": "tonnne (t)",
        "factor": 1000
      },
      {
        "id": "ounce",
        "str": "ounce (oz)",
        "factor": 0.0283495231
      },
      {
        "id": "pound",
        "str": "pound (lb)",
        "factor": 0.45359237
      },
    ]
  },
  {
    "kind": "permeability",
    "units": [
      {
        "id": "mol m/(m2 s Pa)",
        "str": "mol m/(m2 s Pa)",
        "factor": 1
      },
      {
        "id": "barrer",
        "str": "barrer",
        "factor": 3.35e-16
      },
      {
        "id": "cm3STP cm/(cm2 s cmHg)",
        "str": "cm3STP cm/(cm2 s cmHg)",
        "factor": 3.35e-6
      },
    ]
  }, 
  {
    "kind": "permeance",
    "units": [
      {
        "id": "mol/(m2 s Pa)",
        "str": "mol/(m2 s Pa)",
        "factor": 1
      },
      {
        "id": "cm3STP/(cm2 s cmHg)",
        "str": "cm3STP/(cm2 s cmHg)",
        "factor": 3.35e-4
      },
      {
        "id": "m3STP/(m2 s Pa)",
        "str": "m3STP/(m2 s Pa)",
        "factor": 44.6607119051
      },
      {
        "id": "GPU",
        "str": "gas permeance unit (GPU)",
        "factor": 3.35e-10
      },
    ]
  }, 
  {
    "kind": "pressure",
    "units": [
      {
        "id": "atm",
        "str": "atmosphere (atm)",
        "factor": 101325
      },
      {
        "id": "bar",
        "str": "bar",
        "factor": 100000
      },
      {
        "id": "mmHg",
        "str": "millimetre of mercury (mmHg)",
        "factor": 133.322368
      },
      {
        "id": "pascal",
        "str": "pascal (Pa)",
        "factor": 1
      },
      {
        "id": "kilopascal",
        "str": "kilopascal (kPa)",
        "factor": 1000
      },
      {
        "id": "megapascal",
        "str": "megapascal (MPa)",
        "factor": 1e6
      },
      {
        "id": "psi",
        "str": "pounds per square inch (psi)",
        "factor": 6894.75729
      },
      {
        "id": "torr",
        "str": "torr",
        "factor": 133.322368
      },
    ]
  }, 
  {
    "kind": "speed",
    "units": [
      {
        "id": "m s-1",
        "str": "meter per second (m/s)",
        "factor": 1
      },
      {
        "id": "kph",
        "str": "kilometer per hour (km/h)",
        "factor": 0.277777778
      },
      {
        "id": "mph",
        "str": "miles per hour (mph)",
        "factor": 0.44704
      },
    ]
  },
  {
    "kind": "temperature",
    "units": [
      {
        "id": "tempC",
        "str": "Celsius (°C)",
      },
      {
        "id": "tempK",
        "str": "Kelvin (K)",
      },
      {
        "id": "tempF",
        "str": "Fahrenheit (°F)",
      },
      {
        "id": "tempR",
        "str": "Rankine (°R)",
      },
    ]
  },
  {
    "kind": "thermal conductivity",
    "units": [
      {
        "id": "W/(cm K)",
        "str": "watts per centimeter-Kelvin (W/(cm K))",
        "factor": 100
      },
      {
        "id": "W/(m K)",
        "str": "watts per meter-Kelvin (W/(m K))",
        "factor": 1
      },
      {
        "id": "BTU/(h ft F)",
        "str": "BTU per hour-foot-Fahrenheit (BTU/(h ft °F))",
        "factor": 1.7295772056
      },
    ]
  },
  {
    "kind": "time",
    "units": [
      {
        "id": "second",
        "str": "second (s)",
        "factor": 1
      },
      {
        "id": "minute",
        "str": "minute (min)",
        "factor": 60
      },
      {
        "id": "hour",
        "str": "hour (h)",
        "factor": 3600
      },
      {
        "id": "day",
        "str": "day",
        "factor": 86400
      },
      {
        "id": "week",
        "str": "week",
        "factor": 604800
      },
      {
        "id": "year",
        "str": "year",
        "factor": 31556926
      },
    ]
  },
  {
    "kind": "viscosity",
    "units": [
      {
        "id": "mP",
        "str": "milipoise (mP)",
        "factor": 0.0001
      },
      {
        "id": "cP",
        "str": "centipoise (mP)",
        "factor": 0.001
      },
      {
        "id": "P",
        "str": "poise (P)",
        "factor": 0.1
      },
      {
        "id": "mPa s",
        "str": "milipascal second (mPa s)",
        "factor": 0.001
      },
      {
        "id": "Pa s",
        "str": "pascal second (Pa s)",
        "factor": 1
      },
    ]
  },
  {
    "kind": "volume",
    "units": [
      {
        "id": "gallon",
        "str": "gallon (gal)",
        "factor": 0.003785411784
      },
      {
        "id": "ml",
        "str": "mililiter (ml)",
        "factor": 1e-6
      },
      {
        "id": "l",
        "str": "liter (l)",
        "factor": 1e-3
      },
      {
        "id": "cm3",
        "str": "cubic centimeter (cm3)",
        "factor": 1e-6
      },
      {
        "id": "dm3",
        "str": "cubic decimeter (dm3)",
        "factor": 1e-3
      },
      {
        "id": "m3",
        "str": "cubic meter (m3)",
        "factor": 1
      },
    ]
  },
  {
    "kind": "volumetric_flow",
    "units": [
      {
        "id": "m3/s",
        "str": "cubic meter per second (m3/s)",
        "factor": 1
      },
      {
        "id": "m3/h",
        "str": "cubic meter per hour (m3/h)",
        "factor": 3600
      },
      {
        "id": "m3/day",
        "str": "cubic meter per day (m3/day)",
        "factor": 1.15740741e-5
      },
      {
        "id": "ml/s",
        "str": "mililiter per second (ml/s)",
        "factor": 1e-6
      },
      {
        "id": "ml/min",
        "str": "mililiter per minute (ml/min)",
        "factor": 1.66666667e-8
      },
      {
        "id": "l/h",
        "str": "liter per hour (l/h)",
        "factor": 2.7777777777778e-7
      },
      {
        "id": "gal/s",
        "str": "gallon per second (gal/s)",
        "factor": 0.00378541178
      },
    ]
  },
];

var detailedFrom = document.getElementById('detailedFrom');
var fromUnitSelect = document.getElementById('fromUnitSelect');
var toUnitSelect = document.getElementById('toUnitSelect');
var detailedResult = document.getElementById('detailedResult');


// Function to capitalize word
function capitalize(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

// Function to get precision of number
function precision(a) {
  if (!isFinite(a)) return 0;
  var e = 1, p = 0;
  while (Math.round(a * e) / e !== a) { e *= 10; p++; }
  return p;
}


// On page load run
window.onload = function() {
  createSelectOptions('fromUnitSelect');
  createSelectOptions('toUnitSelect');
};

// Listener for selects
fromUnitSelect.addEventListener('change', function() {
  if (fromUnitSelect.value == 'none') {
    createSelectOptions('fromUnitSelect');
    createSelectOptions('toUnitSelect');
  } else {
    var kind = getKindById(fromUnitSelect.value);
    filterSelectOptions('toUnitSelect', kind);
  }
});


// Function to get kind of quantity from a id
function getKindById(idValue) {
  let quantitySelected = unitsByKind.find(quantity => {
    return quantity.units.some(unit => {
      return unit.id === idValue;
    });
  })
  return quantitySelected.kind;
}


// Function to populate the options of the unit select widget
function createSelectOptions(selectId) {
  var options = ['<option value="none" selected>Choose unit</option>'];
  unitsByKind.map(unitKind => {
    options.push(`<optgroup label="${capitalize(unitKind['kind'].replace('_', ' '))}">`);
    unitKind['units'].map(unit => options.push(`<option value="${unit['id']}">${unit['str']}</option>`));
  });
  
  document.getElementById(selectId).innerHTML = options.join("");
}


// Function to filter the options of the unit select widget
function filterSelectOptions(selectId, kind) {
  var options = ['<option value="none" selected>Choose unit</option>'];
  unitsByKind.map(unitKind => {
    if (kind == unitKind['kind']) {
      options.push(`<optgroup label="${capitalize(unitKind['kind'].replace('_', ' '))}">`);
      unitKind['units'].map(unit => options.push(`<option value="${unit['id']}">${unit['str']}</option>`));
    }
  });
  document.getElementById(selectId).innerHTML = options.join("");
}


// Listener for Detailed Form submit
detailedConversionForm.addEventListener('submit', function (event) {
  event.preventDefault(); 
  detailedConvert();
})


// Detailed convert calculation
function detailedConvert() {
  // Remove alert is exists
  clearAlert(detailedConversionAlert);

  try {
    fromQty = Qty.parse(detailedFrom.value + ' ' + fromUnitSelect.value);
    toQty = Qty.parse(toUnitSelect.value);

    result = fromQty.to(toQty);
    
    detailedResult.value = +result.scalar.toPrecision(6);

  } catch (error) {
    try {
      
      let resultManual = manualConversion(detailedFrom.value, fromUnitSelect.value, toUnitSelect.value)

      detailedResult.value = resultManual.toPrecision(6);

    } catch (error2) {
      detailedConversionAlert.style.display = 'block';
      detailedConversionAlert.innerHTML = error;
    }
  }

}


// Function to get unit object
function getUnitObjectById(idValue) {
  let quantitySelected = unitsByKind.find(quantity => {
    return quantity.units.some(unit => {
      return unit.id === idValue;
    });
  })
  return quantitySelected.units.find(unit => {
      return unit.id === idValue;
    });
}


// Function to perform conversion manually (without using quantities.js)
function manualConversion(value, fromUnit, toUnit) {
  let fromUnitObject = getUnitObjectById(fromUnit);
  let toUnitObject = getUnitObjectById(toUnit);

  let result = value * fromUnitObject.factor / toUnitObject.factor;
	
  return result;
}