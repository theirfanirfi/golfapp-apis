from flask import jsonify, request, send_from_directory, url_for, send_file
from flask_classful import FlaskView, route
from golfrica_app import app
import os
class Files(FlaskView):
    def index(self):
        pass

    @route("/clubs/des/<string:file_name>", methods=['GET'])
    def get(self, file_name):
        assets_folder = os.path.join(app.root_path, 'static/clubs/description/')
        print(assets_folder)
        try:
            # file = url_for('static', filename='clubs/description/'+file_name)
            # print(file)
            return send_from_directory(assets_folder,file_name)
        except Exception as e:
            return str(e)
        print("my file: "+file)
        return file
