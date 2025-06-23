# Scripts

このディレクトリには、プロジェクトで使用するスクリプトが含まれています。

## scrape_unityroom.py

unityroomからゲーム情報をスクレイピングするスクリプト

### 使用方法

```bash
python3 scripts/scrape_unityroom.py
```

### 入力
- `data/trainee_data.csv` - 研修生データ（mentor_name, original_repository, game_url）

### 出力
- `output/scraped_game_data.json` - JSON形式のスクレイピング結果
- `output/scraped_game_data.csv` - CSV形式のスクレイピング結果

### 取得情報
- ゲームタイトル
- ゲーム説明文
- ゲームアイコンURL