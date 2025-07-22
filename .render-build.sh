#!/usr/bin/env bash
# 安装 Node.js 的依赖（确保 playwright 被正确安装）
echo "Installing npm dependencies..."
npm install

# 安装 Playwright 浏览器（带依赖）
echo "Installing Playwright browsers..."
npx playwright install --with-deps