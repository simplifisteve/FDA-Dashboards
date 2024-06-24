---
title: Weather Report
toc: false
---

<div class="grid grid-cols-2">
  <div class="card"><h1>A</h1>1 × 1</div>
  <div class="card grid-rowspan-2"><h1>B</h1>1 × 2</div>
  <div class="card"><h1>C</h1>1 × 1</div>
  <div class="card grid-colspan-2"><h1>D</h1>2 × 1</div>
</div>

```js
const industryInput = Inputs.select(industries.map((d) => d.industry), {unique: true, sort: true, label: "Industry:"});
const industry = Generators.input(industryInput);
```

<div class="card" style="display: flex; flex-direction: column; gap: 1rem;">
  ${industryInput}
  ${resize((width) => Plot.plot({
    width,
    y: {grid: true, label: "Unemployed (thousands)"},
    marks: [
      Plot.areaY(industries.filter((d) => d.industry === industry), {x: "date", y: "unemployed", fill: "var(--theme-foreground-muted)", curve: "step"}),
      Plot.lineY(industries.filter((d) => d.industry === industry), {x: "date", y: "unemployed", curve: "step"}),
      Plot.ruleY([0])
    ]
  }))}
</div>

<div class="grid grid-cols-1">
  <div class="card">${resize((width) => temperaturePlot(forecast, {width}))}</div>
</div>

```js
const forecast = FileAttachment("./data/forecast.json").json();
```

```js
function temperaturePlot(data, {width} = {}) {
  return Plot.plot({
    title: "Hourly temperature forecast - White House",
    width,
    x: {type: "utc", ticks: "day", label: null},
    y: {grid: true, inset: 10, label: "Degrees (F)"},
    marks: [
      Plot.lineY(data.properties.periods, {
        x: "startTime",
        y: "temperature",
        z: null, // varying color, not series
        stroke: "temperature",
        curve: "step-after"
      })
    ]
  });
}
```
<!---
<div class="grid grid-cols-2" style="grid-auto-rows: auto;">
  <div class="card">Call me Ishmael.</div>
  <div class="card">Some years ago—never mind how long precisely—having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world.</div>
  <div class="card">It is a way I have of driving off the spleen and regulating the circulation.</div>
</div>
--->

<div class="card" style="max-width: 640px;">
  <h2>It gets hotter during summer</h2>
  <h3>And months have 28–31 days</h3>
  ${Plot.cell(weather.slice(-365), 
  {x: (d) => d.date.getUTCDate(), 
  y: (d) => d.date.getUTCMonth(), 
  fill: "temp_max", tip: true, inset: 0.5}).plot({marginTop: 0, height: 240, padding: 0})}
</div>

<div class="grid grid-cols-2">
  <div class="card">
    <h2>Lorem ipsum</h2>
    <p>Id ornare arcu odio ut sem nulla pharetra. Aliquet lectus proin nibh nisl condimentum id venenatis a. Feugiat sed lectus vestibulum mattis ullamcorper velit. Aliquet nec ullamcorper sit amet. Sit amet tellus cras adipiscing. Condimentum id venenatis a condimentum vitae. Semper eget duis at tellus. Ut faucibus pulvinar elementum integer enim.</p>
    <p>Et malesuada fames ac turpis. Integer vitae justo eget magna fermentum iaculis eu non diam. Aliquet risus feugiat in ante metus dictum at. Consectetur purus ut faucibus pulvinar.</p>
  </div>
  <div class="card" style="padding: 0;">
    ${Inputs.table(industries)}
  </div>
</div>

<div class="note">This is a note.</div>

<div class="tip">
  <p>This is a <i>styled</i> tip using <small>HTML</small>.</p>
</div>

<div class="tip">

This is a *styled* tip using **Markdown**.

</div>

<div class="warning" label="⚠️ Danger ⚠️">No lifeguard on duty. Swim at your own risk!</div>

<div class="caution">This is a caution.</div>