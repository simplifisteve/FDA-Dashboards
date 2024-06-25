---
title: Home
toc: false
---

<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 2rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>

<div class="hero">
  <h1>FDA Dashboards</h1>
  <h2>Only showing data for Biologics, Drugs, and Devices.</h2>
  <a href="https://datadashboard.fda.gov/ora/cd/inspections.htm">View original source<span style="display: inline-block; margin-left: 0.25rem;">↗︎</span></a>
</div>

<div class="grid grid-cols-3">
  <div class="card"><h1>Total Inspections</h1>108,769</div>
  <div class="card"><h1>Total Citations</h1>87,205</div>
  <div class="card"><h1>Published 483s</h1>1,727</div>
</div>

---

## Data Tables

Here are the original data tables from the FDA website:

<!-- Load and transform the data -->

```js
const fda_inspections = FileAttachment("fda_inspections.csv").csv({typed: true});
const fda_citations = FileAttachment("fda_citations.csv").csv({typed: true});
const fda_483s = FileAttachment("fda_483s.csv").csv({typed: true});
```

### Inspections Details
<div class="card">
  ${Inputs.table(fda_inspections)}
</div>

### Inspections Citations Details
<div class="card">
  ${Inputs.table(fda_citations)}
</div>

### Published 483s
<div class="card">
  ${Inputs.table(fda_483s)}
</div>