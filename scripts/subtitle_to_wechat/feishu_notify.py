#!/usr/bin/env python3
"""
将文章摘要推送到飞书群。

用法：
    python3 feishu_notify.py content.json

content.json 中需包含 title 和 key_points 字段。
"""

import json
import sys
import urllib.request

WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/a91e9058-32c8-4232-91b8-5620af17aa87"


def send_to_feishu(title, key_points):
    """推送文章摘要到飞书群。"""
    content = [[{"tag": "text", "text": title, "style": ["bold"]}]]
    content.append([{"tag": "text", "text": "\n\U0001f4cb 要点摘录："}])
    for i, point in enumerate(key_points[:5], 1):
        content.append([{"tag": "text", "text": f"\n{i}. {point}"}])
    content.append([{"tag": "text", "text": "\n\n\u2705 完整文稿已生成，请查看文档。"}])

    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "\U0001f4dd 新文稿编译完成",
                    "content": content
                }
            }
        }
    }

    req = urllib.request.Request(
        WEBHOOK_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        print(f"[OK] 飞书推送成功: {result}")
        return True
    except Exception as e:
        print(f"[WARN] 飞书推送失败: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python3 feishu_notify.py content.json")
        sys.exit(1)

    json_path = sys.argv[1]
    with open(json_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    title = content.get("title", "未命名文稿")
    key_points = content.get("key_points", [])

    success = send_to_feishu(title, key_points)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
