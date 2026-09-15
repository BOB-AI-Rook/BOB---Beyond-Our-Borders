const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({ viewport: { width: 1024, height: 1536 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/bob-poster.html');
  await p.waitForTimeout(600);
  await p.locator('#poster').screenshot({ path: 'bob-poster.png' });
  await b.close();
})();
