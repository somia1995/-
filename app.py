from datetime import datetime
from flask import Flask,render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

class File(db.Model):
   __tablename__ = 'article'
   id = db.Column(db.Integer,primary_key = True )
   title = db.Column(db.String(80))
   created_time = db.Column(db.DateTime)
   category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
   category = db.relationship('Category')
   content = db.Column(db.Text)   
   def __repr__(self):
     return '<File %s>' % self.name
   def __init__(self,title,created_time,category,content):
      self.title=title
      self.created_time=created_time
      self.category=category
      self.content=content
      


class Category(db.Model): 
   __tablename__ = 'category'
   id = db.Column(db.Integer,primary_key = True)
   name = db.Column(db.String(80))
   files = db.relationship('File')
   def __repr__(self):
     return '<File %s>' % self.name
   def __init__(self,name):
     self.name=name

@app.route('/')
def index():
    files=File.query.all()
    return render_template('index.html',files=files)  
@app.route('/files/<file_id>')
def file(file_id):
    ff = File.query.get(file_id)
    if not ff:
        abort(404)
    return render_template('file.html',ff=ff)       
@app.errorhandler(404)
def not_found(error):
     
    return render_template('404.html'),404
if __name__=='__main__':
    app.run()

