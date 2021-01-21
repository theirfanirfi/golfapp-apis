from datetime import datetime
import os
from golfrica_app import app
import json

def uploadMultipleImages(files, upload_folder, user):
    data = {
        'status': None,
        'media': {'images': [], 'video': []},
    }
    if not files:
        return data
    images = files.getlist('images[]')
    media = list()
    for image in images:
        dt_obj = datetime.strptime(str(datetime.now()),'%Y-%m-%d %H:%M:%S.%f')
        millisec = str(dt_obj.timestamp() * 1000)
        time = millisec.replace('.','')
        image_name = user.first_name+str(user.user_id)+time+'.jpg'
        media.append(image_name)
        image.save(os.path.join(app.config['UPLOAD_FOLDER']+'/'+upload_folder+'/', image_name))

    data['media'] = {'images': media, 'video': []}
    return data


def mediaLinksToJson(media):
    data = {
        'video': media['video'],
        'images': media['images'],
    }
    return json.dumps(data)
