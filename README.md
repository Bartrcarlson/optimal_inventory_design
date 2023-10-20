# Plot alloctation by strata

```mermaid
graph TD;
a[input shapefile w/ strata] --> b[[generate spreedsheet using strata names]];
e[user input] --> g[filled in spreedsheet];
b --> g;
c[raster w/ pixel values] --> d[[calculate standard devation of strata based on pixel values]];
d --> f[output standard devation of strata];
h[user editing] --> f;
f --> {calulate number of plots per strata};
```
