from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)


#database items
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#orm class
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=str(datetime.today()))

    def __repr__(self):
        return f"Message: {self.message}, Date Created: {self.date_created}"
    
#render functions
@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)