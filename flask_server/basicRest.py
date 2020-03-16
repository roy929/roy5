import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "users.db"))

# creating a Flask app 
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
ma = Marshmallow(app)


# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# https://docs.sqlalchemy.org/en/13/core/constraints.html#unique-constraint
# https://www.w3schools.com/sql/sql_unique.asp
class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)  # the name of the users is unique
    password = db.Column(db.String(32), nullable=False)
    ip = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return 'users id:{} name:{} ip:{}'.format(self.id, self.name, self.ip)  # omit password


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('name', 'password', 'ip')


users_schema = UsersSchema()
userss_schema = UsersSchema(many=True)


class Call(db.Model):  # call other side
    __tablename__ = 'Call'
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String(32), unique=True, nullable=False)  # the name of the src caller is unique
    operation = db.Column(db.String(32), nullable=False)
    dst = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return 'users id:{} src:{} operation:{} dst:{}'.format(self.id, self.src, self.operation, self.dst)


class CallSchema(ma.Schema):
    class Meta:
        fields = ('src', 'operation', 'dst')


call_schema = CallSchema()
calls_schema = CallSchema(many=True)


@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        data = request.form
        print(data)
        name = request.form.get("name")
        password = request.form.get("password")
        ip = request.remote_addr

        # check if name already exist
        data = Users.query.filter_by(name=name).first()
        if data:
            return jsonify("False")

        new_user = Users(name=name, password=password, ip=ip)
        db.session.add(new_user)
        db.session.commit()
        print("new user:", new_user.id, name, password, ip)
        return jsonify("True")

    if request.method == 'GET':
        # login arrive to here
        user_name = request.form.get("name")
        password = request.form.get("password")
        result = 'False'

        # login
        if password:
            user_info = Users.query.filter_by(name=user_name, password=password).first()
            if user_info:
                print(user_info.name, user_info.ip)
                result = "True"

        # get IP by name
        else:
            user_info = Users.query.filter_by(name=user_name).first()
            if user_info:
                result = user_info.ip
        print('sending:', result)
        return jsonify(result)


@app.route('/call', methods=['POST', 'GET', 'DELETE', 'PUT'])
def call():
    if request.method == 'GET':
        dst = request.form.get("dst")
        src = request.form.get("src")
        result = "False"

        if src and dst:
            data = Call.query.filter_by(dst=dst, src=src).first()
            if data:
                # print(data.src, data.operation, data.dst)
                result = data.operation

        elif dst:
            row = Call.query.filter_by(dst=dst).first()
            if row:
                result = f"you got a call from:{row.src}"
            # print(data.src, data.operation, data.dst )
        # print('sending:', result)
        return jsonify(result)

    if request.method == 'POST':
        src = request.form.get("src")
        operation = request.form.get("operation")
        dst = request.form.get("dst")
        result = 'error'
        try:
            new_call = Call(src=src, operation=operation, dst=dst)
            db.session.add(new_call)
            db.session.commit()
            print("new_call:", new_call.id, src, operation, dst)
            result = "True"
        except:
            pass
        print('sending:', result)
        return jsonify(result)

    if request.method == 'PUT':
        src = request.form.get("src")
        operation = request.form.get("operation")
        dst = request.form.get("dst")
        row = Call.query.filter_by(src=src, dst=dst).first()
        print(row.operation)
        row.operation = operation
        db.session.commit()
        result = 'go to chat'
        print('sending:', result)
        return jsonify(result)

    if request.method == 'DELETE':
        src = request.form.get("src")
        operation = request.form.get("operation")
        dst = request.form.get("dst")
        result = "you are not a part of any connection"
        print('delete method:', src, operation, dst)

        if src:
            row = Call.query.filter_by(src=src).first()
            if row:
                db.session.delete(row)
                db.session.commit()
                result = 'deleted by src'
                print(result)

        if dst:
            row = Call.query.filter_by(dst=dst).first()
            if row:
                db.session.delete(row)
                db.session.commit()
                result = 'deleted by dst'
                print(result)

        print('sending:', result)
        return jsonify(result)

    # driver function


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
