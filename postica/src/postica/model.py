from .extension import db

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
            'description': self.description,
            'picture': self.picture,
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
        return {
            'id': self.id,
            'novel_id': self.novel_id,
            'content': self.content,
            'previous_chapter_id': self.previous_chapter_id,
            'next_chapter_id': self.next_chapter_id,
            'chapter_title': self.chapter_title,
            'date_edited': self.date_edited.isoformat() if self.date_edited else None
        }