"""
极致了 API 独立脚本
依赖：pip install requests
运行：python3 run.py
"""
import json
import requests

# ── 配置区（按需修改）────────────────────────────────────────────────────
API_KEY      = "JZL95ad9ef74f4d8371"
VERIFYCODE   = "syqabcd"
BASE_URL     = "https://www.dajiala.com"
TIMEOUT      = 30
# ─────────────────────────────────────────────────────────────────────────


def post(path, payload=None):
    if payload is None:
        payload = {}
    payload.update({"key": API_KEY, "verifycode": VERIFYCODE})
    resp = requests.post(BASE_URL + path, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def get(path, params=None):
    if params is None:
        params = {}
    params.update({"key": API_KEY, "verifycode": VERIFYCODE})
    resp = requests.get(BASE_URL + path, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def pp(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ── 在下面选择要调用的接口，取消对应注释即可 ──────────────────────────────

# 1. 查询账户余额（免费）
result = post("/fbmain/monitor/v3/get_remain_money")
pp(result)

# 2. 关键词搜索文章（0.02元/条）
# result = post("/fbmain/monitor/v3/kw_search", {
#     "kw": "人工智能",   # 搜索关键词
#     "period": 7,        # 最近7天
#     "mode": 1,          # 1=搜标题
#     "sort_type": 1,     # 1=按阅读数
#     "page": 1,
# })
# pp(result)

# 3. 公众号历史文章（0.06元/次）
# result = get("/fbmain/monitor/v3/post_history", {
#     "account": "人民日报",
#     "page": 1,
# })
# pp(result)

# 4. 文章阅读/点赞数（0.04元/次）
# result = get("/fbmain/monitor/v3/read_zan", {
#     "url": "https://mp.weixin.qq.com/s/xxxxxxxx",
# })
# pp(result)
