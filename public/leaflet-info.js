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

L.Control.Info = L.Control.extend({
  options: {
    title: "",
    content: "",
  },

  initialize: function (options) {
    L.Util.setOptions(this, options);
    this.infoContainer = L.DomUtil.create("div", "leaflet-control-layers");

    this.infoTitle = L.DomUtil.create("div");
    this.infoTitle.setAttribute("style", "padding: 5px;");
    this.infoContainer.appendChild(this.infoTitle);

    this.infoContent = L.DomUtil.create("div", "leaflet-popup-content");
    this.infoContainer.appendChild(this.infoContent);

    this.infoCloseButton = L.DomUtil.create("a", "leaflet-popup-close-button");
    this.infoCloseButton.innerHTML = `<i class="fa-solid fa-xmark"></i>`;
    this.infoCloseButton.setAttribute("style", "cursor: pointer");
    this.infoContainer.appendChild(this.infoCloseButton);

    this.setTitle(this.options.title);
    this.setContent(this.options.content);
    this.toggle(false);

    L.DomEvent.disableClickPropagation(this.infoContainer);
    L.DomEvent.on(this.infoCloseButton, "click", L.DomEvent.stop);
    L.DomEvent.on(
      this.infoContainer,
      "click",
      function () {
        this.toggle(true);
      },
      this,
    );
    L.DomEvent.on(
      this.infoCloseButton,
      "click",
      function () {
        this.toggle(false);
      },
      this,
    );
  },

  onAdd: function (map) {
    return this.infoContainer;
  },

  onRemove: function (map) {},

  setTitle: function (title) {
    this.options.title = title;
    this.infoTitle.innerHTML = title;
  },

  setContent: function (content) {
    this.options.content = content;
    this.infoContent.innerHTML = content;
  },

  toggle: function (extend) {
    this.infoTitle.style.display = !extend ? "" : "none";
    this.infoContent.style.display = extend ? "" : "none";
    this.infoCloseButton.style.display = extend ? "" : "none";
    this.infoContainer.style.cursor = !extend ? "pointer" : "";
  },
});

L.control.info = function (opts) {
  return new L.Control.Info(opts);
};
