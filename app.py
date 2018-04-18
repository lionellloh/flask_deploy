from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from db_interface import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name

def create_item(score, mass, category, deposited_by, created_at=None,
                extra_info=None):
    """
    Create a new deposited item.
    :param created_at: Datetime of creation (if not specified just defaults to
    server time)
    :param score: Score int
    :param mass: Mass int
    :param category: Category int
    :param deposited_by: User ID of depositing user
    :param extra_info: Extra info in JSON format
    :return: Id of new item or False if create failed
    """
    # Only one None of type NoneType - same effect as ... is None
    if not isinstance(extra_info, (str, type(None))):
        raise ValueError('extra_info isn\'t a str or None')

    params = {
        'score': int(score),
        'mass': int(mass),
        'category': int(category),
        'deposited_by': int(deposited_by),
        'created_at': created_at or datetime.now(),
        'extra_info': extra_info
    }

    with records.Database(DATABASE_URL) as db:
        try:
            db.query('''
                INSERT INTO Items (score, mass, category, deposited_by,
                  created_at, extra_info)
                VALUES (:score,:mass,:category,:deposited_by,:created_at,
                  :extra_info);
            ''', **params)

            return db.query('SELECT last_insert_id() AS id;').first()['id']
        except IntegrityError as e:
            print('IntegrityError! {}'.format(repr(e)))
            return False

# from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
# db = SQLAlchemy(app)
#
# # Create our database model
# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self, email):
#         self.email = email
#
#     def __repr__(self):
#         return '<E-mail %r>' % self.email
#
# # Set "homepage" to index.html
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# # Save e-mail to database and send to success page
# @app.route('/prereg', methods=['POST'])
# def prereg():
#     email = None
#     if request.method == 'POST':
#         email = request.form['email']
#         # Check that email does not already exist (not a great query, but works)
#         if not db.session.query(User).filter(User.email == email).count():
#             reg = User(email)
#             db.session.add(reg)
#             db.session.commit()
#             return render_template('success.html')
#     return render_template('index.html')
#
# if __name__ == '__main__':
#     app.debug = True
#     app.run()
#
#
# from flask import Flask, render_template, request
# # # import pymysql
# # import jinja2
# # # from flask.ext import mysql
# # from werkzeug import generate_password_hash, check_password_hash
# # from db_interface import *
#
# # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# # db = pymysql.connect(host = "127.0.0.1", user = "root", passwd = "lionell123", db = "smartbin", port = 3306)
#
# # app = Flask(__name__)
# # api = Api(app)
#
# # @app.route("/")
# # def main():
# # 	return render_template('index.html')
#
# # @app.route("/showSignUp")
# # def showSignUp():
# #  	return render_template('signup.html')
# # #
# # @app.route("/leaderboard", methods = ["GET"])
# # def someName():
# #  	cursor = db.cursor()
# #  	sql = "SELECT * FROM Users"
# #  	cursor.execute(sql)
# #  	results = cursor.fetchall()
# # # 	print(results)
# # # 	return render_template('leaderboard.html', results=results)
# # 	# return render_template('leaderboard.html')
# #
# #  @app.route("/signUp", methods=['POST'])
# #  def signUp():
# # 	return get_leaderboard()
#
# # def signUp():
# # 	try:
# # 		if request.method == "POST":
# # 			print("trying")
# # 			_name = request.form['inputName']
# # 			_email = request.form['inputEmail']
# # 			_password = request.form['inputPassword']
# #
# # 			print(_name, _email, _password)
# #
# # 			# validate the received values
# # 			if _name and _email and _password:
# #
# # 				# All Good, let's call MySQL
# #
# # 				conn = mysql.connect()
# # 				cursor = conn.cursor()
# # 				_hashed_password = generate_password_hash(_password)
# # 				cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
# # 				data = cursor.fetchall()
# #
# # 				if len(data) is 0:
# # 					conn.commit()
# # 					return json.dumps({'message':'User created successfully !'})
# # 				else:
# # 					return json.dumps({'error':str(data[0])})
# # 			else:
# # 				return json.dumps({'html':'<span>Enter the required fields</span>'})
#
# 	# except Exception as e:
# 	# 	return json.dumps({'error':str(e)})
# 	#
# 	# finally:
# 	# 	cursor.close()
# 	# 	conn.close()
#
#
# # if __name__ == "__main__":
# # 	app.run()
#
