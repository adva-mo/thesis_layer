#!/usr/bin/env node
/**
 * Generate a clean PDF from an HTML file.
 * No headers, no footers, no file path, no timestamps.
 *
 * Usage: node scripts/generate/pdf.js <input.html> [output.pdf]
 *
 * If output.pdf is omitted, replaces the .html extension with .pdf.
 */

const puppeteer = require('/Users/adva/.npm/_npx/55158e48eb5c59f7/node_modules/puppeteer');
const path = require('path');
const fs = require('fs');

async function run() {
  const [, , htmlArg, pdfArg] = process.argv;

  if (!htmlArg) {
    console.error('Usage: node scripts/generate/pdf.js <input.html> [output.pdf]');
    process.exit(1);
  }

  const htmlPath = path.resolve(htmlArg);
  const pdfPath = pdfArg
    ? path.resolve(pdfArg)
    : htmlPath.replace(/\.html$/, '.pdf');

  if (!fs.existsSync(htmlPath)) {
    console.error(`File not found: ${htmlPath}`);
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0', timeout: 30000 });

  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: false,
    margin: { top: '14mm', bottom: '14mm', left: '18mm', right: '18mm' },
  });

  await browser.close();
  console.log(`PDF written → ${pdfPath}`);
}

run().catch((err) => { console.error(err); process.exit(1); });
