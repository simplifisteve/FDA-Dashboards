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


<!---Inspection Type Chart--->
```js
function validateAndFormatData(data) {
  if (!Array.isArray(data) || data.length === 0) {
    throw new Error("Invalid or empty data array");
  }

  return data.map(function(item) {
    return {
      "Country/Area": item["Country/Area"],
      "Fiscal Year": +item["Fiscal Year"] // Ensure it's a number
    };
  }).filter(function(item) {
    return item["Country/Area"] && !isNaN(item["Fiscal Year"]);
  });
}

var validatedData = validateAndFormatData(fda_inspections);

// Function to create the chart
function inspection_type(data) {
  var preparedData = data.map(function(d) {
    return {
      ...d,
      inspectionType: d["Country/Area"] === "United States" ? "United States" : "Foreign Countries"
    };
  });

  var groupedData = d3.rollup(
    preparedData,
    function(v) {
      return d3.rollup(v, function(g) {
        return g.length;
      }, function(d) {
        return d.inspectionType;
      });
    },
    function(d) {
      return d["Fiscal Year"];
    }
  );

  var chartData = Array.from(groupedData, function([year, counts]) {
  return {
    year: year,
    "United States": counts.get("United States") || 0,
    "Foreign Countries": counts.get("Foreign Countries") || 0
    };
  });

  var otherCountryKeys = Array.from(new Set(chartData.flatMap(function(d) {
    return Object.keys(d);
  }).filter(function(key) {
    return key !== "year" && key !== "United States" && key !== "Foreign Countries";
  })));

  var chart = Plot.plot({
  title: "US vs Foreign Inspections by Fiscal Year",
  height: 500,
  y: {
    grid: true,
    label: "Number of Inspections"
  },
  x: {
    label: "Fiscal Year",
    tickFormat: d => d.toString()
  },
  color: {
    domain: ["United States", "Foreign Countries"],
    range: ["#4e79a7", "#e15759"],
    legend: true
  },
  marks: [
    Plot.rectY(chartData, {
      x: "year",
      y1: 0,
      y2: d => d["United States"],
      fill: "United States"
    }),
    Plot.rectY(chartData, {
      x: "year",
      y1: d => d["United States"],
      y2: d => d["United States"] + d["Foreign Countries"],
      fill: "Foreign Countries"
    }),
    Plot.ruleY([0])
  ]
});

  return chart;
}

// Create and display the chart
var chart = inspection_type(validatedData);

// Calculate and display totals
var totals = {
  "United States": validatedData.filter(function(d) {
    return d["Country/Area"] === "United States";
  }).length,
  "Foreign Countries": validatedData.filter(function(d) {
    return d["Country/Area"] !== "United States";
  }).length
};
```

<div class="grid grid-cols-1">
  <div class="card">
    ${resize((width) => inspection_type(validatedData, {width}))}
  </div>
</div>


