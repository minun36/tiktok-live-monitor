"""
設定モジュール
-----------
監視対象の TikTok ユーザーや Discord Webhook URL を管理します。

【ユーザーの追加・削除】
TIKTOK_USERNAMES のリストにユーザー名（@なし）を追加・削除するか、
GitHub Secrets の TIKTOK_USERNAMES 環境変数をカンマ区切りで変更してください。
"""

import os

# ─────────────────────────────────────────────
# 監視対象の TikTok ユーザー名リスト（@なし）
# 環境変数 TIKTOK_USERNAMES が設定されている場合はそちらを優先します
# ─────────────────────────────────────────────
DEFAULT_USERNAMES = [
    "rui_s_0",
    # "another_user",  # ← ここに追加するだけでOK
]

raw_env = os.environ.get("TIKTOK_USERNAMES", "")
if raw_env.strip():
    TIKTOK_USERNAMES = [u.strip() for u in raw_env.split(",") if u.strip()]
else:
    TIKTOK_USERNAMES = DEFAULT_USERNAMES

# ─────────────────────────────────────────────
# Discord Webhook URL
# GitHub Secrets の DISCORD_WEBHOOK_URL から読み込みます
# ─────────────────────────────────────────────
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")

# ─────────────────────────────────────────────
# 状態ファイルのパス
# ─────────────────────────────────────────────
STATE_FILE = "state.json"
