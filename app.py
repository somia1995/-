from flask import url_for
from datetime import datetime
from werkzeug.security import  generate_password_hash,check_password_hash
from jobplus.config import configs
from flask_login import UserMixin

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True 
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    
user_job = db.Table(
        'user_job',
        db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
        db.Column('job_id',db.Integer,db.ForeignKey('job.id',ondelete='CASCADE'))
        }

class User(Base,UserMixin):

    ROLE_JobHunter = 10
    ROLE_Company = 20
    ROLE_ADMIN = 30


    id  = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True,index=True,nullable=False)
    email = db.Column(db.string(64),unique=True,index=True,nullable=False)
    _password = db.Column('password',db.String(256),nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_JobHunter)
    realname = db.Column(db.String(32))
    add_jobs = db.relationship('Job',secondary='user_job') 
    resume_urls = db.Column(String(64))

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,orig_password):
        self._password = generate_password_hash(orig_password)
    def check_password(self,password):   
        return check_password_hash(self,_password,password)
    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN
    @property
    def is_company(self):
        return self.role == self.ROLE_Company

class Job(Base):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    lowsalary = db.Column(db.Integer,nullable=False)
    highsalary = db.Column(db.Integer,nullable=False)
    tags = db.Column(db.String(64))
    location = db.Column(db.String(128))
    education = db.Column(db.String(64))
    work_year = db.Column(db.String(24))
    is_fulltime = db.Column(db.Boolean,default=True)
    is_open = db.Column(db.Boolean,default=True)
    company_id = db.Column(db.Integer,db.ForeignKey('company.id',ondelete='CASCADE')
    company = db.relationship('Company',userlist=false) 

class Company(Base):
    
     id = db.Column(db.Integer,primary_key=True)
     name = db.Column(db.String(64),nullable=False,index=True,unique=True)
     logo = db.Column(db.String(64),nullable=False)
     website = db.Column(db.String(64),nullable=False)
     email = db.Column(db.String(24),nullable=False)
     location = db.Column(db.String(24),nullable=False)
     contact = db.Column(db.String(24),nullable=False)
     description = db.Column(db.String(24),nullable=False)
     about = db.Column(db.String(1024),nullable=False)
     tags = db.Column(db.String(128))
     welfares = db.Column(db.String(256))
     user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL'))
     user = db.relationship('User',userlist=False,backref=db.backref('company',userlist=False)

class Dilivery(Base):  
     
     STATUS_WAITING = 1
     STATUS_REJECT = 2
     STATUS_ACCEPT = 3

     id = db.Column(db.Integer,primary_key=True)
     job_id = db.Column(db.Integer,db.ForeignKey('job.id',ondelete='SET NULL')
     user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL')
     status = db.Column(db.SmallInteger,default=STATUS_WAITING)

     response = db.Column(db.String(64))
