---
theme: dashboard
title: FDA Citations
toc: false
---

# FDA Citations

<!-- Load and transform the data -->

```js
const fda_citations = FileAttachment("data/fda_citations.csv").csv({typed: true});
const top_10_citations = FileAttachment("data/top_10_citations_table.csv").csv({typed: true});
```
<div class="grid grid-cols-4">
  <div class="card"><h1>Total Citations</h1>87,205</div>
  <div class="card">
    <h1>Note:</h1> Only showing data for Biologics, Drugs, and Devices product types and Fiscal Years 2009 to 2024.
  </div>
</div>

---

<div class="card">
  <h1>Top 10 Citations</h1>
  ${Plot.plot({
  width: window.innerWidth - 20,
  height: 900,
  marginLeft: 400,
  marginRight: 100,
  marginBottom: 50,
  x: {
    label: "Total Citations",
    tickFormat: d => d.toLocaleString(),
    grid: true,
    fontSize: 15
  },
  y: {
    label: null,
    fontSize: 15
  },
  marks: [
    Plot.barX(top_10_citations, {
      x: "Total",
      y: "Short Description",
      sort: {y: "-x"},
      fill: "steelblue",
      tip: true
    }),
    Plot.text(top_10_citations, {
      x: d => d.Total / 2, // Position text in the middle of each bar
      y: "Short Description",
      text: d => `${d["Act/CFR Number"]}`,
      dy: 0,
      fontSize: 14,
      fill: "white",
      fontWeight: "bold",
      textAnchor: "middle" // Center the text horizontally
    }),
    Plot.text(top_10_citations, {
      x: "Total",
      y: "Short Description",
      text: d => d.Total.toLocaleString(),
      dx: 10,
      dy: 0,
      fontSize: 14,
      fill: "white",
      fontWeight: "bold",
      textAnchor: "start" // position "Total" text to the right of the bar
    })
  ],
  style: {
    color: "white",
    fontFamily: "sans-serif",
    overflow: "visible",
    fontSize: 15
  }
})}
</div>

---

## Inspections Citations Details
<div class="card">
  ${Inputs.table(fda_citations, {
    format: {
      "Inspection ID": (a) => a.toFixed(0),
      "FEI Number": (b) => b.toFixed(0),
    }
  })}
</div>