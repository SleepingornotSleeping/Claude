"""
关键词监控脚本 - monitor.py

搜索指定关键词在过去一段时间内的微信文章，并输出到 CSV 文件。

用法：
    python monitor.py                    # 默认：过去 7 天
    python monitor.py --period 14        # 过去 2 周
    python monitor.py --period 30        # 过去 1 个月
    python monitor.py --dry-run          # 仅显示配置和费用估算，不调用 API
    python monitor.py --period 14 --max-pages 3   # 自定义页数上限
"""

import argparse
import csv
import sys
import time
from datetime import datetime
from pathlib import Path

from config import API_KEY, API_ADDON, USE_LONG_LINK, REQUEST_TIMEOUT
from jizhi_api import JiZhiClient

# ─────────────────────────────────────────────────────────────────────────────
# 监控关键词列表（共 70 个）
# ─────────────────────────────────────────────────────────────────────────────
KEYWORDS = [
    "锦秋基金",
    "锦秋基金 杨洁",
    "锦秋基金 臧天宇",
    "宇树科技 Unitree Robotics",
    "宇树科技 Unitree Robotics 王兴兴",
    "Momenta",
    "Momenta 曹旭东",
    "数美万物 Shumei",
    "数美万物 Shumei 任利锋",
    "地瓜机器人 Digua Robotics",
    "地瓜机器人 Digua Robotics 余凯",
    "地瓜机器人 Digua Robotics 王丛",
    "乐享科技 Lexiang Tech",
    "乐享科技 Lexiang Tech 郭人杰",
    "生数科技 Shengshu Tech",
    "生数科技 Shengshu Tech 朱军",
    "首形科技 Shouxing Tech",
    "首形科技 Shouxing Tech 胡宇航",
    "OiiOii",
    "OiiOii 闹闹",
    "造梦次元 Zaomeng",
    "造梦次元 Zaomeng 沈洽金",
    "星尘智能 Stardust Intelligence",
    "星尘智能 Stardust Intelligence 来杰",
    "Pokee AI",
    "Pokee AI 朱哲清",
    "铭芯启睿",
    "铭芯启睿 Mingxin 刘琦",
    "因克斯 Encos",
    "因克斯 Encos 祝宗煌",
    "独响",
    "独响 Duxiang 王登科",
    "Aha AI",
    "Aha AI Kay Feng",
    "清闲智能",
    "清闲智能 阎乐",
    "微纳核芯 WeNano",
    "微纳核芯 WeNano 叶乐",
    "深度原理 Deep Principle",
    "深度原理 Deep Principle 贾皓钧",
    "深度原理 Deep Principle 段辰儒",
    "光本位 Photonic Base",
    "光本位 程唐盛",
    "光本位 熊胤江",
    "澜昆微 Lankun Micro",
    "澜昆微 祁楠",
    "流形空间 Manifold AI",
    "流形空间 Manifold 武伟",
    "灵启万物",
    "灵启万物 朱庆旭",
    "灵动佳芯",
    "灵动佳芯 关赛新",
    "PongBot庞伯特",
    "PongBot庞伯特 张海波",
    "FastMoss 史文禄",
    "atoms.dev",
    "atoms.dev 吴承霖",
    "MetaGPT 吴承霖",
    "DeepWisdom 吴承霖",
    "Agile Flight 张富",
    "Wanaka 张阳",
    "猴子说话 雷圳鹏",
    "文图跃迁 刘荣名",
    "新控智能 许建平",
    "昌进生物 骆滨",
    "疆海科技 刘兵斌",
    "大秦数能 柳扬",
    "Leonis Capital",
    "奇妙拉比",
]

# ─────────────────────────────────────────────────────────────────────────────
# 默认配置
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_PERIOD = 7      # 时间范围（天）
DEFAULT_MAX_PAGES = 5   # 每个关键词最多抓取页数（每页 20 条）
SORT_TYPE = 2           # 1=按阅读数排序  2=按发布时间排序
MODE = 1                # 1=搜标题  2=搜正文  3=标题+正文
REQUEST_DELAY = 0.5     # 每次请求间隔（秒）

# CSV 输出字段顺序
CSV_COLUMNS = [
    "search_keyword",
    "title",
    "wx_name",
    "wx_id",
    "publish_time_str",
    "read",
    "praise",
    "looking",
    "ip_wording",
    "classify",
    "is_original",
    "url",
    "short_link",
]


# ─────────────────────────────────────────────────────────────────────────────
# 核心函数
# ─────────────────────────────────────────────────────────────────────────────

