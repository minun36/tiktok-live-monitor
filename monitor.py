"""
TikTok Live 監視スクリプト
--------------------------
GitHub Actions から定期実行されることを想定しています。
各配信者のライブ状態を確認し、オフライン→オンラインに変化した場合のみ Discord に通知します。
"""

import asyncio
import json
import sys
from pathlib import Path

from TikTokLive import TikTokLiveClient
from TikTokLive.client.errors import UserOfflineError, UserNotFoundError

from config import TIKTOK_USERNAMES, DISCORD_WEBHOOK_URL, STATE_FILE
from discord_notifier import send_live_notification


def load_state(usernames: list[str]) -> dict[str, bool]:
    """
    state.json を読み込みます。
    ファイルが存在しない場合、またはユーザーが未登録の場合は False で初期化します。
    """
    state_path = Path(STATE_FILE)
    if state_path.exists():
        with open(state_path, encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {}

    # リストにいるが state にないユーザーを初期化
    for username in usernames:
        if username not in state:
            state[username] = False

    # state にいるがリストから削除されたユーザーを削除
    state = {k: v for k, v in state.items() if k in usernames}

    return state


def save_state(state: dict[str, bool]) -> None:
    """現在の状態を state.json に保存します。"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"[状態保存] {STATE_FILE} を更新しました")


async def check_is_live(username: str) -> bool:
    """
    指定した TikTok ユーザーが現在ライブ中かどうかを確認します。

    Returns
    -------
    bool
        ライブ中なら True、オフラインや未検出なら False
    """
    client = TikTokLiveClient(unique_id=username)
    try:
        is_live = await client.is_live()
        print(f"[チェック] @{username}: {'🔴 ライブ中' if is_live else '⚫ オフライン'}")
        return is_live
    except UserOfflineError:
        print(f"[チェック] @{username}: ⚫ オフライン")
        return False
    except UserNotFoundError:
        print(f"[警告] @{username}: ユーザーが見つかりません（ユーザー名を確認してください）")
        return False
    except Exception as e:
        print(f"[エラー] @{username}: チェック中に予期しないエラーが発生しました: {e}")
        return False


async def main() -> None:
    if not DISCORD_WEBHOOK_URL:
        print("[エラー] DISCORD_WEBHOOK_URL が設定されていません。GitHub Secrets を確認してください。")
        sys.exit(1)

    if not TIKTOK_USERNAMES:
        print("[エラー] 監視対象のユーザーが設定されていません。config.py または TIKTOK_USERNAMES 環境変数を確認してください。")
        sys.exit(1)

    print(f"[開始] 監視対象: {', '.join(f'@{u}' for u in TIKTOK_USERNAMES)}")

    state = load_state(TIKTOK_USERNAMES)
    state_changed = False

    for username in TIKTOK_USERNAMES:
        was_live = state.get(username, False)
        is_live_now = await check_is_live(username)

        if is_live_now and not was_live:
            # オフライン → オンライン: 通知を送信
            print(f"[変化検出] @{username}: ライブ開始！通知を送信します。")
            send_live_notification(DISCORD_WEBHOOK_URL, username)
            state[username] = True
            state_changed = True

        elif not is_live_now and was_live:
            # オンライン → オフライン: 状態を更新（通知なし）
            print(f"[変化検出] @{username}: ライブ終了")
            state[username] = False
            state_changed = True

        else:
            print(f"[変化なし] @{username}: 状態変化なし ({'ライブ中' if is_live_now else 'オフライン'})")

    if state_changed:
        save_state(state)
        print("[完了] 状態を更新しました。GitHub Actions が state.json をコミットします。")
    else:
        print("[完了] 状態変化なし。state.json のコミットはスキップします。")


if __name__ == "__main__":
    asyncio.run(main())
