from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_database.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), unique=True)

@login_manager.user_loader
def load_user(user_id):
  # return the sqlalchemy object for the user that it belongs to
  return User.query.get(int(user_id))
  
# route where user can login:
@app.route('/login')
def login():
  user = User.query.filter_by(username='marks214').first()
  # create a session based off the user, put the user id in the session, so when you visit different pages the user loader will look for the user id
  login_user(user)
  return f'<h1>{str(user)} logged in</h1>'

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