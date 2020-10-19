from flask import Flask, render_template, request
import pymysql
app = Flask(__name__)

dbconn = pymysql.connect('3.95.38.205', 'keemo', 'password', 'demodb')

@app.route('/')
def hello_world():
	return render_template('intro.html')

@app.route('/hello/<name>')
def hello_name(name):
	return 'you are now into the webpath /hello with the get argument '+name

@app.route('/form')
def introduction():
	return render_template('webpage.html')

@app.route('/submit', methods=["POST", "GET"])
def submit():
	#form = request.form
	if request.method=="POST":
		print(request.form)
		fn = request.form['first']
		ln = request.form['last']
		em = request.form['myEmail']
		ph = request.form['pnumber']
		try:
			f = request.files['filename']
			f.save(f.filename)
		except:
			pass
		dbconn = pymysql.connect('3.95.38.205','keemo', 'password', 'contactdb')
		curs = dbconn.cursor()
		curs.execute("""INSERT INTO contactInfo values("%s","%s","%s","%s")"""%(fn, ln, em, ph))
		dbconn.commit()
		dbconn.close()
		return fetch()  #result needs to be rendered from fetch.html
	return "Sup Mang"

@app.route('/fetch')
def fetch():

	dbconn = pymysql.connect('3.95.38.205','keemo', 'password', 'contactdb')
	curs = dbconn.cursor()
	curs.execute("SELECT * FROM contactInfo")
	values = curs.fetchall()
	dbconn.close()
	print(values)
	return render_template("fetch.html", title='List of souls', result=values)

@app.route('/check/<uname>')  # this route communcates with MariaDB securely
def check(uname):
	dbconn = pymysql.connect('3.95.38.205','keemo', 'password', 'contactdb')
	curs = dbconn.cursor()
	curs.execute("SELECT * FROM contactInfo")
	values = curs.fetchall()
	dbconn.close()
	for i in values:
		if i[0].strip()==uname:  #strip removes blank spaces
			return "On the list"
	return "available"


if __name__ == '__main__':
	app.run(port=80, debug=True)

