from flask import Flask

app = Flask(__name__)

# @app.route("/")
# def main():
# 	return "heroku deployed haha jiabai zzz!"

@app.route('/')

def homepage():
	return render_template('index.html')


@app.route("/Authenticate")
def Authenticate():
	username = request.args.get('UserName')
	password = request.args.get('Password')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
	data = cursor.fetchone()
	if data is None:
		return "Username or Password is wrong"
	else:
		return "Logged in successfully"


if __name__ == '__main__':
	app.run()

