from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

'''
Piero Orderique 
24 May 2021

Tech w/Tim REST API w/ flask

Next steps:
>>> create a file for models
>>> main file should only include this config stuff and api.add_resource 
'''

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# models to be stored in our database
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # HAS to have info
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"

#? PARSE FORM! -- like parse_form() method in AirPiano I made, it does it easily
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True) # else defaulted to None if not required

#? PARSE FORM! -- all optional paramaters -- 'None' if not given
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video is required")
video_update_args.add_argument("likes", type=int, help="Likes on the video is required") # else defaulted to None if not required

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

# db.create_all() # ONLY RUN THIS LINE ONCE

class Video(Resource):
    # serialize this return value (object) using these resource fields: 
    @marshal_with(resource_fields) 
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first() # look for some VideoModel w/in db that has this id and return instances of those models
        if not result:
            abort(404, message="404 error - could not find video with that id")
        return result, 201

    @marshal_with(resource_fields) 
    def put(self, video_id):
        args = video_put_args.parse_args()

        result = VideoModel.query.filter_by(id=video_id).first() # look for some VideoModel w/in db that has this id and return instances of those models
        if result:
            abort(409, message="409 error: video id already exists fam")

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes']) # can we kwargs this?
        db.session.add(video)
        db.session.commit() # commit the changes
        return video, 201 # 201 means created

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="404 error - Video doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit() # commit the changes. we dont re"add" object.
    
        return result

    @marshal_with(resource_fields)
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first_or_404(description=f"video with id {video_id} not found.")
        db.session.delete(result)
        db.session.commit()
        return '', 204 # 204 = No Content -- signifies deleted successfully 

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
	app.run(debug=True)