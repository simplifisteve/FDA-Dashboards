---
title: FDA Recalls
theme: dashboard
toc: false
---

# FDA Recalls

<!-- Load and transform the data -->

```js
const recalls_fiscal = FileAttachment("data/recalls_fiscal.csv").csv({typed: true});
const recalls_product_types = FileAttachment("data/recalls_product_types.csv").csv({typed: true});
const recalls_product_class = FileAttachment("data/recalls_product_class.csv").csv({typed: true});
```

<div class="grid grid-cols-3">
  <div class="card"><h1>Total Recalls</h1>61,210</div>
  <div class="card">
    <h1>Note:</h1> Only showing data for Biologics, Drugs, and Devices product types. Fiscal Years: 2012 - 2024.
  </div>
</div>

---

## Recalled Products by Fiscal Year

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
    label: "Recalled Products",
    grid: true
  },
  color: {
    legend: true,
    domain: ["Biologics", "Drugs", "Devices"],
    range: ["green", "orange", "red"]
  },
  marks: [
    Plot.barY(recalls_fiscal, {
      x: "Fiscal Year", 
      y: "Count", 
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
    fontSize: 16,
    fontFamily: "sans-serif",
    backgroundColor: "#1e1e1e",
    color: "white"
  }
})}
</div>

---

## Recalled Products by Product Type

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
    label: "Product Type",
    axis: "bottom"
  },
  y: {
    label: "Recalled Products",
    grid: true
  },
  color: {
    legend: true,
    domain: ["Biologics", "Drugs", "Devices"],
    range: ["green", "orange", "red"]
  },
  marks: [
    Plot.barY(recalls_product_types, {
      x: "Product Type", 
      y: "Total", 
      fill: "Product Type", 
      tip: {
        format: {
          x: x => x,
          y: y => y.toLocaleString()
        }
      }
    }),
    Plot.ruleY([0])
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

## Recalled Products by Classification

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
    label: "Recalled Products",
    grid: true
  },
  color: {
    legend: true,
    domain: ["Class I", "Class II", "Class III"],
    range: ["green", "blue", "orange"]
  },
  marks: [
    Plot.barY(recalls_product_class, {
      x: "Fiscal Year", 
      y: "Total", 
      fill: "Product Classification", 
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
    fontSize: 16,
    fontFamily: "sans-serif",
    backgroundColor: "#1e1e1e",
    color: "white"
  }
})}
</div>