---
title: FDA Compliance Actions
theme: dashboard
toc: false
---

# FDA Compliance Actions

<!-- Load and transform the data -->

```js
const fda_compliance_actions = FileAttachment("data/fda_compliance_actions.csv").csv({typed: true});
```

<div class="grid grid-cols-3">
  <div class="card"><h1>Total Compliance Actions</h1>50,000</div>
  <div class="card">
    <h1>Note:</h1> Only showing data for Biologics, Drugs, and Devices product types. Fiscal Years: 2012 - 2024.
  </div>
</div>

---

