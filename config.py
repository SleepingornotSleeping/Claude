"""
极致了 API 配置
建议将 KEY 和 ADDON 通过环境变量注入，避免硬编码在代码中。
"""
import os

# --- 账户凭证 ---
# 优先读取环境变量，其次使用默认值（仅用于本地开发）
API_KEY = os.getenv("JIZHI_KEY", "JZL95ad9ef74f4d8371")
API_ADDON = os.getenv("JIZHI_ADDON", "syqabcd")

# --- 连接设置 ---
USE_LONG_LINK = True   # True: 长链接（推荐）; False: 短链接（备用）
REQUEST_TIMEOUT = 30   # 秒
