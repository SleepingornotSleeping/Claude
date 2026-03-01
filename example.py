"""
极致了 API 使用示例
运行前请确认已安装依赖:  pip install requests
"""
import json
from config import API_KEY, API_ADDON, USE_LONG_LINK, REQUEST_TIMEOUT
from jizhi_api import JiZhiClient


def pp(data: dict) -> None:
    """美化打印 JSON 结果。"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    client = JiZhiClient(
        key=API_KEY,
        addon=API_ADDON,
        use_long_link=USE_LONG_LINK,
        timeout=REQUEST_TIMEOUT,
    )

    # ── 1. 查询账户余额（免费）──────────────────────────────────────────
    print("=" * 60)
    print("1. 查询账户余额")
    result = client.get_remain_money()
    pp(result)

    # ── 2. 获取公众号历史文章列表（0.06元/次）──────────────────────────
    # print("=" * 60)
    # print("2. 公众号历史文章列表")
    # result = client.get_post_history("人民日报", page=1)
    # pp(result)

    # ── 3. 获取文章阅读/点赞数（0.04元/次）────────────────────────────
    # print("=" * 60)
    # print("3. 文章阅读数")
    # article_url = "https://mp.weixin.qq.com/s/xxxxxxxx"
    # result = client.get_read_zan(article_url)
    # pp(result)

    # ── 4. 获取文章详情（0.03元/次）───────────────────────────────────
    # print("=" * 60)
    # print("4. 文章详情")
    # article_url = "https://mp.weixin.qq.com/s/xxxxxxxx"
    # result = client.get_article_detail(article_url)
    # pp(result)

    # ── 5. 关键词搜索文章（0.02元/条）─────────────────────────────────
    # print("=" * 60)
    # print("5. 关键词搜索文章")
    # result = client.search_article_by_keyword(kw="人工智能", period=7, page=1)
    # pp(result)
    #
    # # 多条件搜索示例：标题含"AI"且不含"广告"，按时间排序，最近30天
    # result = client.search_article_by_keyword(kw="AI", ex_kw="广告", period=30, sort_type=2, mode=1)
    # pp(result)

    # ── 6. 获取视频号作品列表（0.2元/次）──────────────────────────────
    # print("=" * 60)
    # print("6. 视频号作品列表")
    # result = client.get_wxvideo_list("sph_xxxxx", page=1)
    # pp(result)

    # ── 7. 搜一搜实时搜文章（0.5元/次）────────────────────────────────
    # print("=" * 60)
    # print("7. 搜一搜文章")
    # result = client.web_search("ChatGPT", mode=1)
    # pp(result)

    # ── 8. 公众号爆文API（0.02元/条）──────────────────────────────────
    # print("=" * 60)
    # print("8. 公众号爆文")
    # result = client.get_hot_articles("AI", page=1)
    # pp(result)

    print("=" * 60)
    print("示例运行完成。取消注释上方代码块以调用更多接口。")


if __name__ == "__main__":
    main()
