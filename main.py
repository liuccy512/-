import requests
import os
import json

def get_gold_price():
    # 爬取上金所数据（此处使用示例接口，实际建议寻找稳定API）
    url = "https://puser.sge.com.cn/sge-open/api/hq/getRealTimeHq"
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        # 寻找 Au99.99 的数据
        for item in data:
            if item['instId'] == 'Au99.99':
                return item
    except Exception as e:
        print(f"抓取失败: {e}")
    return None

def send_wechat(item):
    webhook = os.environ.get("WECHAT_WEBHOOK")
    if not webhook:
        print("未配置 Webhook")
        return

    content = f"### 💰 实时金价提醒\n" \
              f"> **品种**：<font color=\"info\">{item['instId']}</font>\n" \
              f"> **现价**：<font color=\"warning\">{item['last']} 元/克</font>\n" \
              f"> **涨跌**：{item['upDown']}\n" \
              f"> **更新时间**：{item['time']}"

    requests.post(webhook, json={"msgtype": "markdown", "markdown": {"content": content}})

if __name__ == "__main__":
    result = get_gold_price()
    if result:
        send_wechat(result)
