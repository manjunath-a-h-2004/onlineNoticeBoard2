from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ✅ Model MUST be defined before db.create_all()
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

# ✅ Create DB/tables if not exist
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    notices = Notice.query.order_by(Notice.date_posted.desc()).all()
    return render_template('index.html', notices=notices)

@app.route('/create', methods=['GET', 'POST'])
def create_notice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        notice = Notice(title=title, content=content)
        db.session.add(notice)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    create_tables()  # ✅ Ensure tables exist before running
    app.run(debug=True)
