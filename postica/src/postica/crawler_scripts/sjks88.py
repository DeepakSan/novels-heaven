import requests
from bs4 import BeautifulSoup
import time
from deep_translator import GoogleTranslator

BASE_URL = "https://www.sjks88.com"
NOVEL_URL = "https://www.sjks88.com/chuanyue/50166.html"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}


def get_chapter_links(index_url):
    response = requests.get(index_url, headers=HEADERS)
    response.encoding = 'gb2312'  
    
    if response.status_code != 200:
        print("Failed to fetch index page.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    description = soup.select_one('.desc')
    title = soup.select_one('.box-artic h1')
    for br in description.find_all('br'):  # True finds all tags (not just <br>)
        br.decompose()
    description = description.get_text(strip=True)
    title = title.get_text(strip=True)
    arr = [title, description]
    translated_text = GoogleTranslator(source='chinese (simplified)', target='en').translate_batch(arr)
    links = [translated_text]
    links1 = [BASE_URL + a['href'] for a in soup.select('.list li a')]
    
    return links+links1

def get_chapter_content(chapter_url):
    response = requests.get(chapter_url, headers=HEADERS)
    
    response.encoding = 'gb2312'  
    
    if response.status_code != 200:
        print(f"Failed to fetch chapter: {chapter_url}")
        return ""

    soup = BeautifulSoup(response.text, 'html.parser')
    
    content_div = soup.find_all('p')
    text = [p.get_text() for p in content_div]
    
    if text:
        fin = []
        for raw_text in text:
            fin.append(raw_text) 
        translated_text = GoogleTranslator(source='chinese (simplified)', target='en').translate_batch(fin)
        return translated_text
    
    return "Content not found"

def save_to_file(content, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        for i in content:
            if not isinstance(i, str):
                continue
            f.write(i + "\n\n")
        f.write("\n\n")

def save_to_file_title_desc(content, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(content + "\n\n")
        f.write("\n\n")
        

def main():
    print("Fetching chapter links...")
    chapter_links = get_chapter_links(NOVEL_URL)
    
    if not chapter_links:
        print("No chapters found.")
        return
    
    save_to_file_title_desc(chapter_links[0][0], "translated_novel.txt")
    save_to_file_title_desc(chapter_links[0][1], "translated_novel.txt")

    print(f"Found {len(chapter_links)} chapters. Starting download...")
    
    for idx, chapter_link in enumerate(chapter_links[1:]):
        print(f"Crawling chapter {idx+1}/{len(chapter_links)}...")
        chapter_content = get_chapter_content(chapter_link)
        
        if chapter_content:
            save_to_file(chapter_content, "translated_novel.txt")
            print(f"Chapter {idx+1} saved.")
        else:
            print(f"Skipping chapter {idx+1} (no content).")
        
        time.sleep(2)  
    
    print("Crawling completed!")

if __name__ == "__main__":
    main()
