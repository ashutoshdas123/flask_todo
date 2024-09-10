import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:1234@localhost/flask_tut'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db.init_app(app)

class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = User(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = User.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    # to select the particular row to delete
    todo = User.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update')
def update():
    return 'this is the update page'

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)