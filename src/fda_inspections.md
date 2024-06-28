---
theme: dashboard
title: FDA Inspections
toc: false
---

# FDA Inspections

<!-- Load and transform the data -->

```js
const fda_inspections = FileAttachment("fda_inspections.csv").csv({typed: true});
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
    <h2>Foreign Countries</h2>
    <span class="big">${fda_inspections.filter((d) => d["Country/Area"] !== "United States").length.toLocaleString("en-US")}</span>
  </div>
</div>


