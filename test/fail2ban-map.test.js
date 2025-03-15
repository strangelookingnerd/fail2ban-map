const puppeteer = require("puppeteer");

describe("Page Loading Test", () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch();
    page = await browser.newPage();
    await page.goto("file://" + __dirname + "/../public/index.html");
  });

  afterAll(async () => {
    await browser.close();
  });

  test("Check if map is loaded", async () => {
    const map = await page.$("#map") ;
    expect(map !== null).toBe(true);
    const classList = await page.$eval("#map", (el) => el.classList.value);
    expect(classList).toContain("leaflet-container")
  });
});
