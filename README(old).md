# 食べ物クイズレビューアプリケーション

食べ物に関する4選択肢クイズに回答し、結果を記録・分析できるWebアプリケーションです。

## 特徴

- 🍽️ **食べ物特化**: スイーツ、料理、グルメなど食に関する108問のクイズ
- ✅ **即座のフィードバック**: 回答後すぐに正誤判定と解説
- 💾 **進捗保存**: レビュアーごと・カテゴリごとに途中から再開可能
- 📊 **結果記録**: 回答履歴をブラウザに自動保存
- ☁️ **S3バックアップ**: AWS S3への自動バックアップ対応（オプション）
- 📈 **統計分析**: カテゴリ別・レビューアー別の正解率を表示
- 📥 **エクスポート**: JSON/CSV形式でデータをダウンロード可能
- 🎨 **モダンなUI**: レスポンシブデザインで快適な操作感

## クイックスタート

### 方法1: ローカルで実行

```bash
# リポジトリをクローン
git clone https://github.com/obarayui/qareview_notimg.git
cd qareview_notimg

# HTTPサーバーを起動
python3 -m http.server 8000

# ブラウザで開く
open http://localhost:8000
```

### 方法2: GitHub Pagesで公開

1. リポジトリの Settings → Pages
2. Source: `main`ブランチ、`/ (root)`を選択
3. 公開URLにアクセス

**詳細な手順は [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) を参照してください。**

## AWS S3連携（オプション）

レビュー結果をAWS S3に自動バックアップできます。

### クイックセットアップ

1. AWS設定ファイルを作成:
   ```bash
   cp js/aws-config.example.js js/aws-config.js
   ```

2. `js/aws-config.js`を編集して、以下を設定:
   - `identityPoolId`: Cognito Identity Pool ID
   - `bucketName`: S3バケット名
   - `enableS3Upload`: `true`に設定

3. AWS環境の構築方法は [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) を参照

**注意**: `js/aws-config.js`は`.gitignore`に含まれています。Gitにコミットしないでください。

## 使い方

### 1. レビュー開始

1. ホーム画面でレビューアー名を入力
2. 問題セット「食べ物クイズ」を選択
3. レビュー画面に自動遷移

### 2. 回答

1. 4つの選択肢から1つを選択
2. 必要に応じてコメントを入力
3. 「回答を提出」をクリック
4. 正誤判定と正解を確認
5. 「次の問題へ」で続行

### 3. レビュー完了

- 全108問に回答すると自動的に統計が表示されます
- 結果はブラウザのlocalStorageに保存されます

### 4. データのエクスポート

ブラウザのコンソール（F12）で以下を実行:

```javascript
// JSON形式でエクスポート
StorageManager.exportToJSON();

// CSV形式でエクスポート（Excel対応）
StorageManager.exportToCSV();

// 統計情報を表示
const stats = StorageManager.getStatistics();
console.log(stats);

// すべてのデータを削除
StorageManager.clearAll();
```

## ファイル構成

```
qareview_notimg/
├── index.html                    # ホーム画面
├── review.html                   # レビュー画面
├── DEPLOYMENT_GUIDE.md           # デプロイメントガイド（GitHub Pages & AWS S3）
├── README.md                     # このファイル
├── .gitignore                    # Git除外設定
├── css/
│   └── style.css                # スタイルシート
├── js/
│   ├── app.js                   # メインロジック
│   ├── github.js                # データ取得
│   ├── storage.js               # データ保存・統計・S3アップロード
│   ├── aws-config.example.js    # AWS設定テンプレート
│   └── aws-config.js            # AWS設定（.gitignoreで除外）
├── food_quiz/                   # 問題セット
│   └── questions.json           # 食べ物クイズデータ（108問）
└── Claude_food_review.md        # プロジェクト仕様書
```

## 技術スタック

- **HTML5**: セマンティックなマークアップ
- **CSS3**: レスポンシブデザイン、モダンなUI
- **JavaScript (Vanilla ES6+)**: フレームワークなし、軽量高速
- **localStorage API**: ブラウザ内でのデータ永続化
- **AWS SDK for JavaScript**: S3へのデータアップロード（オプション）
- **AWS Services** (オプション):
  - S3: データストレージ
  - Cognito Identity Pool: 匿名認証

## ブラウザ要件

- モダンブラウザ（Chrome, Firefox, Safari, Edge）
- JavaScript有効
- localStorage有効
- Fetch API対応

## トラブルシューティング

### 問題: JSONが読み込めない

**原因**: file://プロトコルを使用している
**解決**: HTTPサーバーを起動してアクセス

```bash
# Python3
python3 -m http.server 8000

# Node.js
npx http-server -p 8000
```

### 問題: データが保存されない

**原因**: localStorageが無効化されている
**解決**: ブラウザの設定でlocalStorageを有効化、またはシークレットモードを解除

## カスタマイズ

### 独自の問題セットを追加

1. `questions.json`形式で問題データを作成
2. `food_quiz/`フォルダに配置
3. `index.html`に問題セットカードを追加

**questions.json形式:**
```json
{
  "questionID": "Q001",
  "keyword": "キーワード",
  "category": "カテゴリ",
  "question": "質問文",
  "choice": [
    "選択肢1(正解)",
    "選択肢2",
    "選択肢3",
    "選択肢4"
  ],
  "year": "2024",
  "reference_url": "https://example.com",
  "authored_by": "作成者名"
}
```

**注**: 正解は常に`choice`配列の**最初の要素（インデックス0）**です。

## ライセンス

MIT License

## 作成者

- オリジナル設計: Claude (Anthropic)
- 実装: Claude Code
- データ提供: SakuraQA food問題セット
