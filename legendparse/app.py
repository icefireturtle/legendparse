from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from slice import slicer
app = Flask(__name__)

#database items
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


#orm classes
class Message(db.Model):
    __tablename__ = "messages"
    
    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(5), db.ForeignKey('records.record_type', name='fk_record_record_type'))
    message = db.Column(db.String(300), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_updated = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"Message: {self.message}, Record Type: {self.record_type}, Date Created: {self.date_created}, Last Updated: {self.last_updated}"
    
class Record(db.Model):
    __tablename__ = "records"
    
    record_type = db.Column(db.String(5), primary_key=True)
    field_id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(25))
    field_description = db.Column(db.String(75))
    field_length = db.Column(db.Integer)

    def __repr__(self):
        return f"Record Type: {self.record_type}, Field: {self.field_name}, Field Length: {self.field_length}"
    
#render functions
@app.route('/')
def index():
    messages = Message.query.all()
    records = Record.query.all()
    return render_template('index.html', messages=messages, records=records)

@app.route('/parser')
def parser():
    record_types = Record.query.with_entities(Record.record_type).distinct()
    return render_template('parser.html', record_types=record_types)

@app.route('/add_message', methods=["POST"])
def message():
    message = request.form.get("message")
    record_type = request.form.get("mRecordType")

    if message is not None and record_type is not None:
        m = Message(record_type=record_type, message=message)
        db.session.add(m)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/add_record', methods=["POST"])
def record():
    record_type = request.form.get("recordType")
    field_name = request.form.getlist("fieldName")
    field_description = request.form.getlist("fieldDesc")
    field_length = request.form.getlist("fieldLength")

    if record_type is not None and field_name is not None and field_length is not None:
        if len(field_name) > 1:
            for i in range(len(field_name)):
                field_id = i + 1
                n = field_name[i]
                d = field_description[i]
                l = field_length[i]
                r = Record(record_type=record_type, field_id=field_id, field_name=n, field_description=d, field_length=l)
                db.session.add(r)
        else:
            r = Record(record_type=record_type, field_id=1, field_name=field_name[0], field_description=field_description[0], field_length=field_length[0])
            db.session.add(r)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/slicer/<int:id>')
def sliced(id):
    message = Message.query.get_or_404(id)
    record_type = message.record_type
    records = Record.query.filter(Record.record_type==record_type)
    slice = slicer(message.message, records)
    return render_template('slicer.html', message=message, slice=slice, records=records, record_type=record_type)
    
@app.route('/delete/<int:id>')
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<string:record_type>/<int:field_id>')
def record_field_delete(record_type, field_id):
    record_field = Record.query.filter_by(record_type=record_type, field_id=field_id).first()
    print(record_field)
    db.session.delete(record_field)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>')
def message_update(id):
    message_id = Message.query.get_or_404(id)
    record_types = [row[0] for row in db.session.query(Record.record_type).filter(Record.record_type != message_id.record_type).distinct()]
    return render_template('update.html', message=message_id.message, id=message_id.id, record_type=message_id.record_type, record_types=record_types)

@app.route('/update/<int:id>', methods=["POST"])
def update_message(id):
    update_time = datetime.now()
    new_message = request.form.get("message")
    record_type = request.form.get("mRecordType")
    
    if new_message is not None and record_type is not None:
        db.session.bulk_update_mappings(Message, [{'id': id, 'record_type': record_type, 'message': new_message, 'last_updated': update_time}])
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')
    
@app.route('/update_field/<string:record_type>/<int:field_id>')
def record_field_update(record_type, field_id):
    record = Record.query.filter_by(record_type=record_type, field_id=field_id).first()
    return render_template('update_field.html', record=record, record_type=record.record_type, field_id=record.field_id)

@app.route('/update_field/<string:record_type>/<int:field_id>', methods=["POST"])
def update_record_field(record_type, field_id):
    field_name = request.form.get("fieldName")
    field_description = request.form.get("fieldDesc")
    field_length = request.form.get("fieldLength")

    if field_name is not None and field_length is not None:
        db.session.bulk_update_mappings(Record, [{'record_type': record_type, 'field_id': field_id, 'field_name': field_name, 'field_description': field_description, 'field_length': field_length}])
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)