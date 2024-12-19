from flask import Flask
from .extension import db, migrate, api
from flask_cors import CORS
from flask_restx import Resource
from . import model
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    @api.route('/novel')
    class NovelHome(Resource):
        def get(self):
            novels = model.Novel.query.all()
            a = [novel.to_dict() for novel in novels]
            return a
    
    @api.route('/novel/<novelID>')
    class FetchNovel(Resource):
        def get(self, novelID):
            novelID = [int(id) for id in novelID.split(',')]
            novels = model.Novel.query.filter(model.Novel.id.in_(novelID)).all()
            return [novel.to_dict() for novel in novels]
        
    @api.route('/novel/<novelID>/<chapterID>')
    class FetchNovelChapter(Resource):
        def get(self, novelID, chapterID):
            chapter = model.NovelChapter.query.filter(model.NovelChapter.novel_id == int(novelID),model.NovelChapter.id == int(chapterID)).all()
            return [chapter.to_dict() for chapter in chapter]
    
    @api.route('/novel/<novelID>/all')
    class FetchAllNovelChapters(Resource):
        def get(self, novelID):
            novelID = [int(id) for id in novelID.split(',')]
            chapters = model.NovelChapter.query.filter(model.NovelChapter.novel_id.in_(novelID)).all()
            return [chapter.to_dict() for chapter in chapters]

    return app