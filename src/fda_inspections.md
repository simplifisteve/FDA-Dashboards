---
theme: dashboard
title: FDA Inspections
toc: false
---

# FDA Inspections

<!-- Load and transform the data -->

```js
const fda_inspections = FileAttachment("fda_inspections.csv").csv({
  typed: true,
  parse: {
    "Zip": d => d ? parseInt(d.replace(/,/g, '')) : null
  }
});

const inspection_countries = FileAttachment("data/inspection_countries.csv").csv({typed: true});
const class_fiscal = FileAttachment("data/class_fiscal.csv").csv({typed: true});
const class_product = FileAttachment("data/class_product.csv").csv({typed: true});
const inspectionData = FileAttachment("data/inspections_state.csv").csv({typed: true})
const us = FileAttachment("data/states-albers-10m.json").json();
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

<div class="grid grid-cols-2">
  <div class="card">
    <h2>United States 🇺🇸</h2>
    <span class="big">${fda_inspections.filter((d) => d["Country/Area"] === "United States").length.toLocaleString("en-US")}</span>
  </div>
  <div class="card">
    <h2>Foreign Countries 🌏</h2>
    <span class="big">${fda_inspections.filter((d) => d["Country/Area"] !== "United States").length.toLocaleString("en-US")}</span>
  </div>
</div>

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
    Plot.line(inspection_countries, {x: "Fiscal Year", y: "Domestic", stroke: "steelblue", strokeWidth: 2, tip: true}),
    Plot.line(inspection_countries, {x: "Fiscal Year", y: "Foreign", stroke: "orange", strokeWidth: 2, tip: true}),
    Plot.dot(inspection_countries, {x: "Fiscal Year", y: "Domestic", stroke: "steelblue", fill: "white"}),
    Plot.dot(inspection_countries, {x: "Fiscal Year", y: "Foreign", stroke: "orange", fill: "white"}),
    Plot.text(inspection_countries, {x: "Fiscal Year", y: "Domestic", text: d => d.Domestic, dy: -10, fontSize: 12}),
    Plot.text(inspection_countries, {x: "Fiscal Year", y: "Foreign", text: d => d.Foreign, dy: 10, fontSize: 12}),
    Plot.text(inspection_countries, {
      x: "Fiscal Year",
      y: "Domestic",
      text: d => d["Fiscal Year"] === 2024 ? "Domestic" : "",
      dx: 45,  // Increased horizontal offset
      dy: -30,  // Added vertical offset to move label up
      fontSize: 16,
      fill: "steelblue",
      fontWeight: "bold"
    }),
    Plot.text(inspection_countries, {
      x: "Fiscal Year",
      y: "Foreign",
      text: d => d["Fiscal Year"] === 2024 ? "Foreign" : "",
      dx: 45,  // Increased horizontal offset
      dy: 20,  // Added vertical offset to move label down
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
    Plot.line(class_fiscal, {x: "Fiscal Year", y: "Count", stroke: "Classification", strokeWidth: 2, tip: true}),
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

## Map of Domestic Inspections

```js
// Convert TopoJSON to GeoJSON
const states = topojson.feature(us, us.objects.states)

// Create a more diverse color scale
const color = d3.scaleQuantile()
  .domain(inspectionData.map(d => d.Total))
  .range(d3.schemeYlOrRd[9])

// Create the map
const chart = Plot.plot({
  projection: "albers-usa",
  color: {
    type: "quantile",
    scheme: "YlOrRd",
    n: 9
  },
  marks: [
    Plot.geo(states, {
      fill: d => {
        const stateData = inspectionData.find(s => s.State_Code === d.properties.code);
        return stateData ? color(stateData.Total) : "#ccc";
      },
      stroke: "white",
      strokeWidth: 0.5,
      title: d => {
        const stateData = inspectionData.find(s => s.State_Code === d.properties.code);
        return stateData 
          ? `${d.properties.name}: ${stateData.Total.toLocaleString()} inspections`
          : `${d.properties.name}: No data`;
      }
    }),
    Plot.text(states.features, {
      text: d => d.properties.code,
      fill: "black",
      stroke: "white",
      strokeWidth: 0.5,
      fontSize: 8,
      dx: d => d.properties.dx || 0,
      dy: d => d.properties.dy || 0
    })
  ],
  width: 975,
  height: 610,
  style: {
    backgroundColor: "white",
    overflow: "visible"
  },
  // Add a color legend
  legend: true
})

// Display the chart
display(chart)
```

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