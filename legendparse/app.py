from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
app = Flask(__name__)

#database items
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


#orm class
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_updated = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"Message: {self.message}, Date Created: {self.date_created}, Last Updated: {self.last_updated}"
    
#render functions
@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@app.route('/parser')
def parser():
    return render_template('parser.html')

@app.route('/parser', methods=["POST"])
def message():
    message = request.form.get("message")

    if message is not None:
        m = Message(message=message)
        db.session.add(m)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')
    
@app.route('/delete/<int:id>')
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>')
def message_update(id):
    message_id = Message.query.get_or_404(id)
    return render_template('update.html', message=message_id.message, id=message_id.id)

@app.route('/update/<int:id>', methods=["POST"])
def update_message(id):
    update_time = datetime.now()
    new_message = request.form.get("message")
    
    if new_message is not None:
        db.session.bulk_update_mappings(Message, [{'id': id, 'message': new_message, 'last_updated': update_time}])
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)