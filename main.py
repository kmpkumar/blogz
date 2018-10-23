from flask import Flask, redirect, request, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['Debug']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:L@unchcode2@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

#bloglist = []
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    
    body = db.Column(db.String(120))
    #completed =db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        #self.completed =False

@app.route("/addblog")
def index():
    
    return render_template('Add-blog.html')

@app.route("/addblog",methods=['GET','POST'])
def addblog():
   
    #if request.method =='GET':
        #return render_template('Add-blog.html')
    #if request.method =='POST':
    title = request.form['title']
    body = request.form['body']
    #bloglist.append(title)
    #bloglist.append(body)
    title_error =''
    body_error =''
    if title == '' or body != '':
        title_error ='Please fill in the title'
    if body == '' or title != '':
        body_error ='Please fill in the body'

    if title != '' and body != '':
        new_blog = Blog(title,body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/mainblog?id='+str(new_blog.id))
        #return redirect ('/addblog?id=' new_blog.id)
    else:
        return render_template('Add-blog.html',title =title, body=body,title_error= title_error,body_error = body_error)
    

#@app.route("/addblog?id=")
@app.route("/mainblog")
def mainblog():
    if request.args.get('id') != None:
        individual_id =request.args.get('id')
        bloglists = Blog.query.get(individual_id)
        return render_template('individual.html',bloglists=bloglists)
    if request.args.get('id')== None:
        bloglists = Blog.query.all()
        #bloglist = Blog.query.filter_by(id=id).all()
        return render_template('Main-blog.html',bloglists=bloglists)



if __name__ == '__main__':        
    app.run()


     