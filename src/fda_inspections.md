---
theme: dashboard
title: FDA Inspections
toc: false
---

# FDA Inspections

<!-- Load and transform the data -->

```js
const fda_inspections = FileAttachment("data/fda_inspections.csv").csv({
  typed: true,
  parse: {
    "Zip": d => d ? parseInt(d.replace(/,/g, '')) : null
  }
});

const inspection_countries = FileAttachment("data/inspection_countries.csv").csv({typed: true});
const class_fiscal = FileAttachment("data/class_fiscal.csv").csv({typed: true});
const class_product = FileAttachment("data/class_product.csv").csv({typed: true});
```

```js
const color = Plot.scale({
  color: {
    type: "categorical",
    domain: d3.groupSort(fda_inspections, (D) => -D.length, (d) => d["Country/Area"]).filter((d) => d !== "Foreign Countries"),
    unknown: "var(--theme-foreground-muted)"
  }
});
```
<!---Summary Cards--->

<div class="grid grid-cols-4">
  <div class="card">
    <h2>United States 🇺🇸</h2>
    <span class="big">${fda_inspections.filter((d) => d["Country/Area"] === "United States").length.toLocaleString("en-US")}</span>
  </div>
  <div class="card">
    <h2>Foreign Countries 🌏</h2>
    <span class="big">${fda_inspections.filter((d) => d["Country/Area"] !== "United States").length.toLocaleString("en-US")}</span>
  </div>
  <div class="card">
    <h1>Note:</h1> Only showing data for Biologics, Drugs, and Devices product types and Fiscal Years 2009 to 2024.
  </div>
</div>

---

## Map of Domestic Inspections

```js
// Load the TopoJSON file
const us = FileAttachment("data/states-albers-10m.json").json();
```

```js
// Load the inspection data
const inspectionData = FileAttachment("data/inspections_state.csv").csv({typed: true});
```

```js
// Convert TopoJSON to GeoJSON
const statesGeoJSON = topojson.feature(us, us.objects.states);
```

```js
// Create a map of state codes to inspection data
const inspectionDataMap = new Map(inspectionData.map(d => [d.State_Code, d]));
```

```js
// Create a mapping of state names to state codes
const stateNameToCode = Object.fromEntries(
  inspectionData.map(d => [d.State.toLowerCase(), d.State_Code])
);
```

```js
// Create a mapping of state codes to state names
const stateCodeToName = Object.fromEntries(
  inspectionData.map(d => [d.State_Code, d.State])
);
```

```js
// Function to calculate responsive dimensions
function getResponsiveDimensions() {
  const aspectRatio = 975 / 610; // Original width / height
  const maxWidth = Math.min(975, window.innerWidth * 0.8); // Using 80% of viewport width
  const maxHeight = Math.min(610, window.innerHeight * 1.0); // Using 100% of viewport height
  
  if (maxWidth / aspectRatio <= maxHeight) {
    return { width: maxWidth, height: maxWidth / aspectRatio };
  } else {
    return { width: maxHeight * aspectRatio, height: maxHeight };
  }
}

// Use the responsive dimensions in the chart
const { width, height } = getResponsiveDimensions();
```

```js
const chart = Plot.plot({
  projection: {
    type: d3.identity,
    domain: statesGeoJSON
  },
  color: {
    type: "quantize",
    domain: [1, d3.max(inspectionData, d => d.Total)],
    range: d3.schemeYlOrRd[7],
    unknown: "#cccccc",  // Light gray for states with no data
    legend: true,
    label: "Number of Inspections",
    tickFormat: d => d3.format(",")(Math.round(d))
  },
  marks: [
    Plot.geo(statesGeoJSON, {
      fill: d => {
        const stateName = d.properties.name.toLowerCase();
        const stateCode = stateNameToCode[stateName];
        const stateData = stateCode ? inspectionDataMap.get(stateCode) : null;
        return stateData ? stateData.Total : 0;
      },
      stroke: "black",
      strokeWidth: 1,
      title: d => {
        const stateName = d.properties.name.toLowerCase();
        const stateCode = stateNameToCode[stateName];
        const stateData = stateCode ? inspectionDataMap.get(stateCode) : null;
        return stateData 
          ? `${d.properties.name}: ${stateData.Total.toLocaleString()} inspections`
          : `${d.properties.name}: No data`;
      }
    })
  ],
  width,
  height,
  marginRight: 120, // Increase right margin for legend
  style: {
    color: "white",
    font: "sans-serif",
    fontSize: 14
  },
  x: {axis: null},  // Hide x-axis
  y: {axis: null},  // Hide y-axis
  margin: 0
});

// Log states that are in the inspection data but not rendered on the map
const renderedStates = new Set(statesGeoJSON.features.map(f => f.properties.name.toLowerCase()));
inspectionData.forEach(d => {
  if (d.State_Code && !renderedStates.has(d.State.toLowerCase())) {
    console.log(`State not rendered: ${d.State} (${d.State_Code})`);
  }
});

// Create the container for the chart
const container = html`<div class="card" style="display: flex; justify-content: center; 
align-items: center; height: 100vh; background-color: #1e1e1e;">
  ${chart}
</div>`;

// Add a resize listener to update the chart when the window size changes
window.addEventListener('resize', () => {
  const { width, height } = getResponsiveDimensions();
  chart.update({width, height});
});

display(container);
```

