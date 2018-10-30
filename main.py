from flask import Flask, redirect, request, render_template, session,flash
from flask_sqlalchemy import SQLAlchemy
#from hashtils import make_pw_hash, check_pw_hash
import cgi

app = Flask(__name__)
app.config['Debug']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:L@unchcode2@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key ='L@unchcode2'

db=SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body,owner):
        self.title = title
        self.body = body
        self.owmer = owner
    
    def __repr__(self):
        return '<Blog %r>' % self.title
    
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(120), unique=True )
    password=db.Column(db.String(120))
    blogpost = db.relationship('Blog', backref='owner')
        
    def __init__(self,username, password):
        self.username = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/newpost')
def newpostform():
    return render_template('Add-blog.html')


@app.route("/login",methods=['GET','POST'])
def login():
    Un_error = ''
    Pw_error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '':
            Un_error('Invalid Username')
        if password =='':
            Pw_error('Invalid Password')       
        
        user = User.query.filter_by(username=username).first()
        #if user == None:
            #   return 'User does not exist'
        if user and user.password == password:
            session['username'] = username
            flash('Logged by' +username)
            return redirect('/newpost')
        else:
            return 'User doesnot exist'
               #else:
    return render_template('login.html',Un_error=Un_error,Pw_error=Pw_error)
@app.route("/signup",methods=['GET','POST'])
def signup():
    un_error=''
    pw_error=''
    vp_error=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verifypassword = request.form['verifypassword']
      
        
        if username == '' or len(username) < 3 or len(username) >20 or username.isalpha() !=True:
            un_error = 'That\'s not a valid username'

        if password == '' or len(password) < 3 or len(password) > 20:
            pw_error = 'That\'s not a valid password'

        if verifypassword != password or verifypassword =='' :
            vp_error = 'Passwords didn\'t match'           

        if not un_error and not pw_error and not vp_error:
            exist_user=User.query.filter_by(username=username).first()
            if not exist_user: #and not user.password == password:            
                new_user=User(username,password)
                db.session.add(new_user)
                db.session.commit()   
                session['username'] = username 
                return redirect('/newpost')
            else:
                return 'A user with that Username already exists'
            
    
    return render_template('signup.html',un_error=un_error,pw_error=pw_error,vp_error=vp_error)         


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blogpost')

@app.route("/newpost",methods=['GET','POST'])
def newpost():
    title_error =''
    body_error =''
   
    title = request.form['title']
    body = request.form['body']
    if title == '' or body != '':
        title_error ='Please fill in the title'
    if body == '' or title != '':
        body_error ='Please fill in the body'
    owner= User.query.filter_by(username=session['username']).first()
    if title != '' and body != '':
        new_blog = Blog(title,body,owner)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blopost?id='+str(new_blog.id))
        #return redirect ('/addblog?id=' new_blog.id)
    else:
        return render_template('Add-blog.html',title =title, body=body,title_error= title_error,body_error = body_error)
    

@app.route("/blogpost")
def allposts():
    if request.args.get('id') != None:
        individual_id = request.args.get('id')
        blogpost = Blog.query.get(individual_id)
        user=User.query.get(blogpost.owner_id)
        print("#####$"+str(user))

        return render_template('individual.html',blogpost=blogpost,user=user)

    if request.args.get('user') != None:
        user_name= request.args.get('user')
        user = User.query.filter_by(username=user_name).first()
        blogpost=Blog.query.filter_by(owner_id=user.id).all()
        return render_template('singleuser.html',blogpost=blogpost,user=user)

    if request.args.get('id') == None:
        blogposts= Blog.query.order_by(Blog.id).all() #sorting the order
        users=User.query.all()
        return render_template('Main-blog.html',blogposts=blogposts,users=users)

@app.route('/')  
def index():
    if request.args.get('user') != None:
        user_name= request.args.get('user')
        user =User.query.get(user_name)
        blogpost =Blog.query.get('user.id')
        return render_template('singleuser.html',user=user,blogpost=blogpost) 
   
    if request.args.get('id') == None:
        users=User.query.all()

        return render_template('index.html',users=users)



@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','allposts','index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect("/login")


if __name__ == '__main__':        
    app.run(debug=True)


     