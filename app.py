import os
from flask import Flask,request,render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

@app.route("/")
def slash():
	db_table = db.execute("SELECT * FROM flights").fetchall()
	print(db_table)
	return render_template("index.html",flights = db_table)

@app.route("/putdb",methods=["POST"])
def putdb():
	'''
	<!-- 
		## If want get the var from html to app.py
		## Get it using the name="variable"
		## variable in the tag < values >
		## If send to the app.py 
		## Use the same things name = value -->
	'''
	value = request.form.get("value")
	fli_id = request.form.get("flight.id")
	# print(fli_id,value)  DEBUG on terminal

	r_c = db.execute("SELECT * FROM flights WHERE id=:id",{"id":fli_id}).rowcount

	db.execute("INSERT INTO passengers (name,flight_id) VALUES (:value,:id)",
		{"value" : value ,"id": fli_id })

	pas_table = db.execute("SELECT * FROM passengers").fetchall()

	db.commit()

	return render_template("sucess.html",value_sucess="You are registered Successfully") 

@app.route("/flights")
def flights():
	flights = db.execute("SELECT * FROM flights").fetchall()
	return render_template("flights.html",flights=flights)

@app.route("/flight/<int:flight_id>")
def flight(flight_id):
	#First html varibale and app.py variable
	flight_table = db.execute("SELECT * FROM flights WHERE id = :id",
		{"id":flight_id}).fetchone()

	passengers_table = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
		{"flight_id":flight_id}).fetchall()

	print(passengers_table,flight_table)

	return render_template("flight.html",flight = flight_table,passengers = passengers_table)

@app.route("/delent",methods=["POST"])
def delent():
	del_val = request.form.get("del_val")

	db.execute("DELETE FROM passengers WHERE name=:name",
	 	{"name" : del_val})

	db.commit()

	return render_template("del.html", val=del_val)