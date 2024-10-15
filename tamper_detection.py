import requests
import hashlib
import time
import os
from datetime import datetime

# 設定ファイルのパス
CONF_FILE = "settings.conf"
LOG_FILE = "tamper_log.txt"
HASH_DIR = "hashes"

def load_config():
    """confファイルからインターバルとURLを読み込む"""
    urls = []
    interval = 60  # デフォルトのインターバル（秒）

    try:
        with open(CONF_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("interval="):
                    interval = int(line.split('=')[1])
                elif line and not line.startswith("#"):
                    urls.append(line)
    except FileNotFoundError:
        print(f"{CONF_FILE} が見つかりません。")
    
    return interval, urls

def get_hash(content):
    """HTMLコンテンツのハッシュを生成"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def log_tamper(url, message):
    """改ざんのログを記録"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {url}: {message}\n"
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(log_message)
    print(log_message.strip())

def check_website(url):
    """Webサイトの改ざんをチェック"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        current_hash = get_hash(response.text)

        os.makedirs(HASH_DIR, exist_ok=True)
        hash_file_path = os.path.join(HASH_DIR, f"{hashlib.md5(url.encode()).hexdigest()}.hash")

        previous_hash = ""
        if os.path.exists(hash_file_path):
            with open(hash_file_path, 'r') as f:
                previous_hash = f.read()

        if previous_hash and previous_hash != current_hash:
            log_tamper(url, "改ざんを検出しました！")

        with open(hash_file_path, 'w') as f:
            f.write(current_hash)

    except requests.RequestException as e:
        log_tamper(url, f"サイトへのアクセスに失敗しました: {e}")

if __name__ == "__main__":
    while True:
        interval, urls = load_config()
        if not urls:
            print("URLのリストが空です。")
            break

        for url in urls:
            check_website(url)

        print(f"{interval}秒後に再チェックします...")
        time.sleep(interval)
