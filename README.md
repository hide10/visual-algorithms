# algorithm.hide10.com

静的HTMLで作る、アルゴリズム学習用の可視化サイトです。  
方針は `1アルゴリズム = 1ページ` で、各ページに次の要素を揃えます。

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

## 生成方式
- ページ本体は `scripts/generate_site.py` から一括生成
- 可視化の共通ランタイムは `app.js`
- 新しいページを足すときは、まず生成スクリプト内の定義を増やす

## ローカル確認
```bash
cd /home/hide10/algorithm.hide10.com
python3 -m http.server 8000
```

確認URL:

- `http://localhost:8000/`
- `http://localhost:8000/complexity/`
- `http://localhost:8000/bubble-sort/`
- `http://localhost:8000/selection-sort/`
- `http://localhost:8000/binary-search/`

## 次に作る予定
- 1ページずつ内容チェック
- GitHub Pages / 独自ドメインの公開手順整備
