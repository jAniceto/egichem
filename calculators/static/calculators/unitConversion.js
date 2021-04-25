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
    "kind": "time",
    "units": [
      {
        "id": "second",
        "str": "second (s)"
      },
      {
        "id": "minute",
        "str": "minute (min)"
      },
      {
        "id": "hour",
        "str": "hour (h)"
      },
      {
        "id": "day",
        "str": "day"
      },
      {
        "id": "week",
        "str": "week"
      },
      {
        "id": "year",
        "str": "year"
      },
    ]
  },
  {
    "kind": "length",
    "units": [
      {
        "id": "angstrom",
        "str": "Ångström (Å)"
      },
      {
        "id": "foot",
        "str": "foot (ft)"
      },
      {
        "id": "inch",
        "str": "inch (in)"
      },
      {
        "id": "yard",
        "str": "yard (yd)"
      },
      {
        "id": "mile",
        "str": "mile (mi)"
      },
      {
        "id": "nm",
        "str": "nanometer (nm)"
      },
      {
        "id": "um",
        "str": "micrometer (um)"
      },
      {
        "id": "cm",
        "str": "centimeter (cm)"
      },
      {
        "id": "dm",
        "str": "decimeter (dm)"
      },
      {
        "id": "m",
        "str": "meter (m)"
      },
      {
        "id": "km",
        "str": "kilometer (km)"
      },
    ]
  },
  {
    "kind": "area",
    "units": [
      {
        "id": "cm2",
        "str": "square centimeter (cm2)"
      },
      {
        "id": "m2",
        "str": "square meter (m2)"
      },
      {
        "id": "km2",
        "str": "square kilometer (km2)"
      },
      {
        "id": "acre",
        "str": "acre"
      },
      {
        "id": "hectare",
        "str": "hectare (ha)"
      },
    ]
  },
  {
    "kind": "volume",
    "units": [
      {
        "id": "gallon",
        "str": "gallon (gal)"
      },
      {
        "id": "ml",
        "str": "mililiter (ml)"
      },
      {
        "id": "l",
        "str": "liter (l)"
      },
      {
        "id": "cm3",
        "str": "cubic centimeter (cm3)"
      },
      {
        "id": "dm3",
        "str": "cubic decimeter (dm3)"
      },
      {
        "id": "m3",
        "str": "cubic meter (m3)"
      },
    ]
  },
  {
    "kind": "mass",
    "units": [
      {
        "id": "mg",
        "str": "miligram (mg)"
      },
      {
        "id": "gram",
        "str": "gram (g)"
      },
      {
        "id": "kg",
        "str": "kilogram"
      },
      {
        "id": "metric-ton",
        "str": "tonnne (t)"
      },
      {
        "id": "ounce",
        "str": "ounce (oz)"
      },
      {
        "id": "pound",
        "str": "pound (lb)"
      },
    ]
  },
  {
    "kind": "temperature",
    "units": [
      {
        "id": "tempC",
        "str": "Celsius (°C)"
      },
      {
        "id": "tempK",
        "str": "Kelvin (K)"
      },
      {
        "id": "tempF",
        "str": "Fahrenheit (°F)"
      },
      {
        "id": "tempR",
        "str": "Rankine (°R)"
      },
    ]
  },
  {
    "kind": "pressure",
    "units": [
      {
        "id": "atm",
        "str": "atmosphere (atm)"
      },
      {
        "id": "bar",
        "str": "bar"
      },
      {
        "id": "mmHg",
        "str": "millimetre of mercury (mmHg)"
      },
      {
        "id": "pascal",
        "str": "pascal (Pa)"
      },
      {
        "id": "kilopascal",
        "str": "kilopascal (kPa)"
      },
      {
        "id": "megapascal",
        "str": "megapascal (MPa)"
      },
      {
        "id": "psi",
        "str": "pounds per square inch (psi)"
      },
      {
        "id": "torr",
        "str": "torr"
      },
    ]
  }, 
  {
    "kind": "energy",
    "units": [
      {
        "id": "joule",
        "str": "joule (J)"
      },
      {
        "id": "kJ",
        "str": "kilojoule (kJ)"
      },
      {
        "id": "MJ",
        "str": "megajoule (MJ)"
      },
      {
        "id": "GJ",
        "str": "gigajoule (GJ)"
      },
      {
        "id": "calorie",
        "str": "calorie (cal)"
      },
      {
        "id": "kilocalorie",
        "str": "kilocalorie (kcal)"
      },
      {
        "id": "btu",
        "str": "british thermal unit (BTU)"
      },
      {
        "id": "erg",
        "str": "erg"
      },
    ]
  },
  {
    "kind": "speed",
    "units": [
      {
        "id": "m s-1",
        "str": "meter per second (m/s)"
      },
      {
        "id": "kph",
        "str": "kilometer per hour (km/h)"
      },
      {
        "id": "mph",
        "str": "miles per hour (mph)"
      },
    ]
  },
  {
    "kind": "volumetric_flow",
    "units": [
      {
        "id": "m3/s",
        "str": "cubic meter per second (m3/s)"
      },
      {
        "id": "m3/h",
        "str": "cubic meter per hour (m3/h)"
      },
      {
        "id": "m3/day",
        "str": "cubic meter per day (m3/day)"
      },
      {
        "id": "ml/s",
        "str": "mililiter per second (ml/s)"
      },
      {
        "id": "ml/min",
        "str": "mililiter per minute (ml/min)"
      },
      {
        "id": "l/h",
        "str": "liter per hour (h)"
      },
    ]
  },
  {
    "kind": "density",
    "units": [
      {
        "id": "g/ml",
        "str": "gram per mililiter (g/ml)"
      },
      {
        "id": "kg/l",
        "str": "kilogram per liter (kg/l)"
      },
      {
        "id": "g/cm3",
        "str": "gram per cubic centimeter (g/cm3)"
      },
      {
        "id": "kg/m3",
        "str": "gram per cubic centimeter (g/cm3)"
      },
      {
        "id": "kg/m3",
        "str": "gram per cubic centimeter (g/cm3)"
      },
    ]
  },
  {
    "kind": "viscosity",
    "units": [
      {
        "id": "mP",
        "str": "milipoise (mP)"
      },
      {
        "id": "cP",
        "str": "centipoise (mP)"
      },
      {
        "id": "P",
        "str": "poise (P)"
      },
      {
        "id": "mPa s",
        "str": "milipascal second (Pa s)"
      },
      {
        "id": "Pa s",
        "str": "pascal second (Pa s)"
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
    var kind = Qty.parse(fromUnitSelect.value).kind();
    filterSelectOptions('toUnitSelect', kind);
  }
});


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
    detailedConversionAlert.style.display = 'block';
    detailedConversionAlert.innerHTML = error;
  }

}