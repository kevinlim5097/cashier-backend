import requests
import asyncio

from playwright_summary import fetch_summary
from flask import Flask, render_template, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许前端访问

@app.route("/")
def index():
    return "Backend is working!"

@app.route("/run-playwright")
def run_playwright():
    try:
        result = asyncio.run(fetch_summary())
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/get-cashier-data")
def get_cashier_data():
    login_url = "https://kybio.pospal-global.com/account/SignIn?noLog="
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": login_url
    }

    payload = {
        "userName": "boampang",
        "password": "150722"
    }

    session = requests.Session()
    login_resp = session.post(login_url, data=payload, headers=headers)

    if login_resp.status_code != 200:
        return jsonify({"error": "Login failed"}), 401

    # 📄 抓取 Summary 页面 HTML
    summary_url = "https://kybio.pospal-global.com/Report/BusinessSummaryV2"
    html_resp = session.get(summary_url)

    if html_resp.status_code != 200:
        return jsonify({"error": "Failed to load summary HTML"}), 500

    soup = BeautifulSoup(html_resp.text, "html.parser")

    def get_span_value(show_name, data_key=None):
        selector = f'span[data-show-name="{show_name}"]'
        if data_key:
            selector += f'[data="{data_key}"]'
        span = soup.select_one(selector)
        return span.text.strip() if span else "N/A"

    result_data = {
        "Sales Amount": get_span_value("Item Sales", "totalAmount"),
        "Profit Amount": get_span_value("Gross margin", "totalProfit"),
        "TNG": get_span_value("TNG"),
        "Cash": get_span_value("现金支付")
    }

    return jsonify(result_data)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
