"""
Discord 通知モジュール
--------------------
Discord Webhook に対してライブ開始通知を送信します。
"""

import requests
from datetime import datetime, timezone, timedelta


JST = timezone(timedelta(hours=9))


def send_live_notification(webhook_url: str, username: str) -> bool:
    """
    指定した TikTok 配信者のライブ開始通知を Discord に送信します。

    Parameters
    ----------
    webhook_url : str
        Discord の Webhook URL
    username : str
        TikTok ユーザー名（@なし）

    Returns
    -------
    bool
        送信成功なら True
    """
    live_url = f"https://www.tiktok.com/@{username}/live"
    now_str = datetime.now(JST).strftime("%Y/%m/%d %H:%M JST")

    payload = {
        "username": "TikTok Live Monitor",
        "avatar_url": "https://i.imgur.com/HXSaOuD.png",
        "embeds": [
            {
                "title": f"🔴 {username} がライブを開始しました！",
                "url": live_url,
                "description": (
                    f"**[▶ ライブを見る]({live_url})**\n\n"
                    f"`@{username}` の TikTok ライブが始まりました！"
                ),
                "color": 0xFF0050,  # TikTok レッド
                "fields": [
                    {
                        "name": "配信者",
                        "value": f"[@{username}](https://www.tiktok.com/@{username})",
                        "inline": True,
                    },
                    {
                        "name": "開始時刻",
                        "value": now_str,
                        "inline": True,
                    },
                ],
                "footer": {
                    "text": "TikTok Live Monitor Bot",
                },
            }
        ],
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"[通知送信] @{username} のライブ開始通知を Discord に送信しました")
        return True
    except requests.RequestException as e:
        print(f"[エラー] Discord への通知送信に失敗しました: {e}")
        return False