---

## Domestic & Foreign Inspections

<div class="card">
  ${Plot.plot({
  width: window.innerWidth - 40,
  height: 600,
  marginLeft: 80,
  marginRight: 80,
  marginTop: 40,
  marginBottom: 60,
  inset: 20,
  x: {
    label: "Fiscal Year",
    tickFormat: "d",
    grid: true
  },
  y: {
    label: "Inspection Count",
    grid: true
  },
  marks: [
    Plot.line(inspection_countries, {
      x: "Fiscal Year", 
      y: "Domestic", 
      stroke: "steelblue", 
      strokeWidth: 2, 
      tip: {
        format: {
          x: x => `Fiscal Year ${x}`,
          y: y => y.toLocaleString()
        }
      }
    }),
    Plot.line(inspection_countries, {
      x: "Fiscal Year", 
      y: "Foreign", 
      stroke: "orange", 
      strokeWidth: 2, 
      tip: {
        format: {
          x: x => `Fiscal Year ${x}`,
          y: y => y.toLocaleString()
        }
      }
    }),
    Plot.dot(inspection_countries, {x: "Fiscal Year", y: "Domestic", stroke: "steelblue", fill: "white"}),
    Plot.dot(inspection_countries, {x: "Fiscal Year", y: "Foreign", stroke: "orange", fill: "white"}),
    Plot.text(inspection_countries, {x: "Fiscal Year", y: "Domestic", text: d => d.Domestic, dy: -10, fontSize: 12}),
    Plot.text(inspection_countries, {x: "Fiscal Year", y: "Foreign", text: d => d.Foreign, dy: 10, fontSize: 12}),
    Plot.text(inspection_countries, {
      x: "Fiscal Year",
      y: "Domestic",
      text: d => d["Fiscal Year"] === 2024 ? "Domestic" : "",
      dx: 45,
      dy: -30,
      fontSize: 16,
      fill: "steelblue",
      fontWeight: "bold"
    }),
    Plot.text(inspection_countries, {
      x: "Fiscal Year",
      y: "Foreign",
      text: d => d["Fiscal Year"] === 2024 ? "Foreign" : "",
      dx: 45,
      dy: 20,
      fontSize: 16,
      fill: "orange",
      fontWeight: "bold"
    })
  ],
  style: {
    fontSize: 16,
    fontFamily: "sans-serif",
    backgroundColor: "#1e1e1e",
    color: "white"
  }
})}
</div>

---

## Inspections Classification by Fiscal Year

<div class="card">
  ${Plot.plot({
  width: window.innerWidth - 40,
  height: 600,
  marginLeft: 80,
  marginRight: 80,
  marginTop: 40,
  marginBottom: 60,
  inset: 20,
  x: {
    label: "Fiscal Year",
    tickFormat: "d",
    grid: true
  },
  y: {
    label: "Inspection Count",
    grid: true
  },
  color: {
    legend: true,
    domain: ["No Action Indicated (NAI)", "Voluntary Action Indicated (VAI)", "Official Action Indicated (OAI)"],
    range: ["green", "orange", "red"]
  },
  marks: [
    Plot.line(class_fiscal, {
      x: "Fiscal Year", 
      y: "Count", 
      stroke: "Classification", 
      strokeWidth: 2, 
      tip: {
        format: {
          x: x => `Fiscal Year ${x}`,
          y: y => y.toLocaleString()
        }
      }
    }),
    Plot.dot(class_fiscal, {x: "Fiscal Year", y: "Count", stroke: "Classification", fill: "white"}),
    Plot.text(class_fiscal, {x: "Fiscal Year", y: "Count", text: d => d.Count, dy: -10, fontSize: 14}),
  ],
  style: {
    fontSize: 16,
    fontFamily: "sans-serif",
    backgroundColor: "#1e1e1e",
    color: "white"
  }
})}
</div>

---

## Inspections Classification by Product Type

<div class="card">
  ${Plot.plot({
    width: window.innerWidth - 40,
    height: 600,
    marginLeft: 80,
    marginRight: 120,
    marginTop: 40,
    marginBottom: 60,
    x: {
      label: "Product Type",
      grid: true
    },
    y: {
      label: "Total Inspections",
      grid: true,
    },
    color: {
      legend: true,
      domain: ["No Action Indicated (NAI)", "Voluntary Action Indicated (VAI)", "Official Action Indicated (OAI)"],
      range: ["green", "yellow", "red"]
    },
    marks: [
      Plot.barY(class_product, Plot.groupX({
        y: "sum"},
        {x: "Product Type",
        y: "Total",
        fill: "Classification",
        tip: true}
      )),
    ],
    style: {
      fontSize: 14,
      fontFamily: "sans-serif",
      backgroundColor: "#1e1e1e",
      color: "white"
    }
  })}
</div>

---

## Inspections Details

<div class="card">
  ${Inputs.table(fda_inspections, {
    format: {
      "FEI Number": (a) => a.toFixed(0),
      "Fiscal Year": (b) => b.toFixed(0),
      "Inspection ID": (c) => c.toFixed(0),
      "Zip": (d) => d ? d.toLocaleString('en-US', {useGrouping: false}) : ''
    }
  })}
</div>