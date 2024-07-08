---
title: FDA Recalls
theme: dashboard
toc: false
---

# FDA Recalls

<!-- Load and transform the data -->

```js
const fda_recalls = FileAttachment("data/fda_recalls.csv").csv({typed: true});
const recalls_product_fiscal = FileAttachment("data/recalls_product_fiscal.csv").csv({typed: true});
const recalls_product_types = FileAttachment("data/recalls_product_types.csv").csv({typed: true});
const recalls_product_class = FileAttachment("data/recalls_product_class.csv").csv({typed: true});
const recalls_events_fiscal = FileAttachment("data/recalls_events_fiscal.csv").csv({typed: true});
const recalls_events_types = FileAttachment("data/recalls_events_types.csv").csv({typed: true});
const recalls_events_status = FileAttachment("data/recalls_events_status.csv").csv({typed: true});
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
    Plot.barY(recalls_product_fiscal, {
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

---

## Recall Events by Status

<div class="card">
  ${Plot.plot({
    width: window.innerWidth - 40,
    height: 500,
    marginLeft: 120,
    marginRight: 60,
    marginTop: 40,
    marginBottom: 60,
    x: {
      label: "Total Events",
      grid: true
    },
    y: {
      label: null,
      domain: recalls_events_status.map(d => d.Status),
      padding: 0.2
    },
    color: {
      legend: true,
      domain: ["Completed", "Ongoing", "Terminated"],
      range: ["#4CAF50", "#FFC107", "#F44336"]
    },
    marks: [
      Plot.barX(recalls_events_status, {
        y: "Status",
        x: "Total",
        fill: "Status",
        sort: {y: "x", reverse: true},
        tip: {
          format: {
            x: x => x.toLocaleString()
          }
        }
      }),
      Plot.text(recalls_events_status, {
        y: "Status",
        x: "Total",
        text: d => d.Total.toLocaleString(),
        dx: -15,
        fill: "white",
        fontWeight: "bold",
        fontSize: 20,
        textAnchor: "start"
      })
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

## Recall Events by Fiscal Year & Event Classification

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
    label: "Recall Events",
    grid: true
  },
  color: {
    legend: true,
    domain: ["Class I", "Class II", "Class III"],
    range: ["green", "orange", "blue"]
  },
  marks: [
    Plot.barY(recalls_events_fiscal, {
      x: "Fiscal Year", 
      y: "Total", 
      fill: "Event Classification", 
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

## Recall Events by Product Type

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
    label: "Recall Events",
    grid: true
  },
  color: {
    legend: true,
    domain: ["Class I", "Class II", "Class III"],
    range: ["green", "orange", "blue"]
  },
  marks: [
    Plot.barY(recalls_events_types, {
      x: "Product Type", 
      y: "Total", 
      fill: "Event Classification",
      stack: true,
      sort: {x: "y", reverse: true},
      tip: {
        format: {
          x: x => x,
          y: y => y.toLocaleString(),
          fill: f => `${f}: `
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

## Recalls Details
<div class="card">
  ${Inputs.table(fda_recalls, {
    format: {
      "FEI Number": (a) => a != null ? a.toString().replace(/,/g, '') : '',
      "Product ID": (b) => b != null ? b.toString().replace(/,/g, '') : '',
      "Event ID": (c) => c != null ? c.toString().replace(/,/g, '') : '',
    }
  })}
</div>

