from flask import Flask
from .extension import db, migrate, api
from flask_cors import CORS
from flask_restx import Resource
from . import model
from .config import Config
from .helpers.modifytime import time_ago
from sqlalchemy.orm import aliased
from flask import request
from bs4 import BeautifulSoup
import base64

def image_to_base64(image_data):
    return base64.b64encode(image_data).decode('utf-8')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    @api.route('/novel')
    class FetchAllNovel(Resource):
        def get(self):
            novels = db.session.query(model.Novel).all()
            return [novel.to_dict() for novel in novels]
    
    @api.route('/novel/<novelID>')
    class FetchOneNovel(Resource):
        def get(self, novelID):
            novelID = [int(id) for id in novelID.split(',')]
            novels = db.session.query(model.Novel).filter(model.Novel.id.in_(novelID)).all()
            return [novel.to_dict() for novel in novels]
        
    @api.route('/novel/<novelID>/<chapterID>')
    class FetchNovelChapter(Resource):
        def get(self, novelID, chapterID):
            chapter = db.session.query(model.NovelChapter).filter(model.NovelChapter.novel_id == int(novelID),model.NovelChapter.id == int(chapterID)).all()
            return [chapter.to_dict() for chapter in chapter]
    
    @api.route('/novel/<novelID>/all')
    class FetchAllNovelChapters(Resource):
        def get(self, novelID):
            novelID = [int(id) for id in novelID.split(',')]
            chapters = (db.session.query(model.NovelChapter.id.label('chapter_id'),model.Novel.id,model.Novel.picture,
                model.NovelChapter.chapter_title, model.Novel.name,model.Novel.description)
                        .join(model.Novel, model.Novel.id == model.NovelChapter.novel_id).filter(model.NovelChapter.novel_id.in_(novelID)).all())
            final = []
            for chapter in chapters:
                description = BeautifulSoup(chapter.description, "html.parser").get_text() if chapter.description else None
                final.append({
                    'novel_id': chapter.id,
                    'chapter_id': chapter.chapter_id,
                    'name': chapter.name,
                    'chapter_title': chapter.chapter_title,
                    'picture': image_to_base64(chapter.picture) if chapter.picture else None, 
                    'description': description
                })
            return final
        
    @api.route('/novel/mod')
    class FetchAllNovelOrderByDateModified(Resource):
        def get(self):
            novels = db.session.query(model.Novel).order_by(model.Novel.date_edited.desc()).all()
            return [novel.to_dict() for novel in novels]    

    @api.route('/novel/last')    
    class FetchNovelWithChapterLastUpdated(Resource):
        def get(self):
            chapter_alias = aliased(model.NovelChapter)
            
            novels = (
                db.session.query(
                    model.Novel.id, 
                    model.Novel.name, 
                    chapter_alias.chapter_title, 
                    chapter_alias.id.label('chapter_id'),  
                    chapter_alias.date_edited
                )
                .join(chapter_alias, model.Novel.id == chapter_alias.novel_id)
                .order_by(chapter_alias.date_edited.desc())
                .limit(10)
                .all()
            )
            
            final = []
            for novel in novels:
                final.append({
                    'novel_id': novel.id,
                    'chapter_id': novel.chapter_id,
                    'name': novel.name,
                    'chapter_title': novel.chapter_title,
                    'date_edited': novel.date_edited if novel.date_edited else None
                })
            
            return time_ago(final)
        

    @api.route('/novel/paginated')
    class FetchPaginatedNovels(Resource):
        def get(self):
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('limit', 20))
            
            pagination = db.session.query(model.Novel).paginate(page=page, per_page=per_page, error_out=False)
            
            final = []
            for novel in pagination:
                final.append({
                'id': novel.id,
                'name': novel.name,
                'chinese_name': novel.chinese_name,
                'picture': image_to_base64(novel.picture) if novel.picture else None,
                })
            return final
        

    @api.route('/search')
    class FetchSearchNovels(Resource):
        def get(self):
            search = str(request.args.get('query', 1))
            
            data = db.session.query(model.Novel).filter(model.Novel.name.contains(search))
            
            final = []
            for novel in data:
                final.append({
                'id': novel.id,
                'name': novel.name,
                'chinese_name': novel.chinese_name,
                'picture': image_to_base64(novel.picture) if novel.picture else None,
                })
            return final

    return app