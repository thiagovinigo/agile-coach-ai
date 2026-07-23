const fs = require('fs');
const { JSDOM } = require('jsdom');

const content = fs.readFileSync('kiro_doc.js', 'utf8');
const match = content.match(/container\.innerHTML\s*=\s*`([\s\S]*?)`;/);
if (!match) {
    console.error("Could not extract HTML string");
    process.exit(1);
}

const html = match[1];
const dom = new JSDOM(html);
const document = dom.window.document;

const simCard = document.getElementById('sim-card');
console.log("sim-card found:", !!simCard);

const tags = document.getElementById('sim-tags');
console.log("sim-tags found:", !!tags);

const btnNext = document.getElementById('btn-kiro-next');
console.log("btnNext found:", !!btnNext);

if (!simCard) {
    console.log("sim-card is null. Let's see what is inside sim-board:");
    const board = document.getElementById('sim-board');
    if (board) {
        console.log(board.innerHTML);
    } else {
        console.log("sim-board is also null");
    }
}
