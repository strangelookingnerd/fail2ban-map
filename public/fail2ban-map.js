/**
 * MIT License
 *
 * Copyright (c) 2025 strangelookingnerd
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

window.onload = async function () {
  const map = L.map("map", {
    center: [30, 0],
    zoom: 3,
    minZoom: 3,
  });
  map.setMaxBounds(map.getBounds());

  // list of tile providers can be seen here: https://leaflet-extras.github.io/leaflet-providers/preview/
  L.tileLayer
    .provider("CartoDB.DarkMatterNoLabels", {
      noWrap: true,
    })
    .addTo(map);

  const markersLayer = L.geoJson(null);
  const heatmapLayer = new HeatmapOverlay({ radius: 5, maxOpacity: 0.8 });
  const heatmapDataset = { data: [] };

  try {
    const response = await fetch("places.geojson");
    const data = await response.json();

    data.features.forEach((feature) => {
      const { properties, geometry } = feature;
      if (!properties?.show_on_map) return;

      const layer = L.geoJSON(feature, {
        onEachFeature: (feature, layer) => {
          if (properties?.place) {
            layer.bindTooltip(properties.place);
          }
        },
      });

      markersLayer.addLayer(layer);
      heatmapDataset.data.push({
        lng: geometry.coordinates[0],
        lat: geometry.coordinates[1],
      });
    });

    heatmapLayer.setData(heatmapDataset);
  } catch (error) {
    console.error("Error loading GeoJSON:", error);
  }

  markersLayer.addTo(map);

  L.control
    .layers({ Markers: markersLayer, Heatmap: heatmapLayer }, null, {
      collapsed: false,
    })
    .setPosition("bottomleft")
    .addTo(map);
};
