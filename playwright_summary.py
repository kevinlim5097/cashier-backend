import asyncio
from playwright.async_api import async_playwright

async def fetch_summary():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Step 1: 登录页面
            await page.goto("https://kybio.pospal-global.com/account/SignIn?noLog=")
            await page.fill('#txt_userName', "boampang")
            await page.fill('#txt_password', "150722")
            await page.click('#longinSubmit')

            # 等待跳转完成
            await page.wait_for_load_state("networkidle")

            # Step 2: 打开 Summary 页面
            await page.goto("https://kybio.pospal-global.com/Report/BusinessSummaryV2")
            await page.wait_for_selector('#mainArea', timeout=8000)

            # Step 3: 抓取数据
            sales_amount = await page.locator('#mainTable > tbody > tr.ticketReport > td.profile > div > span:nth-child(1)').inner_text()
            profit_amount = await page.locator('#mainTable > tbody > tr.ticketReport > td.profile > div > span:nth-child(2)').inner_text()
            tng = await page.locator('#mainTable > tbody > tr.ticketReport > td:nth-child(6) > span').inner_text()
            cash = await page.locator('#mainTable > tbody > tr.ticketReport > td:nth-child(3) > span').inner_text()

            return {
                "Sales Amount": sales_amount.strip(),
                "Profit Amount": profit_amount.strip(),
                "TNG": tng.strip(),
                "Cash": cash.strip()
            }

        except Exception as e:
            return {"error": str(e)}
        finally:
            await browser.close()

# 测试时本地运行
if __name__ == "__main__":
    result = asyncio.run(fetch_summary())
    print(result)
