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
    title: "Info",
    titleTooltip: "Click here for more info",
    content: "",
    maxWidth: "250px",
    titleClass: "",
    contentClass: "",
  },

  initialize: function (options) {
    L.Util.setOptions(this, options);
    this._infoContainer = null;
    this._infoTitleContainer = null;
    this._infoBodyContainer = null;
    this._infoCloseButtonContainer = null;
    this._infoContentContainer = null;
    this._infoTitle = this.options.title;
    this._infoTitleTooltip = this.options.titleTooltip;
    this._infoContent = this.options.content;
    this._titleShown = false;
    this._titleClass = this.options.titleClass;
    this._contentClass = this.options.contentClass;
    this._infoTitleStyle = "padding: 5px;";
    this._infoContainerClasses = "leaflet-control-layers leaflet-control";
  },

  onAdd: function (map) {
    let infoContainer = L.DomUtil.create("div", "leaflet-control-layers");

    let infoTitle = L.DomUtil.create("div");
    infoContainer.appendChild(infoTitle);
    infoTitle.setAttribute("style", this._infoTitleStyle);

    let infoBody = L.DomUtil.create("div", "leaflet-popup-content-wraper");
    infoContainer.appendChild(infoBody);
    infoBody.setAttribute("style", "max-width:" + this.options.maxWidth);

    let infoContent = L.DomUtil.create("div", "leaflet-popup-content");
    infoBody.appendChild(infoContent);

    let infoCloseButton = L.DomUtil.create("a", "leaflet-popup-close-button");
    infoContainer.appendChild(infoCloseButton);
    infoCloseButton.innerHTML = "x";
    infoCloseButton.setAttribute("style", "cursor: pointer");

    this._infoContainer = infoContainer;
    this._infoTitleContainer = infoTitle;
    this._infoBodyContainer = infoBody;
    this._infoContentContainer = infoContent;
    this._infoCloseButtonContainer = infoCloseButton;

    infoTitle.innerHTML = this._infoTitle;
    infoContent.innerHTML = this._infoContent;
    this._showTitle();

    L.DomEvent.disableClickPropagation(infoContainer);
    L.DomEvent.on(infoCloseButton, "click", L.DomEvent.stop);
    L.DomEvent.on(infoContainer, "click", this._showContent, this);
    L.DomEvent.on(infoCloseButton, "click", this._showTitle, this);

    return infoContainer;
  },

  onRemove: function (map) {},

  setTitle: function (title) {
    this._infoTitle = title;
    if (this._infoTitleContainer != null) {
      this._infoTitleContainer.innerHTML = title;
    }
  },

  setTitleTooltip: function (titleTooltip) {
    this._infoTitleTooltip = titleTooltip;
    if (this._titleShown) {
      this._showTitleTooltip(true);
    }
  },

  setContent: function (content) {
    this._infoContent = content;
    if (this._infoContentContainer != null) {
      this._infoContentContainer.innerHTML = content;
    }
  },

  setTitleClass: function (titleClass) {
    this._titleClass = titleClass;
    if (this._titleShown) {
      this._addInfoClass(this._titleClass);
    }
  },

  setContentClass: function (contentClass) {
    this._contentClass = contentClass;
    if (!this._titleShown) {
      this._addInfoClass(this._contentClass);
    }
  },

  _showTitle: function (evt) {
    this._addInfoClass(this._titleClass);
    this._displayElement(this._infoTitleContainer, true);
    this._displayElement(this._infoBodyContainer, false);
    this._displayElement(this._infoCloseButtonContainer, false);
    this._showTitleTooltip(true);
    this._setCursorToPointer(this._infoContainer, true);
    this._titleShown = true;
  },

  _showContent: function (evt) {
    this._addInfoClass(this._contentClass);
    this._displayElement(this._infoTitleContainer, false);
    this._displayElement(this._infoBodyContainer, true);
    this._displayElement(this._infoCloseButtonContainer, true);
    this._showTitleTooltip(false);
    this._setCursorToPointer(this._infoContainer, false);
    this._titleShown = false;
  },

  _showTitleTooltip: function (showIt) {
    this._infoContainer.setAttribute("Title", showIt ? this._infoTitleTooltip : "");
  },

  _displayElement: function (element, displayIt) {
    element.style.display = displayIt ? "" : "none";
  },

  _setCursorToPointer: function (element, setIt) {
    element.style.cursor = setIt ? "pointer" : "";
  },

  _addInfoClass: function (classToAdd) {
    L.DomUtil.setClass(this._infoContainer, this._infoContainerClasses + " " + classToAdd);
  },
});

L.control.info = function (opts) {
  return new L.Control.Info(opts);
};
