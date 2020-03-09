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
        if data is not None:
            return jsonify("False")

        newUser = Users(name=name, password=password, ip=ip)
        db.session.add(newUser)
        db.session.commit()
        print("p1:", newUser.id, name, password, ip)
        return jsonify("True")

    if request.method == 'GET':  # when login arrive to here
        user = request.form.get("name")
        password = request.form.get("password")
        # print("1111", user, password)
        result = 'False'
        data = Users.query.filter_by(name=user, password=password).first()  # data is type <class '__main__.Users'>
        if data is not None:
            print(data.name, data.ip)
            result = "True"

        # user ask for IP of name
        elif password is None:
            data = Users.query.filter_by(name=user).first()
            if data is not None:
                result = data.ip
        print('sending:', result)
        return jsonify(result)


@app.route('/call', methods=['POST', 'GET', 'DELETE', 'PUT'])
def call():
    if request.method == 'GET':
        dst = request.form.get("dst")
        # print("1111", user, password)
        data = Call.query.filter_by(dst=dst).first()
        print(data)
        if data is None:
            result = "False"
        else:
            result = "you got a call"
            # print(data.src, data.operation, data.dst )
        print('sending:', result)
        return jsonify(result)
    if request.method == 'POST':
        src = request.form.get("src")
        operation = request.form.get("operation")
        dst = request.form.get("dst")

        newCall = Call(src=src, operation=operation, dst=dst)
        db.session.add(newCall)
        db.session.commit()
        print("p1:", newCall.id, src, operation, dst)
        result = "calling"
        print('sending:', result)
        return jsonify(result)

    if request.method == 'PUT':
        src = request.form.get("src")
        operation = request.form.get("operation")
        dst = request.form.get("dst")
        row = Call.query.filter_by(src=src, dst=dst).first()
        row.operation = operation
        db.session.commit()
        result = 'go to chat'
        print('sending:', result)
        return jsonify(result)

    if request.method == 'DELETE':
        src = request.form.get("src")
        operation = request.form.get("operation")
        dst = request.form.get("dst")
        result = "there is no ope"

        if src is not None:
            row = Call.query.filter_by(src=src).delete()
            print(row)
            if row == 0:
                result = "False1"
            else:
                result = "{0} stopped".format(operation)
                db.session.commit()
        if dst is not None:
            row = Call.query.filter_by(operation=operation, dst=dst).delete()
            print(row)
            if row == 0:
                result = "False2"
                db.session.commit()

        print('sending:', result)
        return jsonify(result)

    # driver function


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
