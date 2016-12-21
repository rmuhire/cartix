from app.model.models import *
from app.model.schema import *
from flask import jsonify,request, session
from app.controller.exellentodb import Excellentodb
from app.controller.exellentodb import Excellento
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from app.controller.getusername import get_username
from werkzeug import secure_filename
from app.template.email import Email
import os
from app.controller.uniqid import uniqid


bcrypt = Bcrypt(app)
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['ALLOWED_EXTENSIONS'] = set(['xlsx','xls','csv'])


@app.route('/api/v1/exellento',methods=['POST'])
def excellento():
    data = Excellentodb('faking_it_1.xlsx').toexcel()
    return jsonify({'data':data})


@app.route('/api/v1/visualize', methods=['POST'])
def visualize():
    data = Excellento('all.xlsx').json()
    return jsonify({'data':data})


@app.route('/api/v1/user/', methods=['POST'])
def add_user():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    data, errors = user_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    username = get_username(data['email'])
    pwd_hash = bcrypt.generate_password_hash(data['password'])

    try:
        user = User(
            names=data['names'],
            username=username,
            email=data['email'],
            phone=None,
            user_role=None,
            regDate=None,
            password=pwd_hash,
            gender=None,
            update_key=None,
            ngo_id=data['ngo_id']
        )

        db.session.add(user)
        db.session.commit()

        last_user = user_schema.dump(User.query.get(user.id)).data
        Email(user.names, user.username, user.email).account()
        return jsonify({'result':True})

    except IntegrityError:
        return jsonify({'result': False})


@app.route('/api/v1/ngo/', methods=['POST'])
def add_ngo():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message':'No input data provided'}), 400

    data, errors = ngo_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        ngo = Ngo(
            name=data['name'].upper(),
            email=None,
            telephone=None,
            website=None,
            category=data['category'],
            picture=None,
            address=None
        )

        db.session.add(ngo)
        db.session.commit()

        return jsonify({'result': ngo.id})

    except IntegrityError:
        db.session().rollback()
        ngo = Ngo.query.filter_by(name=data['name'].upper()).first()
        return jsonify({'result': ngo.id})


@app.route("/api/v1/login/", methods=['POST'])
def login():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message':'no valid input provided'}), 400
    data, errors = user_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    username, password = data['username'], data['password']

    user = User.query.filter((User.username == username) | (User.email == username)).first()
    try:
        pw_hash = bcrypt.check_password_hash(user.password, password)
        if pw_hash:
            session['logged_in'] = True
            return jsonify({'result': user.id, 'ngo_id':user.ngo_id})
        else:
            status = False
            return jsonify({'result': status})
    except AttributeError:
        status = False
        return jsonify({'result': status})



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/api/upload/', methods=['POST','GET'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        tmp_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(tmp_filename)

        file_name,file_extension = os.path.splitext(tmp_filename)

        re_filename = uniqid()+file_extension


        destination = "/Users/muhireremy/cartix/uploads/user/"+re_filename
        #destination = "/home/www/cartix/uploads/user/"+re_filename
        os.rename(tmp_filename, destination)

        status, data = Excellentodb(destination).toexcel()

        if status:
            return jsonify({'status':status,'json':data,'originalpath':destination, 'filename':filename})
        else:
            return jsonify({'status':status, 'savepath':data, 'originalpath':destination, 'filename':filename})

    else:
        return jsonify({'status':2})


@app.route('/api/v1/file/save/', methods=['POST'])
def file_save():

    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'no valid input provided'}), 400

    data, errors = file_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        files = Files(
            original=data['original'],
            saved=data['save'],
            filename=data['filename'],
            regDate=None,
            user_id=data['user_id']
        )

        db.session.add(files)
        db.session.commit()

        last_file = file_schema.dump(Files.query.get(files.id)).data
        return jsonify({'auth': 1, 'file': last_file})

    except IntegrityError:
        pass


@app.route('/api/v1/file/user/', methods=['POST'])
def file_user():

    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'no valid input provided'}), 400

    data, errors = file_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    try:
        files = Files(
            original=data['original'],
            saved=data['save'],
            filename=data['filename'],
            regDate=None,
            user_id=data['user_id']
        )

        db.session.add(files)
        db.session.commit()

        to_db = Excellentodb(data['original']).todb()

        last_file = file_schema.dump(Files.query.get(files.id)).data
        return jsonify({'auth': 1, 'file': last_file,'todb':to_db})

    except IntegrityError:
        pass









