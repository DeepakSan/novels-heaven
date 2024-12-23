import requests, time, re, math, random
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from multiprocessing import Pool, Manager
from functools import partial
from datetime import datetime
from ..extension import db
from ..app import create_app
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

BASE_URL = "https://www.sjks88.com"
NOVEL_URL = "https://www.sjks88.com/Direct6/50572.html"
NUM_PROCESSES = 5
MIN_DELAY = 30
MAX_DELAY = 40

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def get_random_delay():
    return random.uniform(MIN_DELAY, MAX_DELAY)

def get_chapter_links(index_url):
    for attempt in range(3):
        try:
            response = requests.get(index_url, headers=HEADERS, timeout=10)
            response.encoding = 'gb2312'  
            
            if response.status_code != 200:
                print(f"Failed to fetch index page. Status code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            description = soup.select_one('.desc')
            title = soup.select_one('.box-artic h1')
            
            if not description or not title:
                print("Failed to find required elements on page")
                continue
                
            for br in description.find_all('br'):
                br.decompose()
            description = description.get_text(strip=True)
            title = title.get_text(strip=True)
            chinese_title = title

            arr = [title, description]
            translated_text = GoogleTranslator(source='chinese (simplified)', target='en').translate_batch(arr)
            time.sleep(5)
            translated_text[0] = clean_text(translated_text[0])
            translated_text[1] = clean_text(translated_text[1])

            links1 = [BASE_URL + a['href'] for a in soup.select('.list li a')]
            
            return chinese_title, translated_text[0], translated_text[1], links1
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            time.sleep(get_random_delay())
    
    return None, None, None, []

def process_chapter_batch(chapter_data, shared_dict):
    start_idx, links = chapter_data
    local_chapters = {
        'content': [],
        'chapter_id': [],
        'chapter_title': [],
        'previous_chapter_id': [],
        'next_chapter_id': []
    }
    
    for idx, link in enumerate(links):
        global_idx = start_idx + idx
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Process {start_idx//len(links)}: Processing chapter {global_idx + 1}")
        
        try:
            chapter_content = get_chapter_content(link)
            if chapter_content:
                local_chapters['content'].append(chapter_content)
                local_chapters['chapter_id'].append(global_idx + 1)
                local_chapters['chapter_title'].append(f"Chapter {global_idx + 1}")
                local_chapters['previous_chapter_id'].append(global_idx if global_idx > 0 else None)
                local_chapters['next_chapter_id'].append(global_idx + 2 if global_idx < len(links) - 1 else None)
                
                print(f"[{timestamp}] Chapter {global_idx + 1} processed successfully")
            
            time.sleep(get_random_delay())
            
        except Exception as e:
            print(f"Error processing chapter {global_idx + 1}: {str(e)}")
            time.sleep(get_random_delay() * 2)
    
    shared_dict[start_idx] = local_chapters
    return local_chapters

def get_chapter_content(chapter_url):
    for attempt in range(3):
        try:
            response = requests.get(chapter_url, headers=HEADERS, timeout=10)
            response.encoding = 'gb2312'  
            
            if response.status_code != 200:
                print(f"Failed to fetch chapter: {chapter_url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find_all('p')
            text = [p.get_text() for p in content_div]
            
            if text:
                fin = []
                for raw_text in text:
                    fin.append(raw_text) 
                translated_text = GoogleTranslator(source='chinese (simplified)', target='en').translate_batch(fin)
                return translated_text
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {chapter_url}: {str(e)}")
            time.sleep(get_random_delay())
    
    return "Content not found"

def merge_results(shared_dict, total_batches):
    merged_chapters = {
        'content': [],
        'chapter_id': [],
        'chapter_title': [],
        'previous_chapter_id': [],
        'next_chapter_id': []
    }
    
    # Merge in correct order
    for batch_idx in range(total_batches):
        if batch_idx in shared_dict:
            batch_data = shared_dict[batch_idx]
            for key in merged_chapters.keys():
                merged_chapters[key].extend(batch_data[key])
    
    return merged_chapters

def clean_text(text):
    return re.sub(r"[^+【】.,!?a-zA-Z\s]", "", text)

def main():
    start_time = time.time()
    print(f"Starting crawl with {NUM_PROCESSES} parallel processes at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("Fetching chapter links...")
    chinese_title, title, description, chapter_links = get_chapter_links(NOVEL_URL)
    
    if not chapter_links:
        print("No chapters found.")
        return
    
    novel = {
        'chinese_title': chinese_title,
        'title': title,
        'description': description
    }
    
    batch_size = math.ceil(len(chapter_links) / NUM_PROCESSES)
    batches = []
    for i in range(0, len(chapter_links), batch_size):
        batch_links = chapter_links[i:i + batch_size]
        batches.append((i, batch_links))
    
    print(f"Split {len(chapter_links)} chapters into {len(batches)} batches")
    
    final_result = {}
    # Create a manager for sharing data between processes
    with Manager() as manager:
        shared_dict = manager.dict()
        
        # Create process pool and run parallel processing
        with Pool(processes=NUM_PROCESSES) as pool:
            process_batch_partial = partial(process_chapter_batch, shared_dict=shared_dict)
            pool.map(process_batch_partial, batches)
        
        # Merge results into final dictionary
        chapters = merge_results(shared_dict, len(batches))
        
        # Create the final dictionary structure
        final_result = {
            'novel': novel,
            'chapters': chapters
        }
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nCrawling completed!")
    print(f"Total time taken: {total_time/60:.2f} minutes")
    print(f"Average time per chapter: {total_time/len(chapter_links):.2f} seconds")
    print(f"Total chapters processed: {len(chapters['content'])}")
    
    return final_result

if __name__ == "__main__":
    result = main()
    novel_data = result['novel']
    chapters_data = result['chapters']

    app = create_app()
    with app.app_context():
        try:
            # Get current timestamp
            now = datetime.now()

            # Step 1: Insert Novel
            insert_novel_sql = text("""
                INSERT INTO novel (chinese_name, name, description, date_created, date_edited)
                VALUES (:chinese_title, :title, :description, :date_created, :date_edited);
            """)
            
            db.session.execute(insert_novel_sql, {
                'chinese_title': novel_data['chinese_title'],
                'title': novel_data['title'],
                'description': novel_data['description'],
                'date_created': now,
                'date_edited': now
            })

            # Step 2: Retrieve the novel_id of the inserted novel
            novel_id = db.session.execute(text("SELECT LAST_INSERT_ID();")).scalar()

            # Step 3: Insert Chapters
            insert_chapter_sql = text("""
                INSERT INTO chapter 
                (novel_id, id, chapter_title, content, previous_chapter_id, next_chapter_id, date_edited)
                VALUES (:novel_id, :chapter_id, :title, :content, :previous_chapter_id, :next_chapter_id, :date_edited);
            """)

            # Prepare chapter data
            chapters = []
            for i in range(len(chapters_data['content'])):
                chapters.append({
                    'novel_id': novel_id,
                    'chapter_id': chapters_data['chapter_id'][i],
                    'title': chapters_data['chapter_title'][i],
                    'content': chapters_data['content'][i],
                    'previous_chapter_id': chapters_data['previous_chapter_id'][i],
                    'next_chapter_id': chapters_data['next_chapter_id'][i],
                    'date_edited': now
                })

            # Bulk insert chapters
            db.session.execute(insert_chapter_sql, chapters)

            # Commit the transaction
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error inserting novel and chapters: {e}")
