import csv
import json
import time
import urllib.request
from html.parser import HTMLParser
import re

class UnityroomParser(HTMLParser):
    """unityroomのページから情報を抽出するパーサー"""
    def __init__(self):
        super().__init__()
        self.og_title = ""
        self.og_description = ""
        self.og_image = ""
        self.twitter_image = ""
        self.title = ""
        self.in_title = False
        self.game_icon_url = ""
        self.description_text = ""
        self.in_description = False
        self.current_h2 = ""
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'meta':
            # Open Graphタグから情報を取得
            if attrs_dict.get('property') == 'og:title':
                self.og_title = attrs_dict.get('content', '')
            elif attrs_dict.get('property') == 'og:description':
                self.og_description = attrs_dict.get('content', '')
            elif attrs_dict.get('property') == 'og:image':
                self.og_image = attrs_dict.get('content', '')
            # Twitterカードの画像も確認
            elif attrs_dict.get('name') == 'twitter:image':
                self.twitter_image = attrs_dict.get('content', '')
                
        elif tag == 'title':
            self.in_title = True
            
        elif tag == 'img':
            # ゲームアイコンを探す
            if 'class' in attrs_dict:
                classes = attrs_dict['class']
                if 'game-icon' in classes or 'GameIcon' in classes:
                    self.game_icon_url = attrs_dict.get('src', '')
            # srcにicon_という文字列が含まれる画像も候補とする
            src = attrs_dict.get('src', '')
            if 'icon_' in src and not self.game_icon_url:
                self.game_icon_url = src
                
        elif tag == 'h2':
            self.current_h2 = ""
            self.in_h2 = True
            
        elif tag == 'div':
            # ゲーム説明文のdivを探す
            if self.current_h2 == 'ゲーム紹介':
                self.in_description = True
            
    def handle_data(self, data):
        if hasattr(self, 'in_title') and self.in_title:
            self.title += data
        elif hasattr(self, 'in_h2') and self.in_h2:
            self.current_h2 += data.strip()
        elif self.in_description:
            self.description_text += data.strip()
            
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'h2':
            self.in_h2 = False
        elif tag == 'div' and self.in_description:
            self.in_description = False

def scrape_unityroom_game(url):
    """unityroomのゲームページから情報を取得"""
    try:
        print(f"スクレイピング中: {url}")
        
        # リクエストを送信
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        # HTMLを解析
        parser = UnityroomParser()
        parser.feed(html)
        
        # タイトルを決定（og:titleを優先、次にtitleタグ）
        title = parser.og_title or parser.title
        # " | フリーゲーム投稿サイト unityroom"などの余分な部分を削除
        title = re.sub(r'\s*\|\s*フリーゲーム投稿サイト\s*unityroom.*$', '', title, flags=re.IGNORECASE).strip()
        if not title:
            # titleタグから取得を試みる
            title = re.sub(r'\s*[\|｜]\s*.*unityroom.*$', '', parser.title, flags=re.IGNORECASE).strip()
        
        # 説明文を決定（og:descriptionを優先、なければ本文から）
        description = parser.og_description or parser.description_text
        
        # アイコンURLを決定（優先順位: ゲームアイコン > og:image > twitter:image）
        icon_url = parser.game_icon_url or parser.og_image or parser.twitter_image
        
        return {
            'title': title,
            'description': description,
            'icon_url': icon_url
        }
        
    except urllib.error.URLError as e:
        print(f"エラー: {url} - {str(e)}")
        return None
    except Exception as e:
        print(f"予期しないエラー: {url} - {str(e)}")
        return None

def main():
    input_file = 'data/trainee_data.csv'
    output_file = 'output/scraped_game_data.json'
    
    # 結果を格納する辞書
    scraped_data = {}
    
    # CSVファイルを読み込む
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            mentor_name = row['mentor_name']
            game_url = row['game_url']
            
            # unityroomのURLのみを処理
            if game_url and 'unityroom.com' in game_url:
                # スクレイピング実行
                game_info = scrape_unityroom_game(game_url)
                
                if game_info:
                    scraped_data[mentor_name] = {
                        'url': game_url,
                        'title': game_info['title'],
                        'description': game_info['description'],
                        'icon_url': game_info['icon_url']
                    }
                
                # サーバーに負荷をかけないよう待機
                time.sleep(1)
    
    # 結果をJSONファイルに保存
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(scraped_data, file, ensure_ascii=False, indent=2)
    
    print(f"\nスクレイピング完了: {len(scraped_data)}件のデータを取得")
    print(f"出力ファイル: {output_file}")
    
    # CSVファイルも作成
    csv_output = 'output/scraped_game_data.csv'
    with open(csv_output, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['mentor_name', 'game_url', 'title', 'description', 'icon_url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for mentor_name, data in scraped_data.items():
            writer.writerow({
                'mentor_name': mentor_name,
                'game_url': data['url'],
                'title': data['title'],
                'description': data['description'],
                'icon_url': data['icon_url']
            })
    
    print(f"CSVファイル: {csv_output}")

if __name__ == '__main__':
    main()