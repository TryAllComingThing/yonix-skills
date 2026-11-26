from playwright.sync_api import sync_playwright
from pathlib import Path
p=Path(__file__).with_name('index.html')
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1280,'height':800})
 page.set_content(p.read_text(encoding="utf-8"))
 def row(id):return page.locator(f'tr[data-id="{id}"]')
 assert row('dev-001').count()==1
 page.locator('#create').click();page.locator('#name').fill('测试设备 C');page.locator('#save').click();assert row('dev-003').count()==1
 row('dev-003').locator('[data-action="edit"]').click();page.locator('#name').fill('临时值');page.locator('#cancel').click();assert '测试设备 C' in row('dev-003').inner_text()
 row('dev-003').locator('[data-action="edit"]').click();page.locator('#name').fill('设备 C 新名');page.locator('#save').click();assert '设备 C 新名' in row('dev-003').inner_text()
 row('dev-001').locator('[data-action="delete"]').click();assert '仍被工单引用' in page.locator('#feedback').inner_text()
 row('dev-003').locator('[data-action="publish"]').click();assert page.evaluate('mockTest.getPublished().name')=='设备 C 新名'
 row('dev-003').locator('[data-action="edit"]').click();page.locator('#name').fill('设备 C 草稿');page.locator('#save').click();assert page.evaluate('mockTest.getPublished().name')=='设备 C 新名'
 page.locator('#search').fill('不存在');assert '暂无数据' in page.locator('#rows').inner_text();page.locator('#reset').click();assert row('dev-003').count()==1
 page.evaluate('mockTest.setFailure(true)');row('dev-003').locator('[data-action="edit"]').click();page.locator('#name').fill('错误保存');page.locator('#save').click();assert '模拟保存失败' in page.locator('#feedback').inner_text();page.locator('#cancel').click()
 page.locator('#restore').click();assert row('dev-003').count()==0 and page.evaluate('mockTest.getPublished()') is None
 page.screenshot(path=str(Path(__file__).with_name('browser-evidence.png')),full_page=True)
 print('PASS: 8 browser scenarios; screenshot browser-evidence.png')
 b.close()
