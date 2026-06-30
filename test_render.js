const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('c:/Users/User/.antigravity/Agile Coach AI/index.html', 'utf8');
const fluxoIa = fs.readFileSync('c:/Users/User/.antigravity/Agile Coach AI/fluxo_ia.js', 'utf8');
const app = fs.readFileSync('c:/Users/User/.antigravity/Agile Coach AI/app.js', 'utf8');

const dom = new JSDOM(html, { runScripts: "dangerously" });

// Manually evaluate the scripts
try {
  dom.window.eval(fluxoIa);
  console.log("fluxo_ia.js evaluated successfully");
} catch (e) {
  console.error("Error evaluating fluxo_ia.js:", e);
}

try {
  dom.window.eval(app);
  console.log("app.js evaluated successfully");
} catch (e) {
  console.error("Error evaluating app.js:", e);
}

// Trigger DOMContentLoaded
dom.window.document.dispatchEvent(new dom.window.Event("DOMContentLoaded"));

// Check if container has content
const container = dom.window.document.getElementById('fluxo-ia-view');
if (container && container.innerHTML.trim().length > 0) {
  console.log("Container is populated! Length:", container.innerHTML.length);
} else {
  console.log("Container is EMPTY!");
}
