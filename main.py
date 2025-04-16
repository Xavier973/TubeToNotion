import os
import re
from dotenv import load_dotenv
from notion_client import Client as NotionClient
from googleapiclient.discovery import build

# Charger les variables d'environnement
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

print("\n▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃")
print("📺  TubeToNotion  📝")
print("▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃\n")
print("Configuration :")
print(f"└─ Notion API   : {'✅' if NOTION_TOKEN else '❌'}")
print(f"└─ Base Notion  : {'✅' if NOTION_DATABASE_ID else '❌'}")
print(f"└─ YouTube API  : {'✅' if YOUTUBE_API_KEY else '❌'}\n")

# Initialiser les clients Notion et YouTube
notion = NotionClient(auth=NOTION_TOKEN)
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_youtube_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([\w\-]{11})", url)
    return match.group(1) if match else None

def parse_duration(duration):
    h, m, s = 0, 0, 0
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if match:
        h, m, s = [int(g) if g else 0 for g in match.groups()]
    return f"{h:02}:{m:02}:{s:02}" if h else f"{m:02}:{s:02}"

def get_video_duration_and_chanel(video_id):
    response = youtube.videos().list(
        part="contentDetails,snippet",
        id=video_id
    ).execute()
    items = response.get("items")
    if items:
        iso_duration = items[0]["contentDetails"]["duration"]
        channel_title = items[0]["snippet"]["channelTitle"]
        return parse_duration(iso_duration), channel_title
    return None, None

def update_notion_page(page_id, duration, channel_title):
    # Convertir la durée (HH:MM:SS ou MM:SS) en nombre de secondes pour Notion
    parts = duration.split(':')
    if len(parts) == 2:  # Format MM:SS
        minutes, seconds = map(int, parts)
        total_seconds = minutes * 60 + seconds
    else:  # Format HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        total_seconds = hours * 3600 + minutes * 60 + seconds

    notion.pages.update(
        page_id=page_id,
        properties={
            "Durée (s)": {"number": total_seconds},
            "Durée": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": duration}
                    }
                ]
            },
            "Auteur": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": channel_title}
                    }
                ]
            }
        }
    )

def get_all_pages():
    pages = []
    has_more = True
    next_cursor = None
    
    while has_more:
        if next_cursor:
            results = notion.databases.query(
                database_id=NOTION_DATABASE_ID,
                start_cursor=next_cursor,
                page_size=100
            )
        else:
            results = notion.databases.query(
                database_id=NOTION_DATABASE_ID,
                page_size=100
            )
        
        pages.extend(results["results"])
        has_more = results.get("has_more", False)
        next_cursor = results.get("next_cursor")
        
        if has_more:
            print(f"📑 Chargement des pages ... ({len(pages)} pages jusqu'à présent)")
    
    return pages

def get_page_title(props):
    try:
        title_prop = props.get("Titre", {})
        if not title_prop or not title_prop.get("title"):
            return "Sans titre"
        title_content = title_prop.get("title", [])
        if not title_content:
            return "Sans titre"
        return title_content[0].get("text", {}).get("content", "Sans titre")
    except:
        return "Sans titre"

def main():
    print("Analyse de la base Notion :")
    pages = get_all_pages()
    print(f"└─ {len(pages)} pages trouvées\n")
    print("⏳ Traitement des vidéos YouTube en cours...\n")
    
    youtube_count = 0
    updated_count = 0
    error_count = 0

    for page in pages:
        page_id = page["id"]
        props = page["properties"]
        url = ""
        title = get_page_title(props)

        # lire la propriété "URL"
        if "URL" in props:
            url_prop = props["URL"]
            if url_prop.get("url"):
                url = url_prop["url"]

        if "youtube.com/watch" in url:
            youtube_count += 1  # On compte toutes les URLs de vidéos
            
            # Vérifier si la page a déjà une durée ET un auteur
            if ("Durée" in props and props["Durée"].get("rich_text")) and \
               ("Auteur" in props and props["Auteur"].get("rich_text")):
                continue  # Passer à la page suivante si la durée et l'auteur existent déjà
            
            video_id = get_youtube_video_id(url)
            if video_id:
                duration, channel_title = get_video_duration_and_chanel(video_id)
                if duration:
                    try:
                        update_notion_page(page_id, duration, channel_title)
                        updated_count += 1
                    except Exception as e:
                        error_count += 1
                        print(f"└─ ❌ Erreur : '{title}'")
                        print(f"   └─ {str(e)}")
                else:
                    error_count += 1
                    print(f"└─ ⛔ Durée non trouvée : '{title}'")
                    print(f"   └─ {url}")
            else:
                error_count += 1
                print(f"└─ ⚠️ URL YouTube invalide : '{title}'")
                print(f"   └─ {url}")

    print("\n📊 Résumé :")
    print(f"└─ 📄 Pages analysées : {len(pages)}")
    print(f"└─ 🎥 URLs vidéos YouTube trouvées : {youtube_count}")
    print(f"└─ ✅ Pages mises à jour : {updated_count}")
    if error_count > 0:
        print(f"└─  ❌ Erreurs            : {error_count}")
    print("▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃\n")

if __name__ == "__main__":
    main()
