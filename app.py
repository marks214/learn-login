from flask import Flask, render_template, request, session, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse, urljoin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_database.db'
# this should take the user to the page they were trying to access after they login
app.config['USE_SESSION_FOR_NEXT'] = True

db = SQLAlchemy(app)
login_manager = LoginManager(app)
# this redirects the user to the login screen if they are not logged in
login_manager.login_view = 'login'
# set a person message, otherwise there is a default
login_manager.login_message = 'You can\'t access that page, you need to login first'

def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  
  # is this a url on my server? if it is, redirect, if not, don't
  return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), unique=True)

@login_manager.user_loader
def load_user(user_id):
  # return the sqlalchemy object for the user that it belongs to
  return User.query.get(int(user_id))
  
# route where user can login:
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    user = User.query.filter_by(username=username).first()

    if not user:
      return 'User does not exist!'
    
    login_user(user)

    if 'next' in session:
      next = session['next']

      if is_safe_url(next):
        return redirect(next)
    
    return '<h1>Your are now logged in!</h1>'
  
  # session['next'] = request.args.get('next')
  return render_template('login.html')

@app.route('/home')
@login_required
def home():
  return '<h1>You are in the protected area!</h1>'

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return '<h1>you are now logged out</h1>'

if __name__ == '__main__':
  app.run(debug=True)