const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    console.log("Navigating to local server...");
    await page.goto(`file://${process.cwd()}/index.html`);
    
    console.log("Waiting for Kiro Doc Tab...");
    const kiroTab = page.locator('a', { hasText: 'Tudo sobre Kiro' });
    await kiroTab.click();
    console.log("Clicked Kiro Tab.");
    
    console.log("Waiting for Simulator Button...");
    const nextBtn = page.locator('#btn-kiro-next');
    await nextBtn.waitFor({ state: 'visible', timeout: 5000 });
    console.log("Found Next Button!");
    
    console.log("Checking initial position...");
    const simCard = page.locator('#sim-card');
    await simCard.waitFor({ state: 'visible' });
    const initialBox = await simCard.boundingBox();
    console.log("Initial Card position:", initialBox);
    
    console.log("Clicking Next Step...");
    await page.evaluate(() => document.getElementById('btn-kiro-next').click());
    
    console.log("Waiting for transition timeout...");
    await page.waitForTimeout(1000); // wait for transition
    
    console.log("Getting second box...");
    
    const secondBox = await simCard.boundingBox();
    console.log("Card position after 1 click:", secondBox);
    if (secondBox.x > initialBox.x) {
        console.log("SUCCESS: Card moved to the right!");
    } else {
        console.log("ERROR: Card did not move!");
    }
    
    console.log("Waiting for PRD tag...");
    const prdTag = page.locator('span.tfs-tag', { hasText: 'PRD' });
    await prdTag.waitFor({ state: 'visible' });
    console.log("PRD tag found! Clicking it...");
    await prdTag.click();
    
    console.log("Checking Modal...");
    const modalTitle = page.locator('#sim-modal-title');
    await modalTitle.waitFor({ state: 'visible' });
    const titleText = await modalTitle.textContent();
    console.log("Modal opened successfully with title:", titleText);
    
    console.log("ALL TESTS PASSED.");
    
  } catch (error) {
    console.error("TEST FAILED:", error);
  } finally {
    await browser.close();
  }
})();
