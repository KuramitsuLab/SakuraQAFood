# SakuraQA レビューツール - 運用ガイド

このドキュメントは、SakuraQAのレビューツールの実際の運用方法とデータの流れを説明します。

---

## 📋 目次

1. [プロジェクト概要](#プロジェクト概要)
2. [アクセス方法](#アクセス方法)
3. [データセット](#データセット)
4. [レビューの流れ](#レビューの流れ)
5. [データの保存先](#データの保存先)
6. [システムアーキテクチャ](#システムアーキテクチャ)
7. [データ分析](#データ分析)

---

## プロジェクト概要

**SakuraQA レビューツール**は、4択クイズをレビューし、その結果をAWS S3に保存するWebアプリケーションです。

### 主な機能

- ✅ カテゴリ別の問題をレビュー
- 💾 1問ごとにリアルタイムでS3に保存
- 📊 レビュー結果の統計表示
- 📝 各問題へのコメント機能
- 🔄 途中保存と再開機能

---

## アクセス方法

### 本番環境（GitHub Pages）

**URL**: https://kuramitsulab.github.io/SakuraQAReview/

ブラウザで上記URLにアクセスすると、レビューツールが利用できます。

---

## データセット

### 問題ファイルの場所

```
/quiz/questions.json
```

### 問題数

問題セットに応じて変動します

### データ形式

各問題は以下の形式で保存されています：

```json
{
  "questionID": "Q001",
  "keyword": "キーワード例",
  "category": "カテゴリ名",
  "question": "問題文がここに入ります",
  "choice": [
    "選択肢1",
    "選択肢2",
    "選択肢3",
    "選択肢4"
  ],
  "answer": "正解となる選択肢",
  "year": "いつの時代の問題か",
  "reference_url": "参考になるURL",
  "authored_by": "GPT, Gemini, Claude, human...."
}
```

**重要**: 正解は`answer`フィールドに記載されており、`choice`配列のいずれかの選択肢と一致します。

---

## レビューの流れ

### 1. レビュー開始

アプリケーションのURLにアクセスして、レビュアー名とカテゴリを選択します。

### 2. 問題に回答

1. **問題文**と**4つの選択肢**が表示される
2. 1つの選択肢を選択
3. **「回答を提出」**ボタンをクリック
4. 正誤判定が即座に表示される
5. 問題に不備がある場合など、問題についてのコメントを入力可能

### 5. 次の問題へ

- **「次の問題へ」**ボタンで次の問題に進む
- 問題が途中の状態で保存される。続きから問題を解きたい場合は同じレビュー名にすれば、再度その続きから解ける
- 最後の問題では**「レビュー完了」**ボタンが表示される

### 6. レビュー完了

- 正解数・正解率などの統計が表示される
- 自動的にホーム画面に戻る

---

## データ分析

### 1. Webインターフェースで分析（※推奨　基本的にこちらでデータ分析が可能）

ホーム画面の**「📊 分析を見る」**ボタンをクリックすると、`analytics.html`が開き、レビュー結果を視覚的に分析できます。

**確認できる情報:**
- **全体正答率** - すべてのレビューの統計
- **レビュアー別正答率** - 各レビュアーの成績（グラフ・表）
- **問題作成者別正答率** - AIモデル別の正答率比較
- **問題別難易度** - 各問題の正答率（正答率順）

**使用できる機能:**
- **レビュアーのフィルター設定**: テスト用や練習用のレビュアーを統計から除外可能
  - 「レビュアー選択」セクションでチェックボックスを操作
  - 「すべて選択」「すべて解除」ボタンで一括操作
  - フィルター変更後、統計が自動的に再計算される
- **データのダウンロード**:
  - **全データ (JSONL)**: すべてのレビュー結果を詳細にダウンロード（AWS S3に保存されるのと同じ形式）
  - **問題別集計CSV**: 各問題の統計をExcelで開ける形式でダウンロード　こちらのファイルを使用すると分析しやすいかも

### 2. S3から直接データをダウンロード(研究室AWSを見る場合)

AWS Consoleから直接データを取得する場合：

1. **AWS Console** → **S3**
2. バケット `sakuraqa-review-results` を開く
3. `review.json` をクリック
4. **ダウンロード** ボタンをクリック

---

## データの保存先

### ローカル保存（localStorage）

すべてのレビュー結果は、まずブラウザの`localStorage`に保存されます。

**キー**: `review_results`

**形式**: JSON配列

### AWS S3への保存

レビュー結果は1問回答するごとに、AWS S3に自動保存されます。

#### 保存先

**S3バケット**: `sakuraqa-review-results`

**ファイルパス**: `review.json`

**リージョン**: `ap-northeast-1`（東京）

#### アクセス方法

```
AWS Console
→ S3
→ sakuraqa-review-results
→ review.json
```

### データ形式

S3の`review.json`は以下の形式で保存されています：

```json
[
  {
    "review_id": "review_1730369876543_abc12345",
    "question_id": "Q001",
    "question_set": "カテゴリ名",
    "question_index": 0,
    "keyword": "キーワード",
    "category": "カテゴリ名",
    "question_text": "問題文がここに入ります",
    "reviewer_name": "田中太郎",
    "answer": "選択肢1",
    "correct_answer": "選択肢1",
    "is_correct": true,
    "timestamp": "2025-10-31T12:34:56.789Z",
    "comment": "コメント例"
  },
  {
    "review_id": "review_1730369901234_def67890",
    "question_id": "Q002",
    "question_set": "カテゴリ名",
    "question_index": 1,
    "keyword": "キーワード2",
    "category": "カテゴリ名",
    "question_text": "別の問題文の例",
    "reviewer_name": "田中太郎",
    "answer": "選択肢2",
    "correct_answer": "選択肢1",
    "is_correct": false,
    "timestamp": "2025-10-31T12:35:23.456Z",
    "comment": ""
  }
]
```

### データ構造の詳細

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `review_id` | String | レビューの一意識別子（タイムスタンプ + ランダム文字列） |
| `question_id` | String | 問題ID（例: Q001） |
| `question_set` | String | 問題セット名（例: 食） |
| `question_index` | Number | 問題のインデックス番号（0から開始） |
| `keyword` | String | 問題のキーワード |
| `category` | String | カテゴリ名 |
| `question_text` | String | 問題文 |
| `reviewer_name` | String | レビューアー名 |
| `answer` | String | 選択した回答 |
| `correct_answer` | String | 正解の選択肢 |
| `is_correct` | Boolean | 正誤判定（true=正解、false=不正解） |
| `timestamp` | String | 回答日時（ISO 8601形式） |
| `comment` | String | コメント（オプション） |

### データの追記方式

- **1問回答するごとに**、Lambda関数が`review.json`を読み込み、新しいレビューデータを追加してS3に保存
- 同じ`review_id`が既に存在する場合は、そのレビューを更新（コメント追加など）
- 複数のレビューアーのデータが同一ファイルに蓄積される


### 使用しているAWSサービス

1. **API Gateway (HTTP API)**
   - エンドポイント: `https://ogllpkngp1.execute-api.ap-northeast-1.amazonaws.com/review`
   - メソッド: POST
   - CORS有効化

2. **AWS Lambda**
   - 関数名: `SaveReviewToS3`
   - ランタイム: Node.js 20.x
   - 役割: S3への読み書き処理

3. **AWS S3**
   - バケット名: `sakuraqa-review-results`
   - ファイル: `review.json`
   - アクセス: Lambda経由のみ（プライベート）

4. **CloudWatch Logs**
   - Lambda関数の実行ログを記録
   - エラー監視・デバッグに使用


---

## まとめ

このレビューツールは、以下の流れでデータを管理します：

1. **questions.json**（GitHub）から問題を取得
2. ユーザーがレビューを実行
3. **localStorage**（ブラウザ）に即座に保存
4. **API Gateway → Lambda → S3**の経路で`review.json`に追記保存
5. S3の`review.json`で全レビューデータを一元管理

すべてのデータは1つの`review.json`ファイルにJSON配列形式で保存され、後から分析や統計処理が可能です。

---

## 関連ドキュメント

- [README.md](./README.md) - プロジェクト全体の概要説明
