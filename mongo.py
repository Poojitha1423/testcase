from pyexpat import model
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import json
from healthcheck import HealthCheck
from py import code


app = Flask(__name__)
health = HealthCheck()

app.config['MONGODB_SETTINGS'] = {
    'db': 'Table',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)


class User (db.Document):
    name = db.StringField()
    branch = db.StringField()
    age = db.IntField()
    def to_json(self):
        return {"name": self.name,
                "branch": self.branch,
                "age" : self.age}

@app.route("/")
def root_path():
    return("pooji")




def test_name():
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.get_data() == b'pooji'

@app.route('/user/', methods=['GET'])
def get_user():
    user = User.objects()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user)




def test_get():
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.get_data() 


@app.route('/user/', methods=['POST'])
def add_user():
    record = json.loads(request.data)
    user = User(name=record['name'],
                branch=record['branch'],
                age=record["age"])
    user.save()
    return jsonify(user)



def test_post():
    client = app.test_client()
    url = '/user'
    response = client.get(url)
    assert response.get_data() 

@app.route('/user/<id>/', methods=['PUT'])
def Update_user(id):
    record = json.loads(request.data)
    user = User.objects.get_or_404(id=id)
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(name=record['name'],
                    branch=record['branch'],
                    age=record["age"])
    return jsonify(user)




def test_put():
    client = app.test_client()
    url = '/user/'
    response = client.get(url)
    assert response.status_code == 200


@app.route('/user/<id>/', methods=['DELETE'])
def delete_user(id):
    user = User.objects(id=id)
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user)




class test(db.Document):
    name = db.StringField()
    job = db.StringField()
    salry = db.IntField()
    def to_json(self):
        return {"name": self.name,
                "job": self.job,
                "salry" : self.salry}



@app.route('/poojitha/', methods=['GET'])
def get_poojitha():
    poojitha = test.objects()
    if not poojitha:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(poojitha)



@app.route('/poojitha/', methods=['POST'])
def add_poojitha():
    record = json.loads(request.data)
    poojitha = test(name=record['name'],
                job=record['job'],
                salry=record["salry"])
    poojitha.save()
    return jsonify(poojitha)



@app.route('/poojitha/<id>/', methods=['PUT'])
def Update_poojitha(id):
    record = json.loads(request.data)
    poojitha=test.objects.get_or_404(id=id)
    if not poojitha:
        return jsonify({'error': 'data not found'})
    else:
        poojitha.update(name=record['name'],
                    job=record['job'],
                    salry=record["salry"])
    return jsonify(poojitha)




@app.route('/poojitha/<id>', methods=['DELETE'])
def delete_poojitha(id):
    poojitha= test.objects(id=id)
    if not poojitha:
        return jsonify({'error': 'data not found'})
    else:
       poojitha.delete()
    return jsonify(poojitha)

app.add_url_rule('/healthcheck','healthcheck',view_func=lambda: health.run())

if __name__=="__main__":
	app.run(debug=True)