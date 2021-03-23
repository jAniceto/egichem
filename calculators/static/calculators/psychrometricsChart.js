// ---------------------------------------------- //
// PSYCHROMETRIC CHART
// ---------------------------------------------- //

// Function to create a range array
function range(start, stop, step) {
  if (typeof stop == 'undefined') {
      // one param defined
      stop = start;
      start = 0;
  }

  if (typeof step == 'undefined') {
      step = 1;
  }

  if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
      return [];
  }

  var result = [];
  for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
      result.push(i);
  }

  return result;
};


// Load psychrolib and set unit system
// let psychrolib = new Psychrometrics();
// psychrolib.SetUnitSystem(psychrolib.SI);


// Get DOM Elements
// let psychrometricsForm = document.getElementById('psychrometricsForm');
// let refPressInput = document.getElementById('refPress');


// Global layout configuration for Plotly 
var layout = {
  margin: {
    l: 50,
    // r: 50,
    // b: 100,
    t: 10,
    // pad: 4
  },
  hovermode:'closest',
  xaxis: {
    'title': 'Dry Bulb Temperature (°C)',
    'range': [0, 40],
    'zeroline': false,
  },
  yaxis: {
    'title': 'Absolute Humidity (g water / kg air)',
    'range': [0, 35],
    'side': 'right',
  },
  shapes: [{
    'type': 'line', 'x0': 40, 'x1': 40, 'xref': 'x', 'y0': 0, 'y1': 70, 'yref': 'y', 'line': {'width': 1}
  }],
  showlegend: true,
	legend: {
    y: 0.5,
    x: 1.1,
    title: {text: 'Click to hide/show lines.<br>Double-click to isolate.<br>'}
  }
};


var config = {
  modeBarButtonsToRemove: ['autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian', 'zoom2d']
};


// Create fixed variable ranges
let dryBulbTempRange = range(-10, 55.5, 0.5);
let relHumRange = range(10, 110, 10);
let enthalRange = range(0, 150, 20);
let wetBulbTempRange = range(-5, 35, 5);


