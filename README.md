# 傘いるくん 自動ツイートBot 🌧☁☀

くもすけが毎朝7時に、日本のランダムな都市の天気と傘の要否をツイートします。

## 仕組み

1. GitHub Actionsが毎朝7:00 JST に起動
2. 日本の49都市からランダムに1つ選択
3. Open-Meteo APIで天気を取得
4. くもすけ風のツイートを生成（〜くも。語尾）
5. X APIで `@kasa_kumosuke` に自動投稿

## セットアップ

### 1. X Developer APIキーの設定

GitHubリポジトリの Settings → Secrets and variables → Actions で以下を追加：

| Secret名 | 内容 |
|---|---|
| `X_API_KEY` | API Key |
| `X_API_KEY_SECRET` | API Key Secret |
| `X_ACCESS_TOKEN` | Access Token |
| `X_ACCESS_TOKEN_SECRET` | Access Token Secret |

### 2. 手動テスト

Actions タブ → "Daily Kumosuke Tweet" → "Run workflow" で手動実行できます。

### 3. ローカルテスト（ツイートせずに確認）

```bash
cd src
DRY_RUN=true python tweet.py
```

## ツイート例

```
おはよう〜くも！
今日の東京は☀️晴れだくも〜！傘はいらないくも！いってらっしゃい〜くも✨
（🌡8℃〜18℃・☔5%）

#傘いるくん #今日の天気 #東京
```

```
くもすけだくも〜！おはよう！
札幌は❄️雪が降りそうだくも〜！傘もマフラーもいるくも⛄
（🌡-3℃〜2℃・☔80%）

#傘いるくん #天気 #北海道
```
