"""
临时脚本：对 9 个关键词跑一次专项搜索（过去7天）
"""
import csv
import sys
import time
from datetime import datetime
from pathlib import Path

from config import API_KEY, API_ADDON, USE_LONG_LINK, REQUEST_TIMEOUT
from jizhi_api import JiZhiClient

KEYWORDS = [
    "锦秋基金",
    "宇树科技 Unitree Robotics",
    "Momenta",
    "数美万物 Shumei",
    "地瓜机器人 Digua Robotics",
    "生数科技 Shengshu Tech",
    "星尘智能 Stardust Intelligence",
    "Pokee AI",
    "Aha AI",
]

PERIOD = 7
MAX_PAGES = 5
SORT_TYPE = 2
MODE = 1
REQUEST_DELAY = 0.5

CSV_COLUMNS = [
    "search_keyword", "title", "wx_name", "wx_id",
    "publish_time_str", "read", "praise", "looking",
    "ip_wording", "classify", "is_original", "url", "short_link",
]


def fetch_all_pages(client, keyword):
    all_articles = []
    for page in range(1, MAX_PAGES + 1):
        try:
            resp = client.search_article_by_keyword(
                kw=keyword, period=PERIOD,
                sort_type=SORT_TYPE, mode=MODE, page=page,
            )
        except Exception as e:
            print(f"    [ERROR] 第{page}页请求失败: {e}", file=sys.stderr)
            break

        if resp.get("code", -1) != 0:
            print(f"    [WARN] code={resp.get('code')}, msg={resp.get('msg', '')}")
            break

        data = resp.get("data", [])
        if not data:
            break

        all_articles.extend(data)
        total_pages = resp.get("total_page", 1)
        print(
            f"    第{page}/{min(total_pages, MAX_PAGES)}页 | "
            f"{len(data):3d}条 | 累计{len(all_articles):4d}条 | "
            f"总共{resp.get('total', 0)}条 | 花费¥{resp.get('cost_money', 0):.2f}"
        )

        if page >= total_pages or page >= MAX_PAGES:
            break
        time.sleep(REQUEST_DELAY)

    return all_articles


def main():
    print("=" * 60)
    print(f"  专项监控 | {len(KEYWORDS)} 个关键词 | 过去 {PERIOD} 天")
    print("=" * 60)

    client = JiZhiClient(
        key=API_KEY, addon=API_ADDON,
        use_long_link=USE_LONG_LINK, timeout=REQUEST_TIMEOUT,
    )

    all_rows = []
    run_start = datetime.now()

    for i, keyword in enumerate(KEYWORDS, 1):
        print(f"\n[{i}/{len(KEYWORDS)}] {keyword}")
        articles = fetch_all_pages(client, keyword)
        if not articles:
            print("    (无结果)")
            time.sleep(REQUEST_DELAY)
            continue
        for art in articles:
            row = {col: art.get(col, "") for col in CSV_COLUMNS}
            row["search_keyword"] = keyword
            all_rows.append(row)
        print(f"    => 本词合计 {len(articles)} 条")
        time.sleep(REQUEST_DELAY)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    ts = run_start.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"adhoc_9kw_{ts}.csv"

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)

    elapsed = (datetime.now() - run_start).seconds
    print(f"\n{'=' * 60}")
    print(f"  完成！共 {len(all_rows)} 条文章")
    print(f"  耗时: {elapsed // 60}分{elapsed % 60}秒")
    print(f"  输出: {output_path.resolve()}")
    print("=" * 60)

    # ── 打印可读摘要（贴到对话框用）─────────────────────────────
    print(f"\n📋 结果摘要（过去 {PERIOD} 天）\n")
    for kw in KEYWORDS:
        kw_rows = [r for r in all_rows if r["search_keyword"] == kw]
        print(f"【{kw}】{len(kw_rows)} 篇")
        for r in kw_rows:
            date = r.get("publish_time_str", "")[:10]
            title = r.get("title", "").strip()[:40]
            source = r.get("wx_name", "").strip()[:15]
            read = r.get("read", "")
            url = r.get("url", "").strip()
            print(f"  {date}  {source}  阅读{read}  {title}")
            print(f"         {url}")
        if not kw_rows:
            print("  （无结果）")
        print()


if __name__ == "__main__":
    main()
