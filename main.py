import datetime
import os
import time
import subprocess
import platform
import shutil
from pathlib import Path


def find_chrome_executable():
    """
    Chromeの実行ファイルパスを取得
    """
    system = platform.system()

    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(
                r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"
            ),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

    elif system == "Darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            return chrome_path

    elif system == "Linux":
        # コマンドラインでChromeを探す
        chrome_commands = ["google-chrome", "chromium-browser", "chromium"]
        for cmd in chrome_commands:
            if shutil.which(cmd):
                return cmd

    return None


def open_urls_in_new_tabs(urls, delay=2):
    """
    URLを確実に新しいタブで開く
    """
    if not urls:
        print("❌ URLリストが空です。")
        return

    chrome_path = find_chrome_executable()

    if not chrome_path:
        print("❌ Chromeが見つかりません。手動でブラウザを開いてください。")
        print("📋 開くべきURLリスト:")
        for i, url in enumerate(urls, 1):
            print(f"  {i}. {url}")
        return

    print(f"🌐 {len(urls)}個のURLを新しいタブで開きます...")
    print(f"🔧 使用ブラウザ: {chrome_path}")
    print("-" * 60)

    for i, url in enumerate(urls, 1):
        try:
            # URLの形式をチェック
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            print(f"  {i:2d}. 🔗 開いています: {url}")

            # OS別のコマンド実行
            if platform.system() == "Windows":
                # Windows: --new-tab オプションでタブで開く
                subprocess.Popen(
                    [chrome_path, "--new-tab", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            elif platform.system() == "Darwin":  # macOS
                # macOS: --args --new-tab でタブで開く
                subprocess.Popen(
                    ["open", "-na", "Google Chrome", "--args", "--new-tab", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            else:  # Linux
                # Linux: --new-tab オプション
                subprocess.Popen(
                    [chrome_path, "--new-tab", url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            # 次のURLを開く前に少し待機
            if i < len(urls):
                time.sleep(delay)

        except Exception as e:
            print(f"  ❌ エラー: {url} を開けませんでした - {e}")

    print("-" * 60)
    print("✅ URLオープン完了！")


def open_single_url_batch(urls):
    """
    全URLを一度に開く（代替方法）
    """
    chrome_path = find_chrome_executable()

    if not chrome_path:
        print("❌ Chromeが見つかりません。")
        return

    print(f"🚀 {len(urls)}個のURLを一括で開きます...")

    try:
        # 全URLを一度にChromeで開く
        formatted_urls = []
        for url in urls:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            formatted_urls.append(url)

        if platform.system() == "Windows":
            cmd = [chrome_path] + formatted_urls
        elif platform.system() == "Darwin":  # macOS
            cmd = ["open", "-na", "Google Chrome"] + formatted_urls
        else:  # Linux
            cmd = [chrome_path] + formatted_urls

        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ 一括オープン完了！")

    except Exception as e:
        print(f"❌ 一括オープンエラー: {e}")


def create_daily_memo():
    """
    今日の日付でメモファイルをダウンロードフォルダに作成
    """
    today = datetime.datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    downloads_path = Path.home() / "Downloads"
    memo_filename = f"memo_{date_str}.txt"
    memo_path = downloads_path / memo_filename

    memo_content = f"""📝 デイリーメモ - {date_str}
{'=' * 50}

作成日時: {today.strftime("%Y年%m月%d日 %H:%M:%S")}

【今日のタスク】
□ 
□ 
□ 

【重要事項】
• 
• 

【アイデア・メモ】
💡 
💡 

【明日の準備】
→ 
→ 

【その他】


---
自動生成: {memo_path}
"""

    try:
        if memo_path.exists():
            print(f"📄 メモファイル既存: {memo_path}")
        else:
            with open(memo_path, "w", encoding="utf-8") as f:
                f.write(memo_content)
            print(f"📝 メモファイル作成: {memo_path}")

        # ファイルを開く
        if platform.system() == "Windows":
            os.startfile(memo_path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", memo_path])
        else:
            subprocess.run(["xdg-open", memo_path])

        return str(memo_path)

    except Exception as e:
        print(f"❌ メモ作成エラー: {e}")
        return None


def main():
    """
    メイン実行関数
    """
    print("🚀 URL自動タブオープン&メモ作成ツール")
    print("=" * 60)

    # 実用的なURLサンプル
    general_urls = [
        "https://www.google.com",
        "https://github.com",
        "https://stackoverflow.com",
    ]

    dev_urls = [
        "https://www.python.org",
        "https://docs.python.org/ja/3/",
        "https://qiita.com",
        "https://zenn.dev",
    ]

    news_urls = [
        "https://news.yahoo.co.jp",
        "https://www.nikkei.com",
        "https://www.itmedia.co.jp",
    ]

    print("どのURLセットを開きますか？")
    print("1. 一般サイト (Google, GitHub, Stack Overflow)")
    print("2. 開発関連 (Python, Qiita, Zenn)")
    print("3. ニュース (Yahoo, 日経, ITmedia)")
    print("4. 全部")
    print("5. カスタム（コード内で編集）")

    # ここに自分用のURLを設定
    custom_urls = [
        "https://www.example.com",
        "https://www.google.com/search?q=Python+tutorial",
        # ← ここに好きなURLを追加してください
    ]

    try:
        choice = input("\n選択 (1-5) [Enter で1]: ").strip()

        if choice == "2":
            urls = dev_urls
        elif choice == "3":
            urls = news_urls
        elif choice == "4":
            urls = general_urls + dev_urls + news_urls
        elif choice == "5":
            urls = custom_urls
        else:
            urls = general_urls

    except KeyboardInterrupt:
        print("\n👋 終了します。")
        return

    print(f"\n📋 開くURL ({len(urls)}個):")
    for i, url in enumerate(urls, 1):
        print(f"  {i}. {url}")

    # 開き方を選択
    print(f"\n開き方を選択:")
    print("1. 順次タブで開く（推奨）")
    print("2. 一括で開く")

    try:
        method = input("選択 (1/2) [Enter で1]: ").strip()
    except KeyboardInterrupt:
        print("\n👋 終了します。")
        return

    # メモファイル作成
    print(f"\n1️⃣ メモファイル作成中...")
    memo_path = create_daily_memo()

    # URLを開く
    print(f"\n2️⃣ URLを開いています...")

    if method == "2":
        open_single_url_batch(urls)
    else:
        open_urls_in_new_tabs(urls, delay=2)

    print(f"\n🎉 完了！")
    if memo_path:
        print(f"📝 メモ: {memo_path}")

    print(f"\n💡 カスタムURLを使いたい場合:")
    print(f"   コード内の custom_urls リストを編集してください")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 プログラム中断")
    except Exception as e:
        print(f"\n❌ エラー: {e}")
