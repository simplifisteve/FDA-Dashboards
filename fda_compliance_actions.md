---
title: FDA Compliance Actions
theme: dashboard
toc: false
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
  <div class="card"><h1>Total Compliance Actions</h1>4,233</div>
  <div class="card">
    <h1>Note:</h1> Only showing data for Biologics, Drugs, and Devices product types. Fiscal Years: 2008 - 2024.
  </div>
</div>

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
    range: ["green", "orange", "blue"]
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
    range: ["blue", "green"]
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
  width: window.innerWidth - 40,
  height: 400,
  marginLeft: 120,
  marginRight: 80,
  marginTop: 40,
  marginBottom: 60,
  x: {
    label: "Total Actions Taken",
    grid: true
  },
  y: {
    label: "Product Type",
    domain: compliance_products.map(d => d["Product Type"]).filter((v, i, a) => a.indexOf(v) === i)
  },
  color: {
    legend: true,
    domain: ["Injunction", "Seizure"],
    range: ["blue", "green"]
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

## Map of Compliance Actions

---

## Compliance Actions Details
<div class="card">
  ${Inputs.table(fda_compliance_actions, {
    format: {
      "FEI Number": (a) => a != null ? a.toString().replace(/,/g, '') : '',
    }
  })}
</div>

