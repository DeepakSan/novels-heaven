import requests
from bs4 import BeautifulSoup
import time
from deep_translator import GoogleTranslator
import re

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
    description = soup.select_one('.desc')
    title = soup.select_one('.box-artic h1')
    for br in description.find_all('br'):  # True finds all tags (not just <br>)
        br.decompose()
    description = description.get_text(strip=True)
    title = title.get_text(strip=True)
    chinese_title=title

    arr = [title, description]

    translated_text = GoogleTranslator(source='chinese (simplified)', target='en').translate_batch(arr)
    translated_text[0] = clean_text(translated_text[0])
    translated_text[1] = clean_text(translated_text[1])


    links1 = [BASE_URL + a['href'] for a in soup.select('.list li a')]
    
    return chinese_title, translated_text[0], translated_text[1], links1

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

def clean_text(text):
    cleaned_text = re.sub(r"[^+【】.,!?a-zA-Z\s]", "", text)

    return cleaned_text
        

def main():
    print("Fetching chapter links...")
    chinese_title, title, description, chapter_links = get_chapter_links(NOVEL_URL)
    
    if not chapter_links:
        print("No chapters found.")
        return
    
    novel = {'chinese_title': chinese_title, 'title': title, 'description': description}

    chapters = {}

    print(f"Found {len(chapter_links)} chapters. Starting download...")
    
    for idx, chapter_link in enumerate(chapter_links):
        print(f"Crawling chapter {idx+1}/{len(chapter_links)}...")
        chapter_content = get_chapter_content(chapter_link)
        
        if chapter_content:
            save_to_file(chapter_content, "translated_novel.txt")
            if chapters.get('content') is None:
                chapters['content'] = []
                chapters['chapter_id'] = []
                chapters['chapter_title'] = []
                chapters['previous_chapter_id'] = []
                chapters['next_chapter_id'] = []
            chapters['content'].append(chapter_content)
            chapters['chapter_id'].append(idx+1)
            chapters['chapter_title'].append(idx+1)
            chapters['previous_chapter_id'].append(idx-1 if idx > 0 else None)
            chapters['next_chapter_id'].append(idx+2 if idx < len(chapter_links) - 1 else None)

            print(f"Chapter {idx+1} saved.")
            print(novel)
            print(chapters)

        else:
            print(f"Skipping chapter {idx+1} (no content).")
        
        time.sleep(2)  
    
    print("Crawling completed!")

if __name__ == "__main__":
    main()
