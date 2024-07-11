---
title: FDA Compliance Actions
theme: dashboard
toc: true
---

# FDA Compliance Actions

<!-- Load and transform the data -->

```js
const fda_compliance_actions = FileAttachment("data/fda_compliance_actions.csv").csv({typed: true});
const warning_letters_fiscal = FileAttachment("data/warning_letters_fiscal.csv").csv({typed: true});
const compliance_fiscal = FileAttachment("data/compliance_fiscal.csv").csv({typed: true});
const compliance_products = FileAttachment("data/compliance_products.csv").csv({typed: true});
```

<div class="grid grid-cols-3">
  <div class="card"><h1>Global Compliance Actions</h1>4,233</div>
  <div class="card"><h1>US Compliance Actions</h1>2,992 or 70.7% of total</div>
  <div class="card">
    <h1>Note:</h1> Only showing data for Biologics, Drugs, and Devices product types and Fiscal Years 2008 to 2024.
  </div>
</div>

---

## Global Map of Compliance Actions

```js
// Load the TopoJSON file
const world = FileAttachment("data/countries-110m.json").json();
```

```js
// Load the compliance action data
const complianceData = FileAttachment("data/compliance_countries.csv").csv({typed: true});
```

```js
// Convert TopoJSON to GeoJSON
const countriesGeoJSON = topojson.feature(world, world.objects.countries);
```

```js
// Create a map of ISO codes to compliance data
const complianceDataMap = new Map(complianceData.map(d => [d.ISO_Code, d]));
```

<!-- ```js
// Console.log to catch errors
console.log(complianceData.slice(0, 67));
``` -->

```js
// Function to validate coordinates
function validateCoordinates(country, lon, lat) {
  if (lon === null || lat === null) return null;
  
  // Correct incorrect coordinates from CSV
  if (country === "Thailand") lon = 100.992541;
  if (country === "Jordan") {
    lat = 31.24;
    lon = 36.51;
  }
  if (country === "Armenia") {
    lat = 40.0691;
    lon = 45.0382;
  }
  
  // Ensure longitude is between -180 and 180
  lon = ((lon + 180) % 360) - 180;
  
  // Ensure latitude is between -90 and 90
  lat = Math.max(-90, Math.min(90, lat));
  
  return [lon, lat];
}
```

```js
// Function to calculate responsive dimensions
function getResponsiveDimensions() {
  const aspectRatio = 975 / 610;
  const maxWidth = Math.min(975, window.innerWidth * 0.8);
  const maxHeight = Math.min(610, window.innerHeight * 0.8);
  
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
  projection: d3.geoNaturalEarth1(), // {type: "orthographic", rotate: [45, -5]},
  color: {
    type: "quantize",
    domain: [1, d3.max(complianceData, d => d.Count)],
    range: d3.schemeBlues[7],
    legend: true,
    label: "Number of Compliance Actions",
    tickFormat: d => d3.format(",")(Math.round(d))
  },
  marks: [
    Plot.geo(countriesGeoJSON, {
      fill: d => {
        const countryData = complianceDataMap.get(d.id);
        return countryData ? countryData.Count : 0;
      },
      stroke: "black", 
      strokeWidth: 1.0,
    }),
    // Plot.sphere(),
    Plot.dot(complianceData.filter(d => d.longitude != null && d.latitude != null), {
      x: d => {
      const coords = validateCoordinates(d.Country, +d.longitude, +d.latitude);
      return coords ? coords[0] : null;
    },
    y: d => {
      const coords = validateCoordinates(d.Country, +d.longitude, +d.latitude);
      return coords ? coords[1] : null;
    },
    r: d => Math.sqrt(d.Count) * 0.5,
    fill: d => d.Count,
    fillOpacity: 1.0,
    stroke: "black",
    strokeWidth: 1.0,
    title: d => `${d.Country}: ${d.Count.toLocaleString()} compliance actions (${d.Percentage.toFixed(1)}% of total)`
  })
  ],
  width,
  height,
  marginRight: 0,
  marginLeft: 0,
  style: {
    backgroundColor: "#1e1e1e",
    color: "white",
    fontFamily: "sans-serif",
    fontSize: 18
  },
  x: {axis: null},
  y: {axis: null},
});

// Create the container for the chart
const container = html`<div class="card" style="display: flex; justify-content: center; 
align-items: center; height: 80vh; background-color: #1e1e1e;">
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

## Warning Letters by Fiscal Year & Product Type

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
    label: "Warning Letters",
    grid: true
  },
  color: {
    legend: true,
    domain: ["Biologics", "Drugs", "Devices"],
    range: ["#23CE6B", "#F45D01", "#004E7C"]
  },
  marks: [
    Plot.barY(warning_letters_fiscal, {
      x: "Fiscal Year", 
      y: "Total",
      fill: "Product Type", 
      tip: {
        format: {
          x: x => `Fiscal Year ${x}`,
          y: y => y.toLocaleString()
        }
      }
    }),
    Plot.ruleY([0])
  ],
  style: {
    fontSize: 18,
    fontFamily: "sans-serif",
    backgroundColor: "#1e1e1e",
    color: "white"
  }
})}
</div>

---

## Injunctions & Seizures by Fiscal Year

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
    label: "Action Type",
    grid: true
  },
  color: {
    legend: true,
    domain: ["Injunction", "Seizure"],
    range: ["#004e7c", "#23CE6B"]
  },
  marks: [
    Plot.barY(compliance_fiscal, {
      x: "Fiscal Year", 
      y: "Total",
      fill: "Action Type", 
      tip: {
        format: {
          x: x => `Fiscal Year ${x}`,
          y: y => y.toLocaleString()
        }
      }
    }),
    Plot.ruleY([0])
  ],
  style: {
    fontSize: 18,
    fontFamily: "sans-serif",
    backgroundColor: "#1e1e1e",
    color: "white"
  }
})}
</div>

---

## Injunctions & Seizures by Product Type

<div class="card">
  ${Plot.plot({
  width: window.innerWidth - 35,
  height: 450,
  marginLeft: 100,
  marginRight: 80,
  marginTop: 40,
  marginBottom: 60,
  x: {
    label: "Total Actions Taken",
    grid: true
  },
  y: {
    label: null,
    domain: compliance_products.map(d => d["Product Type"]).filter((v, i, a) => a.indexOf(v) === i)
  },
  color: {
    legend: true,
    domain: ["Injunction", "Seizure"],
    range: ["#004E7C", "#23CE6B"]
  },
  marks: [
    Plot.barX(compliance_products, {
      y: "Product Type",
      x: "Total",
      fill: "Action Type",
      sort: {y: "x", reverse: true},
      tip: {
        format: {
          x: x => x.toLocaleString(),
          y: y => y
        }
      }
    }),
    Plot.ruleX([0])
  ],
  style: {
    fontSize: 18,
    fontFamily: "sans-serif",
    backgroundColor: "#1e1e1e",
    color: "white"
  }
})}
</div>

---

## Compliance Actions Details

<div class="card">
  ${Inputs.table(fda_compliance_actions, {
    format: {
      "FEI Number": (a) => a != null ? a.toString().replace(/,/g, '') : '',
    }
  })}
</div>

