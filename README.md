# algorithm.hide10.com

静的HTMLで作る、アルゴリズム学習用の可視化サイトです。  
方針は `1アルゴリズム = 1ページ` で、各ページに次の要素を揃えます。

- 公開リポジトリ: `https://github.com/hide10/visual-algorithms`
- 公開URL: `http://algorithm.hide10.com/`

- アルゴリズムの短い説明
- 動きを追えるビジュアライザー
- 擬似コードとの対応
- 計算量の要約
- なぜその計算量になるかの補足

## 現在あるページ
- `/`
- `/complexity/`
- `/bubble-sort/`
- `/selection-sort/`
- `/binary-search/`
- そのほかを含め、現在は 31 ページ

## ディレクトリ構成
```text
algorithm.hide10.com/
├── AGENTS.md
├── README.md
├── app.js
├── binary-search/
│   └── index.html
├── bubble-sort/
│   └── index.html
├── complexity/
│   └── index.html
├── index.html
├── scripts/
│   └── generate_site.py
├── selection-sort/
│   └── index.html
├── styles.css
```

## コンテンツ方針
- 初学者向けを最優先
- まず直感、そのあと記法
- 小さな入力では見えない差を、数字と動きで見せる
- UIは派手さより理解しやすさを優先

## 公開方針
- GitHub Pages でも `algorithm.hide10.com` でも動くように、相対パス中心で構成
- 基本は同一コンテンツを配信
- 将来的に `hide10.com` 側へ展開する場合は、広告を載せるのは外側レイアウトのみで、教材本体は分離して保つ

## GitHub Pages 公開メモ
- `main` の静的ファイルをそのまま公開する前提
- 独自ドメインは `CNAME` に `algorithm.hide10.com` を置いて管理
- `.nojekyll` を置いて、GitHub Pages の Jekyll 変換を止める
- Pages の設定では、公開元を `Deploy from a branch` / `main` / `/ (root)` にする

## 生成方式
- ページ本体は `scripts/generate_site.py` から一括生成
- 可視化の共通ランタイムは `app.js`
- 新しいページを足すときは、まず生成スクリプト内の定義を増やす

## ローカル確認
```bash
cd /home/hide10/algorithm.hide10.com
python3 -m http.server 8017
```

確認URL:

- `http://127.0.0.1:8017/`
- `http://127.0.0.1:8017/complexity/`
- `http://127.0.0.1:8017/bubble-sort/`
- `http://127.0.0.1:8017/selection-sort/`
- `http://127.0.0.1:8017/binary-search/`

## 次に作る予定
- 1ページずつ内容チェック
- 用語と言い回しの重複整理
