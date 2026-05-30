import yt_dlp
import requests
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1510217727317377076/97JvAAoeLdrbwq23prH9JnXjc-qzKiH765A9KCnztGNhtAlyJnu2bwYBlssk_p7ClELL"
TIKTOK_USER = "yaraa2901"
LAST_VIDEO_FILE = "last_video.txt"

def get_latest_video():
    ydl_opts = {
        'extract_flat': True,
        'playlistend': 1,
        'quiet': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.tiktok.com/@{TIKTOK_USER}", download=False)
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
                return entry.get('id'), entry.get('url'), entry.get('title')
    except Exception as e:
        print(f"Error fetching TikTok: {e}")
    return None, None, None

def main():
    latest_id, video_url, title = get_latest_video()
    if not latest_id:
        print("Gagal mengambil data atau tidak ada video.")
        return

    last_id = ""
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, "r") as f:
            last_id = f.read().strip()

    if latest_id != last_id:
        print(f"Video baru: {latest_id}")
        msg = f"🚨 **{TIKTOK_USER}** baru upload TikTok!\n**Judul:** {title}\n**Tonton:** {video_url}"
        requests.post(WEBHOOK_URL, json={"content": msg})
        
        # Simpan ID agar tidak kirim notif ganda
        with open(LAST_VIDEO_FILE, "w") as f:
            f.write(latest_id)
    else:
        print("Tidak ada video baru.")

if __name__ == "__main__":
    main()
