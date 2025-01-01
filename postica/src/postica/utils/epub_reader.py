from ebooklib import epub
import ebooklib
from ..extension import db
from ..app import create_app
from bs4 import BeautifulSoup
from ..model import Novel, NovelChapter
from PIL import Image
import io


def get_all_metadata(book):
    metadata = {}
    for namespace, data in book.metadata.items():
        for name, values in data.items():
            key = f"{namespace}:{name}"
            metadata[key] = values
    return metadata

def resize_image(image_path, width, height):
    # Open the image file
    with Image.open(image_path) as img:
        # Resize the image
        img = img.resize((width, height))
        
        # Save the resized image to a byte buffer
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)  # Reset pointer to the beginning
        return img_byte_arr.read()

def update_novel_from_epub(epub_path, image_storage_path):
    book = epub.read_epub(epub_path)

    metadata = get_all_metadata(book)

    name = metadata.get('http://purl.org/dc/elements/1.1/:title', [''])[0][0]
    chinese_name = None  # metadata.get('http://purl.org/dc/elements/1.1/:creator', [''])[0][0]
    description = metadata.get('http://purl.org/dc/elements/1.1/:description', [''])[0][0]

    app = create_app()
    with app.app_context():

        novel = Novel.query.filter_by(name=name).first()

        if not novel:
            novel = Novel(
                name=name,
                chinese_name=chinese_name,
                description=description
            )
            db.session.add(novel)
            db.session.commit()

        # Now, handle the chapters
        chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        previous_chapter = None
        inserted_chapters = []

        # First, insert all chapters without setting previous/next chapter references
        for i in range(len(chapters)):  
            soup = BeautifulSoup(chapters[i].content, 'html.parser')

            # Extract chapter title
            chapter_title = soup.title.string if soup.title else 'Untitled'

            # Extract content
            content = str(soup)

            # Create the NovelChapter entry
            novel_chapter = NovelChapter(
                novel_id=novel.id,
                content=content,
                chapter_title=chapter_title,
                previous_chapter_id=None,  # Set later
                next_chapter_id=None  # Set later
            )

            # Add the chapter to the list to update later
            inserted_chapters.append(novel_chapter)
            db.session.add(novel_chapter)

        # Commit all the chapters at once
        db.session.commit()

        # Now, update previous_chapter_id and next_chapter_id for each chapter
        for i, chapter in enumerate(inserted_chapters):
            previous_chapter_id = inserted_chapters[i-1].id if i > 0 else None
            next_chapter_id = inserted_chapters[i+1].id if i < len(inserted_chapters) - 1 else None

            chapter.previous_chapter_id = previous_chapter_id
            chapter.next_chapter_id = next_chapter_id
            db.session.commit()  # Update each chapter individually

        # If there's a cover image, update the novel's record
        if image_storage_path:
            resized_image_data = resize_image(image_storage_path, 185, 250)  # Resize image to 200x250
            novel.picture = resized_image_data
            db.session.commit()

        print(f"Novel '{name}' and its chapters have been added/updated in the database.")


if __name__ == "__main__":
    image = ["/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/I Became An Immortal On Mortal Realm/",
             "/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/Invincible Divine Dragon S Cultivation System/",
             "/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/My Brother S The Protagonist Good Thing I Awakened/",
             "/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/My Life Can Be Infinitely Simulated/",
             "/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/The Big Shot S Movie Star Wife Is Beautiful And/",
             "/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/The Lucky Star Blessing The Whole Village/",]
    book = ["/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/I Became An Immortal On Mortal Realm/epub/I Became An Immortal On Mortal Realm c1-495.epub",
            "/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/Invincible Divine Dragon S Cultivation System/epub/Invincible Divine Dragon S Cultivation System c1-1609.epub",
            "/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/My Brother S The Protagonist Good Thing I Awakened/epub/My Brother S The Protagonist Good Thing I Awakened c1-149.epub",
            "/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/My Life Can Be Infinitely Simulated/epub/My Life Can Be Infinitely Simulated c1-432.epub",
            "/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/The Big Shot S Movie Star Wife Is Beautiful And/epub/The Big Shot S Movie Star Wife Is Beautiful And c1-732.epub",
            "/Users/deepaksanjaysj/Deepak Projects/Github Projects/novels-heaven/Lightnovels/www-novelhall-com/The Lucky Star Blessing The Whole Village/epub/The Lucky Star Blessing The Whole Village c1-466.epub"]
    for i in range(len(image)): 
        update_novel_from_epub(book[i],image[i]+"cover.jpg")
