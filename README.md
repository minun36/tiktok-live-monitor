# TikTok Live Monitor Bot

TikTok の特定配信者のライブ開始を検知して、Discord に自動通知するボットです。
GitHub Actions で 5 分ごとに自動実行されます。

---

## ✨ 機能

- 指定した TikTok ユーザーがライブを開始したときだけ Discord に通知
- ライブ中か否かの状態を記憶し、**重複通知を防止**
- 監視対象の追加・削除が簡単

---

## 🚀 セットアップ

### 1. リポジトリを GitHub に公開する

```bash
git remote add origin https://github.com/<あなたのユーザー名>/<リポジトリ名>.git
git push -u origin main
```

---

### 2. Discord Webhook URL を取得する

1. 通知を送りたい Discord チャンネルの **設定** を開く
2. **連携サービス** → **ウェブフック** → **新しいウェブフック** をクリック
3. 名前を設定して **ウェブフック URL をコピー**

---

### 3. GitHub Secrets を設定する

リポジトリの **Settings → Secrets and variables → Actions → New repository secret** から以下を追加:

| Secret 名 | 値 |
|---|---|
| `DISCORD_WEBHOOK_URL` | コピーした Discord Webhook URL |
| `TIKTOK_USERNAMES` | 監視するユーザー名（複数はカンマ区切り: `rui_s_0,other_user`）|

> **メモ**: `TIKTOK_USERNAMES` を設定しない場合は `config.py` の `DEFAULT_USERNAMES` が使用されます。

---

### 4. GitHub Actions を有効化する

リポジトリの **Actions** タブを開き、`TikTok Live Monitor` を有効化してください。
`Run workflow` ボタンで即時テスト実行も可能です。

---

## ➕ 監視対象の追加・削除

### 方法 A: GitHub Secrets を編集（推奨）

`TIKTOK_USERNAMES` の値をカンマ区切りで変更するだけです。

例: `rui_s_0,new_streamer,another_one`

### 方法 B: `config.py` を直接編集

```python
DEFAULT_USERNAMES = [
    "rui_s_0",
    "new_streamer",  # ← この行を追加
    # "removed_user", # ← この行をコメントアウトまたは削除
]
```

変更後は `git commit & push` するだけで次回実行から反映されます。
`state.json` は自動的に同期されます（手動編集不要）。

---

## ⏰ 実行間隔の変更

`.github/workflows/monitor.yml` の `cron` 式を変更してください。

```yaml
- cron: '*/5 * * * *'   # 5分ごと（デフォルト・最短）
- cron: '*/10 * * * *'  # 10分ごと
- cron: '0 * * * *'     # 1時間ごと
```

> **注意**: GitHub Actions の無料プランでは cron の最短実行間隔は 5 分です。

---

## 🧪 ローカルテスト

```powershell
pip install -r requirements.txt

$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
$env:TIKTOK_USERNAMES   = "rui_s_0"
python monitor.py
```

---

## 📁 ファイル構成

```
tiktok-live-monitor/
├── .github/
│   └── workflows/
│       └── monitor.yml       # GitHub Actions ワークフロー
├── config.py                 # 設定（監視ユーザー一覧など）
├── discord_notifier.py       # Discord 通知モジュール
├── monitor.py                # メイン監視スクリプト
├── state.json                # ライブ状態記録ファイル（自動管理）
├── requirements.txt          # Python 依存関係
└── README.md
```

---

## ⚠️ 注意事項

- `TikTokLive` は非公式ライブラリです。TikTok の仕様変更で停止する可能性があります
- 問題が発生した場合は `pip install TikTokLive --upgrade` でアップデートしてください
- `state.json` は手動で編集しないでください（スクリプトが自動管理します）
