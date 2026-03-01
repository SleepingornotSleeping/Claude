"""
极致了 (JiZhiLe) API 客户端
文档参考: https://www.jizhi.vip
"""

import requests
from typing import Optional, Dict, Any


class JiZhiClient:
    """极致了API客户端，封装所有接口调用。"""

    LONG_BASE_URL = "https://www.jizhi.vip"   # 长链接（推荐）
    SHORT_BASE_URL = "https://jzl.wiki"        # 短链接（备用，有一定延迟）

    def __init__(self, key: str, addon: str, use_long_link: bool = True, timeout: int = 30):
        """
        初始化客户端。

        Args:
            key:           API Key，例如 'JZL95ad9ef74f4d8371'
            addon:         附加码，例如 'syqabcd'
            use_long_link: 是否使用长链接（推荐），默认 True
            timeout:       请求超时秒数，默认 30
        """
        self.key = key
        self.addon = addon
        self.base_url = self.LONG_BASE_URL if use_long_link else self.SHORT_BASE_URL
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    # ------------------------------------------------------------------ #
    #  内部工具方法
    # ------------------------------------------------------------------ #

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict:
        payload.update({"key": self.key, "addon": self.addon})
        url = self.base_url + path
        resp = self.session.post(url, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def _get(self, path: str, params: Dict[str, Any]) -> Dict:
        params.update({"key": self.key, "addon": self.addon})
        url = self.base_url + path
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------ #
    #  账户信息
    # ------------------------------------------------------------------ #

    def get_remain_money(self) -> Dict:
        """获取当前账户余额（免费）。"""
        return self._post("/fbmain/monitor/v3/get_remain_money", {})

    # ------------------------------------------------------------------ #
    #  视频号相关接口
    # ------------------------------------------------------------------ #

    def get_wxvideo_list(self, finder_username: str, page: int = 1) -> Dict:
        """获取单个视频号作品列表（链接不可下载，可翻页）。0.2元/次"""
        return self._post("/fbmain/monitor/v3/wxvideo", {
            "type": "get_video_list",
            "finder_username": finder_username,
            "page": page,
        })

    def get_wxvideo_live_replay(self, finder_username: str, page: int = 1) -> Dict:
        """获取视频号直播回放记录（实时数据，可翻页）。0.2元/次"""
        return self._post("/fbmain/monitor/v3/wxvideo", {
            "type": "get_live_replay",
            "finder_username": finder_username,
            "page": page,
        })

    def get_wxvideo_interact(self, object_id: str) -> Dict:
        """获取视频号视频点赞、阅读等互动信息。0.05元/次"""
        return self._post("/fbmain/monitor/v3/wxvideo", {
            "type": "get_video_like",
            "object_id": object_id,
        })

    def get_wxvideo_comment(self, object_id: str) -> Dict:
        """获取视频号视频评论。0.05元/次"""
        return self._post("/fbmain/monitor/v3/wxvideo", {
            "type": "get_comment",
            "object_id": object_id,
        })

    def get_wxvideo_download_url(self, object_id: str) -> Dict:
        """获取视频可下载链接。0.2元/次"""
        return self._post("/fbmain/monitor/v3/wxvideo", {
            "type": "get_video_url",
            "object_id": object_id,
        })

    def export_id_to_object_id(self, export_id: str) -> Dict:
        """export_id 转 object_id。0.05元/次"""
        return self._post("/fbmain/monitor/v3/wxvideo", {
            "type": "export_id_to_object_id",
            "export_id": export_id,
        })

    def search_video(self, keyword: str, mode: int = 1) -> Dict:
        """搜一搜 搜视频。mode=1: 0.5元/次；mode=2: 1.0元/次"""
        return self._post("/fbmain/monitor/v3/web_search", {
            "type": "search_video",
            "keyword": keyword,
            "mode": mode,
        })

    def search_video_account(self, keyword: str, mode: int = 1) -> Dict:
        """搜一搜 搜视频账号。mode=1: 0.5元/次；mode=2: 1.0元/次"""
        return self._post("/fbmain/monitor/v3/web_search", {
            "type": "search_video_account",
            "keyword": keyword,
            "mode": mode,
        })

    def search_wxvideo_by_keyword(self, keyword: str) -> Dict:
        """关键词搜索视频号。0.5元/次"""
        return self._post("/fbmain/monitor/v3/wxvideo", {
            "type": "search_finder",
            "keyword": keyword,
        })

    def get_wxvideo_info(self, finder_username: str) -> Dict:
        """获取指定视频号信息。0.2元/次"""
        return self._post("/fbmain/monitor/v3/wxvideo", {
            "type": "get_finder_info",
            "finder_username": finder_username,
        })

    def get_wxvideo_by_ghid(self, ghid: str) -> Dict:
        """通过公众号原始id获取绑定的视频号。0.5元/次起"""
        return self._post("/fbmain/monitor/v3/history_by_ghid", {
            "type": "get_finder_by_ghid",
            "ghid": ghid,
        })

    # ------------------------------------------------------------------ #
    #  公众号历史文章列表
    # ------------------------------------------------------------------ #

    def get_post_history(self, account: str, page: int = 1) -> Dict:
        """通过公众号名称/微信ID/链接获取历史发文列表。0.06元/次起"""
        return self._get("/fbmain/monitor/v3/post_history", {
            "account": account,
            "page": page,
        })

    def get_post_today(self, account: str) -> Dict:
        """获取公众号当天发文情况。0.06元/次起"""
        return self._get("/fbmain/monitor/v3/post_condition", {
            "account": account,
        })

    def get_history_by_ghid(self, ghid: str, page: int = 1) -> Dict:
        """通过公众号原始id获取历史列表（针对无法搜索账号）。0.2元/次起"""
        return self._get("/fbmain/monitor/v3/post_condition", {
            "ghid": ghid,
            "page": page,
        })

    # ------------------------------------------------------------------ #
    #  文章阅读数/互动数
    # ------------------------------------------------------------------ #

    def get_read_zan(self, url: str) -> Dict:
        """获取文章阅读数、点赞数与在看数。0.04元/次"""
        return self._get("/fbmain/monitor/v3/read_zan", {"url": url})

    def get_read_zan_pro(self, url: str) -> Dict:
        """获取文章阅读、点赞、在看、转发、收藏、评论数。0.06元/次"""
        return self._get("/fbmain/monitor/v3/read_zan_pro", {"url": url})

    def convert_link(self, url: str) -> Dict:
        """公众号文章链接长短互转。0.02元/次"""
        return self._get("/fbmain/monitor/v3/link/short2long", {"url": url})

    # ------------------------------------------------------------------ #
    #  文章内容
    # ------------------------------------------------------------------ #

    def get_article_detail(self, url: str) -> Dict:
        """获取文章详情（纯文本/富文本）。0.03元/次"""
        return self._get("/fbmain/monitor/v3/article_detail", {"url": url})

    def get_article_html(self, url: str) -> Dict:
        """获取文章正文（带html格式）。0.04元/次"""
        return self._get("/fbmain/monitor/v3/article_html", {"url": url})

    def get_article_detail_pro(self, url: str) -> Dict:
        """获取文章详情Pro。0.045元/次"""
        return self._post("/fbmain/monitor/v3/article_detail", {"url": url})

    def search_article_by_keyword(self, keyword: str, page: int = 1, mode: str = "keyword") -> Dict:
        """
        关键词/分词搜索微信文章（数据库）。0.02元/条。
        mode: 'keyword' 精确关键词 | 'segment' 分词
        """
        return self._post("/fbmain/monitor/v3/kw_search", {
            "keyword": keyword,
            "page": page,
            "mode": mode,
        })

    # ------------------------------------------------------------------ #
    #  公众号信息
    # ------------------------------------------------------------------ #

    def get_principal_info(self, account: str) -> Dict:
        """获取公众号主体信息。0.5元/次"""
        return self._get("/fbmain/monitor/v3/principal_info", {"account": account})

    def get_article_comment(self, url: str) -> Dict:
        """获取公众号文章评论。0.06元/次"""
        return self._get("/fbmain/monitor/v3/article_comment2", {"url": url})

    def get_account_basic_info(self, account: str) -> Dict:
        """获取公众号基础信息（头像、类型、简介等）。0.5元/次"""
        return self._get("/fbmain/monitor/v3/avatar_type", {"account": account})

    def get_account_basic_data(self, account: str) -> Dict:
        """获取公众号基础数据（活跃粉丝、平均阅读等）。0.5元/次"""
        return self._get("/fbmain/monitor/v3/Keyverifycode", {"account": account})

    def search_account_by_owner(self, owner: str) -> Dict:
        """根据主体名获取该主体下所属公众号信息。0.2元/条"""
        return self._get("/fbmain/monitor/v3/owner_search_mp", {"owner": owner})

    def search_account_by_keyword(self, keyword: str) -> Dict:
        """根据关键字查询公众号。0.2元/条"""
        return self._get("/fbmain/monitor/v3/wx_account/search", {"keyword": keyword})

    def get_article_info(self, url: str) -> Dict:
        """获取公众号名称、文章标题和URL等信息。0.03元/次起"""
        return self._get("/fbmain/monitor/v3/article_info", {"url": url})

    def search_mp_via_sogou(self, keyword: str) -> Dict:
        """搜一搜 搜公众号。1.0元/次"""
        return self._post("/fbmain/monitor/v3/web_search", {
            "type": "search_mp",
            "keyword": keyword,
        })

    def get_follower_stats(self, url: str) -> Dict:
        """通过文章链接获取公众号最新粉丝数。0.5元/次起"""
        return self._get("/fbmain/monitor/v3/follower_stats", {"url": url})

    # ------------------------------------------------------------------ #
    #  榜单
    # ------------------------------------------------------------------ #

    def get_rank(self, category: str, period: str = "day") -> Dict:
        """
        获取指定类别公众号日榜/周榜/月榜。0.02元/次

        Args:
            category: 公众号类别
            period:   'day' | 'week' | 'month'
        """
        return self._get("/fbmain/rank/v1/get_account_type_rank", {
            "category": category,
            "period": period,
        })

    # ------------------------------------------------------------------ #
    #  搜一搜（实时）
    # ------------------------------------------------------------------ #

    def web_search(self, keyword: str, mode: int = 1) -> Dict:
        """
        获取微信搜一搜结果（实时）。mode=1: 0.5元/次；mode=2: 1.0元/次
        包含 mode1 和 mode2 两种模式。
        """
        return self._post("/fbmain/monitor/v3/web_search", {
            "type": "search_article",
            "keyword": keyword,
            "mode": mode,
        })

    def get_weixin_index(self, keyword: str) -> Dict:
        """获取微信指数。0.5元/次"""
        return self._post("/fbmain/monitor/v3/web_search", {
            "type": "weixin_index",
            "keyword": keyword,
        })

    def get_hot_articles(self, keyword: str, page: int = 1) -> Dict:
        """公众号爆文API。0.02元/条"""
        return self._post("/fbmain/monitor/v3/hot_typical_search", {
            "keyword": keyword,
            "page": page,
        })

    # ------------------------------------------------------------------ #
    #  搜狗链接转换
    # ------------------------------------------------------------------ #

    def sougou_temp_to_perm(self, url: str) -> Dict:
        """搜狗临时链接转永久链接。0.10元/次"""
        return self._get("/fbmain/monitor/v3/sougou_link", {"url": url})

    def sougou_search_to_perm(self, url: str) -> Dict:
        """搜狗搜索文章链接转永久链接。0.02元/次"""
        return self._get("/fbmain/monitor/v3/sougou_dn9a", {"url": url})
