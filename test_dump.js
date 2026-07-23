const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    console.log("Navigating...");
    await page.goto(`file://${process.cwd()}/index.html`);
    
    console.log("Waiting for Kiro Doc Tab...");
    const kiroTab = page.locator('a', { hasText: 'Tudo sobre Kiro' });
    await kiroTab.click();
    console.log("Clicked Kiro Tab.");
    
    await page.waitForTimeout(2000); // wait for render
    
    const containerHtml = await page.evaluate(() => {
        const c = document.getElementById('kiro-doc-view');
        return c ? c.innerHTML : 'NOT FOUND';
    });
    
    const fs = require('fs');
    fs.writeFileSync('dump.html', containerHtml);
    console.log("Dumped HTML to dump.html. Length:", containerHtml.length);
    
  } catch (error) {
    console.error("TEST FAILED:", error);
  } finally {
    await browser.close();
  }
})();