// Update Psychrometric Chart
function createPsychrometricChart(pressure) {

  // Calculate Relative Humidity lines
  //----------------------------------
  let relHumLines = new Array(10);
  // For each RH in the RH range [10, 100]
  relHumRange.forEach(function (relHum, i) {
    // Calculate range of Absolute Humidity
    relHumLines[i] = dryBulbTempRange.map(function(temp) { 
      return psychrolib.GetHumRatioFromRelHum(temp, relHum/100, pressure) * 1000; 
    })
  });

  // Calculate Enthalpy Saturation lines
  //----------------------------------
  let enthalLines = new Array(8);
  // For each enthalpy in the enthalpy range [0, 140]
  enthalRange.forEach(function (enthal, i) {
    // Calculate range of Absolute Humidity
    enthalLines[i] = dryBulbTempRange.map(function(temp) { 
        var absHumValue = psychrolib.GetHumRatioFromEnthalpyAndTDryBulb(enthal*1000, temp) * 1000; 
        var maxHumValue = psychrolib.GetHumRatioFromRelHum(temp, 1, pressure) * 1000;
        if (absHumValue > maxHumValue) {
          absHumValue = null;
        }
      return absHumValue; 
    })
  });

  // Calculate Wet Bulb Temperature lines
  //----------------------------------
  let wetBulbTempLines = new Array(8);
  // For each dry bulb temperature in the dry bulb temperature range [-5, 30] 
  wetBulbTempRange.forEach(function (wetBulbTemp, i) {
    // Calculate range of Absolute Humidity
    wetBulbTempLines[i] = dryBulbTempRange.map(function(temp) { 
      try {
        return psychrolib.GetHumRatioFromTWetBulb(temp, wetBulbTemp, pressure) * 1000; 
      } catch(e) {
        return null;
      }
    })
  });

  // Build chart
  //----------------------------------
  var traceRelHum100 = {
    x: dryBulbTempRange,
    y: relHumLines[9],
    mode: 'lines',
    type: 'scatter',
    opacity: 1,
    line: {'color': '#e74c3c'},
    legendgroup: 'Saturation line',
    hoverinfo: 'text+x+y',
    name: 'Saturation line',
    hovertext: 'RH: 100 %'
  };
  
  var traceRelHum90 = {
    x: dryBulbTempRange,
    y: relHumLines[8],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#e74c3c'},
    legendgroup: 'Relative Humidity',
    showlegend: false,
    hoverinfo: 'text+x+y',
    name: 'Relative Humidity',
    hovertext: 'RH: 90 %'
  };

  var traceRelHum80 = {
    x: dryBulbTempRange,
    y: relHumLines[7],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#e74c3c'},
    legendgroup: 'Relative Humidity',
    // showlegend: false,
    hoverinfo: 'text+x+y',
    name: 'Relative Humidity',
    hovertext: 'RH: 80 %'
  };

  var traceRelHum70 = {
    x: dryBulbTempRange,
    y: relHumLines[6],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#e74c3c'},
    legendgroup: 'Relative Humidity',
    showlegend: false,
    hoverinfo: 'text+x+y',
    name: 'Relative Humidity',
    hovertext: 'RH: 70 %'
  };
  
  var traceRelHum60 = {
    x: dryBulbTempRange,
    y: relHumLines[5],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#e74c3c'},
    legendgroup: 'Relative Humidity',
    showlegend: false,
    hoverinfo: 'text+x+y',
    name: 'Relative Humidity',
    hovertext: 'RH: 60 %'
  };

  var traceRelHum50 = {
    x: dryBulbTempRange,
    y: relHumLines[4],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#e74c3c'},
    legendgroup: 'Relative Humidity',
    showlegend: false,
    hoverinfo: 'text+x+y',
    name: 'Relative Humidity',
    hovertext: 'RH: 50 %'
  };
  
  var traceRelHum40 = {
    x: dryBulbTempRange,
    y: relHumLines[3],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#e74c3c'},
    legendgroup: 'Relative Humidity',
    showlegend: false,
    hoverinfo: 'text+x+y',
    name: 'Relative Humidity',
    hovertext: 'RH: 40 %'
  };

  var traceRelHum30 = {
    x: dryBulbTempRange,
    y: relHumLines[2],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#e74c3c'},
    legendgroup: 'Relative Humidity',
    showlegend: false,
    hoverinfo: 'text+x+y',
    name: 'Relative Humidity',
    hovertext: 'RH: 30 %'
  };
  
  var traceRelHum20 = {
    x: dryBulbTempRange,
    y: relHumLines[1],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#e74c3c'},
    legendgroup: 'Relative Humidity',
    showlegend: false,
    hoverinfo: 'text+x+y',
    name: 'Relative Humidity',
    hovertext: 'RH: 20 %'
  };
  
  var traceRelHum10 = {
    x: dryBulbTempRange,
    y: relHumLines[0],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#e74c3c'},
    legendgroup: 'Relative Humidity',
    showlegend: false,
    hoverinfo: 'text+x+y',
    name: 'Relative Humidity',
    hovertext: 'RH: 10 %'
  };

  var traceEnthal0 = {
    x: dryBulbTempRange,
    y: enthalLines[0],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#34495e'},
    legendgroup: 'Sat. Enthalpy',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Sat. Enthalpy: 0 kJ/kg dry air',
    name: 'Sat. Enthalpy',
    visible: 'legendonly'
  };

  var traceEnthal20 = {
    x: dryBulbTempRange,
    y: enthalLines[1],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#34495e'},
    legendgroup: 'Sat. Enthalpy',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Sat. Enthalpy: 20 kJ/kg dry air',
    name: 'Sat. Enthalpy',
    visible: 'legendonly'
  };

  var traceEnthal40 = {
    x: dryBulbTempRange,
    y: enthalLines[2],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#34495e'},
    legendgroup: 'Sat. Enthalpy',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Sat. Enthalpy: 40 kJ/kg dry air',
    name: 'Sat. Enthalpy',
    visible: 'legendonly'
  };

  var traceEnthal60 = {
    x: dryBulbTempRange,
    y: enthalLines[3],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#34495e'},
    legendgroup: 'Sat. Enthalpy',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Sat. Enthalpy: 60 kJ/kg dry air',
    name: 'Sat. Enthalpy',
    visible: 'legendonly'
  };

  var traceEnthal80 = {
    x: dryBulbTempRange,
    y: enthalLines[4],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#34495e'},
    legendgroup: 'Sat. Enthalpy',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Sat. Enthalpy: 80 kJ/kg dry air',
    name: 'Sat. Enthalpy',
    visible: 'legendonly'
  };

  var traceEnthal100 = {
    x: dryBulbTempRange,
    y: enthalLines[5],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#34495e'},
    legendgroup: 'Sat. Enthalpy',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Sat. Enthalpy: 100 kJ/kg dry air',
    name: 'Sat. Enthalpy',
    visible: 'legendonly'
  };

  var traceEnthal120 = {
    x: dryBulbTempRange,
    y: enthalLines[6],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#34495e'},
    legendgroup: 'Sat. Enthalpy',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Sat. Enthalpy: 120 kJ/kg dry air',
    name: 'Sat. Enthalpy',
    visible: 'legendonly'
  };

  var traceEnthal140 = {
    x: dryBulbTempRange,
    y: enthalLines[7],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#34495e'},
    legendgroup: 'Sat. Enthalpy',
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Sat. Enthalpy: 140 kJ/kg dry air',
    name: 'Sat. Enthalpy',
    visible: 'legendonly'
  };

  var traceWetBulbTemp_5 = {
    x: dryBulbTempRange,
    y: wetBulbTempLines[0],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#3498db'},
    legendgroup: 'Wet bulb temperature',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Wet bulb temperature: -5 °C',
    name: 'Wet bulb temperature'
  };
  
  var traceWetBulbTemp0 = {
    x: dryBulbTempRange,
    y: wetBulbTempLines[1],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#3498db'},
    legendgroup: 'Wet bulb temperature',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Wet bulb temperature: 0 °C',
    name: 'Wet bulb temperature'
  };

  var traceWetBulbTemp5 = {
    x: dryBulbTempRange,
    y: wetBulbTempLines[2],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#3498db'},
    legendgroup: 'Wet bulb temperature',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Wet bulb temperature: 5 °C',
    name: 'Wet bulb temperature'
  };

  var traceWetBulbTemp10 = {
    x: dryBulbTempRange,
    y: wetBulbTempLines[3],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#3498db'},
    legendgroup: 'Wet bulb temperature',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Wet bulb temperature: 10 °C',
    name: 'Wet bulb temperature'
  };

  var traceWetBulbTemp15 = {
    x: dryBulbTempRange,
    y: wetBulbTempLines[4],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#3498db'},
    legendgroup: 'Wet bulb temperature',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Wet bulb temperature: 15 °C',
    name: 'Wet bulb temperature'
  };

  var traceWetBulbTemp20 = {
    x: dryBulbTempRange,
    y: wetBulbTempLines[5],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#3498db'},
    legendgroup: 'Wet bulb temperature',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Wet bulb temperature: 20 °C',
    name: 'Wet bulb temperature'
  };

  var traceWetBulbTemp25 = {
    x: dryBulbTempRange,
    y: wetBulbTempLines[6],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#3498db'},
    legendgroup: 'Wet bulb temperature',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Wet bulb temperature: 25 °C',
    name: 'Wet bulb temperature'
  };

  var traceWetBulbTemp30 = {
    x: dryBulbTempRange,
    y: wetBulbTempLines[6],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#3498db'},
    legendgroup: 'Wet bulb temperature',
    showlegend: false,
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Wet bulb temperature: 30 °C',
    name: 'Wet bulb temperature'
  };

  var traceWetBulbTemp35 = {
    x: dryBulbTempRange,
    y: wetBulbTempLines[7],
    mode: 'lines',
    type: 'scatter',
    opacity: 0.65,
    line: {'color': '#3498db'},
    legendgroup: 'Wet bulb temperature',
    hoverinfo: 'text+x+y',
    hoverlabel: {namelength: -1},
    hovertext: 'Wet bulb temperature: 35 °C',
    name: 'Wet bulb temperature'
  };

  var data = [
    traceRelHum100, traceRelHum90, traceRelHum80, traceRelHum70, traceRelHum60, traceRelHum50, traceRelHum40, traceRelHum30, traceRelHum20, traceRelHum10,  // relative humidity lines
    traceEnthal140, traceEnthal120, traceEnthal100, traceEnthal80, traceEnthal60, traceEnthal40, traceEnthal20, traceEnthal0,  // enthalpy lines
    traceWetBulbTemp35, traceWetBulbTemp30, traceWetBulbTemp25, traceWetBulbTemp20, traceWetBulbTemp15, traceWetBulbTemp10, traceWetBulbTemp5, traceWetBulbTemp0, traceWetBulbTemp_5  // Wet bulb temperature lines
  ];

  Plotly.newPlot('psychrometricChart', data, layout, config);

}


// Create Psychrometric Chart
createPsychrometricChart(refPressInput.value);


var point = 0;  // counter for the point added to the plot

// Update Psychrometric Chart
function updatePsychrometricChart() {
  let dryBulbTempVal = document.getElementById('dryBulbTemp').value;
  let absHumVal = document.getElementById('absHum').value;

  point += 1;
  pointStr = 'Point ' + point.toString();

  Plotly.addTraces('psychrometricChart', {
    x: [dryBulbTempVal],
    y: [absHumVal],
    mode: 'markers',
    type: 'scatter',
    marker: {
      size: 10
    },
    hoverinfo: 'name+x+y',
    hoverlabel: {namelength: -1},
    name: pointStr
  });
}

psychrometricsForm.addEventListener('submit', function (event) { 
  event.preventDefault(); 
  updatePsychrometricChart();
});


// Clear Psychrometric Chart
var clearButton = document.getElementById('clearButton');
clearButton.addEventListener('click', function (event) { 
  point = 0;  // reset point count
  createPsychrometricChart(refPressInput.value);  // reset whole plot (redraw)
});


