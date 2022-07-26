from flask import Flask,render_template,session,url_for,request,redirect
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

app = Flask(__name__)
app.config["MYSQL_HOST"]       = "localhost"
app.config['MYSQL_DB']       = "posts"
app.config['MYSQL_USER']     = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():
    
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM postsss")
        posts = cur.fetchall()
        
        return render_template('index.html', posts=posts)

@app.route('/comments')
def comments():
    pass        
       

@app.route('/posts',methods=['POST','GET'])
def posts(): 
    
    
    if request.method == 'GET':
        return render_template('posts.html')

    else:
        author = request.form['author']
        title = request.form['title']
        post  = request.form['post']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO postsss(author,title,post) VALUES(%s,%s,%s)",(author,title,post))
        mysql.connection.commit()   
        return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM postsss WHERE post_id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        post  = request.form['post']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE postsss SET author=%s, title=%s, post=%s WHERE post_id=%s",(author,title,post,id))
        mysql.connection.commit()   
        return redirect(url_for('index'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM postsss WHERE post_id=%s",[id])
    pos = cur.fetchone()
    cur.connection.commit()
    return render_template('edit.html',pos=pos)
        
   
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'] .encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username,email,password) VALUES(%s,%s,%s)",(username,email,hash_password))
        cur.connection.commit()
        session['username'] = username
        session['email'] = email
        return redirect('/')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user) >= 0:
            if bcrypt.hashpw(password,user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['username'] = user['username']
                session['email'] = user['email']
                return redirect(url_for('index'))
            else:
                ms = "Your username and password does not match, please try again!"
                return render_template("Login.html", ms=ms)
        else:
            mm='user is not in the system'
            return render_template('signup.html', mm=mm)
    else:
        return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/like')
def like():
    pass

if __name__ == "__main__":
    app.secret_key='posts23uwe4ruy237'
    app.run(debug=True, port=1000)    
