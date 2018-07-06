from flask import Blueprint,render_template,abort
from simpledu.models import User

user = Blueprint('user',__name__,url_prefix='/user')

@user.route('/<username>')
def index(username):

    
    user = User.query.all()
    u =  User.query.filter_by(username=username).all()
       
    if not u:    
    
        abort(404)
    else: 
      
        return render_template('user.html',user=user)
    
    

