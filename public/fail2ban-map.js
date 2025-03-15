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
    minZoom: 2,
    worldCopyJump: true,
  });

  // list of tile providers can be seen here: https://leaflet-extras.github.io/leaflet-providers/preview/
  L.tileLayer.provider("CartoDB.DarkMatterNoLabels").addTo(map);

  const info = L.control.info({
    title: `<i style="color: rgb(69, 69, 69)" class="fa-solid fa-circle-info"></i>&nbsp;Info`,
  });
  const markersLayer = L.geoJson(null);
  const marker = L.ExtraMarkers.icon({
    icon: "fa-solid fa-ban",
    markerColor: "red",
    shape: "circle",
    svg: "true",
  });
  const heatmapLayer = L.heatLayer([], {
    radius: 35,
    gradient: {
      0.01: "rgb(0,0,255)",
      0.05: "rgb(0,127,255)",
      0.1: "rgb(0,255,255)",
      0.15: "rgb(0,255,127)",
      0.2: "rgb(0,255,0)",
      0.25: "rgb(127,255,0)",
      0.3: "rgb(255,255,0)",
      0.35: "rgb(255,127,0)",
      0.4: "rgb(255,0,0)",
      0.45: "rgb(255,0,127)",
      0.5: "rgb(255,0,255)",
      0.55: "rgb(127,0,255)",
    },
  });

  try {
    const response = await fetch("places.geojson");
    const data = await response.json();

    info.setContent(`
    <a class="github-fork-ribbon" target="_blank" href="https://github.com/strangelookingnerd/fail2ban-map" 
       data-ribbon="Fork me on GitHub" title="Fork me on GitHub">Fork me on GitHub</a>
    <div class="info-container">
        <img src="./favicon.ico" alt="fail2ban-map icon" title="fail2ban-map &copy; strangelookingnerd">
        <div class="banned-count">${data.features.length} banned IP</div>
    </div>`);

    data.features.forEach((feature) => {
      const { properties, geometry } = feature;
      if (!properties?.show_on_map) return;

      const layer = L.geoJSON(feature, {
        pointToLayer: (feature, latlng) => {
          return L.marker(latlng, { icon: marker });
        },
        onEachFeature: (feature, layer) => {
          if (properties?.place) {
            layer.bindTooltip(properties.place);
          }
        },
      });

      markersLayer.addLayer(layer);
      heatmapLayer.addLatLng(geometry.coordinates.reverse());
    });
  } catch (error) {
    console.error("Error loading GeoJSON:", error);
  }

  markersLayer.addTo(map);
  info.addTo(map);

  L.control
    .layers({ Markers: markersLayer, Heatmap: heatmapLayer }, null, {
      collapsed: false,
    })
    .setPosition("bottomleft")
    .addTo(map);
};