def fetch_all_pages(client: JiZhiClient, keyword: str, period: int, max_pages: int) -> list:
    """抓取某关键词的全部结果，最多 max_pages 页。"""
    all_articles = []
    for page in range(1, max_pages + 1):
        try:
            resp = client.search_article_by_keyword(
                kw=keyword,
                period=period,
                sort_type=SORT_TYPE,
                mode=MODE,
                page=page,
            )
        except Exception as e:
            print(f"    [ERROR] 第{page}页请求失败: {e}", file=sys.stderr)
            break

        code = resp.get("code", -1)
        if code != 0:
            print(f"    [WARN] API 返回非0: code={code}, msg={resp.get('msg', '')}")
            break

        data = resp.get("data", [])
        if not data:
            break

        all_articles.extend(data)

        total = resp.get("total", 0)
        total_pages = resp.get("total_page", 1)
        cost = resp.get("cost_money", 0)
        print(
            f"    第{page}/{min(total_pages, max_pages)}页 | "
            f"{len(data):3d}条 | 累计{len(all_articles):4d}条 | "
            f"总共{total}条 | 花费¥{cost:.2f}"
        )

        if page >= total_pages or page >= max_pages:
            break

        time.sleep(REQUEST_DELAY)

    return all_articles


def save_csv(rows: list, output_path: Path) -> None:
    """将结果写入 CSV（UTF-8 with BOM，Excel 可直接打开）。"""
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


# ─────────────────────────────────────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="微信公众号关键词监控脚本，结果输出为 CSV。"
    )
    parser.add_argument(
        "--period", type=int, default=DEFAULT_PERIOD,
        choices=[7, 14, 30],
        help="监控时间范围（天）：7=1周，14=2周，30=1个月，默认 %(default)s",
    )
    parser.add_argument(
        "--max-pages", type=int, default=DEFAULT_MAX_PAGES,
        help=f"每个关键词最多抓取页数（每页20条），默认 %(default)s",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="仅显示配置和费用估算，不实际调用 API",
    )
    args = parser.parse_args()

    period = args.period
    max_pages = args.max_pages
    dry_run = args.dry_run

    period_label = {7: "1周 (7天)", 14: "2周 (14天)", 30: "1个月 (30天)"}.get(
        period, f"{period}天"
    )
    max_cost = len(KEYWORDS) * max_pages * 20 * 0.02

    print("=" * 65)
    print("  微信公众号关键词监控脚本")
    print("=" * 65)
    print(f"  关键词数量  : {len(KEYWORDS)} 个")
    print(f"  监控范围    : 过去 {period_label}")
    print(f"  最大页数    : {max_pages} 页/词（最多 {max_pages * 20} 条/词）")
    print(f"  费用上限估算: ¥{max_cost:.2f}（实际按有结果条数计算）")
    print("=" * 65)

    if dry_run:
        print("\n[dry-run 模式] 仅列出关键词，不调用 API：\n")
        for i, kw in enumerate(KEYWORDS, 1):
            print(f"  {i:3d}. {kw}")
        print(f"\n共 {len(KEYWORDS)} 个关键词。")
        return

    client = JiZhiClient(
        key=API_KEY,
        addon=API_ADDON,
        use_long_link=USE_LONG_LINK,
        timeout=REQUEST_TIMEOUT,
    )

    all_rows = []
    keywords_with_results = 0
    run_start = datetime.now()

    for i, keyword in enumerate(KEYWORDS, 1):
        print(f"\n[{i:3d}/{len(KEYWORDS)}] {keyword}")
        articles = fetch_all_pages(client, keyword, period, max_pages)

        if not articles:
            print("    (无结果)")
            time.sleep(REQUEST_DELAY)
            continue

        keywords_with_results += 1
        for art in articles:
            row = {col: art.get(col, "") for col in CSV_COLUMNS}
            row["search_keyword"] = keyword
            all_rows.append(row)

        print(f"    => 本词合计 {len(articles)} 条")
        time.sleep(REQUEST_DELAY)

    # ── 保存结果 ────────────────────────────────────────────────────────────
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    timestamp = run_start.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"monitor_{period}d_{timestamp}.csv"
    save_csv(all_rows, output_path)

    elapsed = (datetime.now() - run_start).seconds
    print(f"\n{'=' * 65}")
    print(f"  完成！")
    print(f"  有结果的关键词 : {keywords_with_results} / {len(KEYWORDS)}")
    print(f"  总文章数       : {len(all_rows)} 条")
    print(f"  耗时           : {elapsed // 60}分{elapsed % 60}秒")
    print(f"  输出文件       : {output_path.resolve()}")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    main()
