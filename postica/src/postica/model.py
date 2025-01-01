from .extension import db
import base64
from bs4 import BeautifulSoup

def image_to_base64(image_data):
    return base64.b64encode(image_data).decode('utf-8')

def format_html_to_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    content_div = soup.find('div', {'id': 'htmlContent'})
    if not content_div:
        return ''
    
    for br in content_div.find_all('br'):
        br.replace_with('||LINEBREAK||')
    
    text = content_div.get_text()
    lines = [line.strip() for line in text.split('\n')]
    text = '\n\n'.join(line for line in lines if line)
    
    return text.strip()

class Novel(db.Model):
    __tablename__ = 'novel'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    chinese_name = db.Column(db.String(1000))
    description = db.Column(db.String(100000))
    picture = db.Column(db.LargeBinary)
    date_edited = db.Column(db.DateTime, nullable=False,default=db.func.now())
    date_created = db.Column(db.DateTime, nullable=False,default=db.func.now())
    
    chapters = db.relationship('NovelChapter', back_populates='novel', lazy='dynamic')
    
    def __repr__(self):
        return f'<Novel {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'chinese_name': self.chinese_name,
            'description': format_html_to_text(self.description) if self.description else None,
            'picture': image_to_base64(self.picture) if self.picture else None,
            'date_edited': self.date_edited.isoformat() if self.date_edited else None,
            'date_created': self.date_created.isoformat() if self.date_created else None
        }

class NovelChapter(db.Model):
    __tablename__ = 'novelchapter'
    
    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'), nullable=False)
    content = db.Column(db.Text, nullable=True)
    previous_chapter_id = db.Column(db.Integer, db.ForeignKey('novelchapter.id'), nullable=True)
    next_chapter_id = db.Column(db.Integer, db.ForeignKey('novelchapter.id'), nullable=True)
    chapter_title = db.Column(db.String(10000), nullable=False)
    date_edited = db.Column(db.DateTime, nullable=False,default=db.func.now())
    
    novel = db.relationship('Novel', back_populates='chapters')
    
    # Previous chapter relationship
    previous_chapter = db.relationship(
        'NovelChapter',
        primaryjoin="NovelChapter.previous_chapter_id==NovelChapter.id",
        remote_side=[id],
        backref=db.backref("next_chapters", uselist=False)
    )
    
    # Next chapter relationship
    next_chapter = db.relationship(
        'NovelChapter',
        primaryjoin="NovelChapter.next_chapter_id==NovelChapter.id",
        remote_side=[id],
        backref=db.backref("previous_chapters", uselist=False)
    )
    
    def __repr__(self):
        return f'<NovelChapter {self.chapter_title}>'
    
    def to_dict(self):
        description = format_html_to_text(self.content) if self.content else None
        return {
            'id': self.id,
            'novel_id': self.novel_id,
            'content': description,
            'previous_chapter_id': self.previous_chapter_id,
            'next_chapter_id': self.next_chapter_id,
            'chapter_title': self.chapter_title,
            'date_edited': self.date_edited.isoformat() if self.date_edited else None
        }