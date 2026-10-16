// 輕量檢查：manifest 格式、內嵌 JS 語法、頁面載入無 console 錯誤。
// 用法：node scripts/check.mjs
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import vm from 'node:vm';

let failed = false;
const fail = (m) => { console.error('FAIL', m); failed = true; };
const ok = (m) => console.log('OK  ', m);

// 1. manifest.json
try {
  const m = JSON.parse(readFileSync('manifest.json', 'utf8'));
  for (const k of ['name', 'start_url', 'icons']) if (!m[k]) fail(`manifest 缺少 ${k}`);
  ok('manifest.json 是合法 JSON');
} catch (e) { fail(`manifest.json: ${e.message}`); }

// 2. index.html 內嵌 <script> 語法
const html = readFileSync('index.html', 'utf8');
const inline = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)];
inline.forEach((s, i) => {
  try { new vm.Script(s[1]); ok(`內嵌 script #${i + 1} 語法正確`); }
  catch (e) { fail(`內嵌 script #${i + 1}: ${e.message}`); }
});

// 3. Playwright 開頁面，收集 console 錯誤（忽略外部 CDN 載入失敗）
let chromium;
try {
  const root = execFileSync('npm', ['root', '-g']).toString().trim();
  ({ chromium } = createRequire(root + '/')('playwright'));
} catch { console.log('SKIP Playwright 未安裝，略過頁面檢查'); }
if (chromium) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => {
    if (m.type() === 'error' && !/Failed to load resource|net::ERR/.test(m.text())) errors.push(m.text());
  });
  await page.goto(pathToFileURL('index.html').href, { waitUntil: 'load' }).catch((e) => errors.push(e.message));
  await browser.close();
  errors.length ? errors.forEach((e) => fail(`頁面錯誤: ${e}`)) : ok('頁面載入無 console 錯誤');
}

process.exit(failed ? 1 : 0);
