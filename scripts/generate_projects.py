import json
import csv
import re

def clean_description(desc):
    """説明文から不要な文字列を削除"""
    if not desc or desc == "登録されていません。":
        return ""
    
    # 説明文の冒頭を抽出（最初の意味のある文章を取得）
    desc = desc.strip()
    
    # 不要な文字列パターンを削除
    patterns_to_remove = [
        r'操作方法関連記事使用アセット.*$',
        r'登録されていません。',
        r'このゲームは実況.*$',
        r'このゲームの実況ポリシー.*$',
        r'詳しくは「unityroom実況ポリシー」.*$',
        r'コピー用テキスト.*$',
        r'実況を行う場合は下記をよくご確認ください。.*$'
    ]
    
    for pattern in patterns_to_remove:
        desc = re.sub(pattern, '', desc, flags=re.MULTILINE | re.DOTALL)
    
    # 操作方法の前で切る
    if '操作方法' in desc:
        desc = desc.split('操作方法')[0]
    
    return desc.strip()

def generate_typescript_data():
    # CSVデータを読み込む
    trainee_data = {}
    with open('data/trainee_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['mentor_name']:
                trainee_data[row['mentor_name']] = {
                    'github_url': row['original_repository'],
                    'game_url': row['game_url']
                }
    
    # スクレイピングデータを読み込む
    with open('output/scraped_game_data.json', 'r', encoding='utf-8') as f:
        scraped_data = json.load(f)
    
    # TypeScriptデータを生成
    projects = []
    id_counter = 1
    
    for mentor_name, data in trainee_data.items():
        # GitHubリポジトリまたはgame_urlがない場合はスキップ
        if not data['github_url'] or not data['game_url']:
            continue
        
        # unityroomのURLがある場合、スクレイピングデータが存在しない（404エラー）ならスキップ
        if data['game_url'] and 'unityroom.com' in data['game_url'] and mentor_name not in scraped_data:
            continue
            
        project = {
            'id': str(id_counter),
            'studentName': mentor_name,
            'githubUrl': data['github_url']
        }
        
        # スクレイピングデータがある場合
        if mentor_name in scraped_data:
            scraped = scraped_data[mentor_name]
            project['projectTitle'] = scraped['title']
            project['description'] = clean_description(scraped['description'])
            project['thumbnail'] = scraped['icon_url']
            project['unityroomUrl'] = scraped['url']
        else:
            # スクレイピングデータがない場合（GitHub Releasesのみ）
            project['projectTitle'] = f"{mentor_name}の作品"
            project['description'] = ""
            
            # GitHub ReleasesのURLがある場合
            if data['game_url'] and 'github.com' in data['game_url']:
                project['githubReleaseUrl'] = data['game_url']
        
        projects.append(project)
        id_counter += 1
    
    return projects

def format_typescript_code(projects):
    """TypeScriptコードとしてフォーマット"""
    output = "import { Project } from '../types';\n\n"
    output += "export const projects: Project[] = [\n"
    
    for i, project in enumerate(projects):
        output += "  {\n"
        output += f"    id: '{project['id']}',\n"
        output += f"    studentName: '{project['studentName']}',\n"
        output += f"    projectTitle: '{project['projectTitle']}',\n"
        output += f"    description: '{project['description']}',\n"
        
        if 'unityroomUrl' in project:
            output += f"    unityroomUrl: '{project['unityroomUrl']}',\n"
        if 'githubReleaseUrl' in project:
            output += f"    githubReleaseUrl: '{project['githubReleaseUrl']}',\n"
        
        output += f"    githubUrl: '{project['githubUrl']}',\n"
        
        if 'thumbnail' in project and project['thumbnail']:
            output += f"    thumbnail: '{project['thumbnail']}',\n"
        
        output += "  }"
        if i < len(projects) - 1:
            output += ","
        output += "\n"
    
    output += "];\n"
    return output

if __name__ == '__main__':
    projects = generate_typescript_data()
    typescript_code = format_typescript_code(projects)
    
    # ファイルに出力
    with open('src/data/projects.ts', 'w', encoding='utf-8') as f:
        f.write(typescript_code)
    
    print(f"TypeScriptデータを生成しました: {len(projects)}件")
    print("出力ファイル: src/data/projects.ts")