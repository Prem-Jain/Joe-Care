from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
from User import User
from Query import Query
from Admin import Admin, AdminUSER
from ExpertRequest import ExpertRequest as Expreq
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from datetime import timedelta, date, datetime

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'JoeCare_801')

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"Login to access this page." ##Added

class LoginUser(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"    
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)
    def is_active():
        return True

logged_user = False 

class event_login:
    def user_in(self):
        self.login = True
    def user_out(self):
        self.login = False
    def get_user(self):
        return self.login
    
class JoeCareUser:
    def __init__(self):
        self.login = self.id = self.name = self.dob = self.age = self.phno = self.add = self.email = self.pwd = self.login = False
    def set_user(self, user_id, name, dob, address, phno, email, password):
        self.id = user_id
        self.name = name
        self.dob = dob
        self.age = self.calc_age()
        self.add = address
        self.phno = phno
        self.email = email
        self.pwd = password   
    def calc_age(self):
         x = datetime.strptime(self.dob, '%Y-%m-%d')
         today = date.today()
         one_or_zero = ((today.month, today.day) < (x.month, x.day))
         year_difference = today.year - x.year
         y = 1 if one_or_zero else 0
         curr_age = year_difference - y
         return curr_age
    def user_in(self):
        self.login = True
    def user_out(self):
        self.login = False
    def get_user(self):
        return self.login
    def check_passowrd(self, pwd):
        return self.pwd == pwd
    def get_curr_user_name(self):
        return self.name
curr_user = JoeCareUser()
      
@app.route('/')
def index():
    return render_template("index.html", logged = curr_user.get_user())

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['user_email']
        pwd = request.form['pwd']
        if User.check_email_exists(email) == False:
            return render_template('login.html', info='Email Does Not Exist!!!')
        record = User.get_user_details(email)
        if record[6] != pwd:
            return render_template('login.html', info='Invalid Password!!!')
        else:
            logged_user = LoginUser(record)
            curr_user.set_user(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            login_user(logged_user)
            curr_user.user_in()
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        address = request.form['Address']
        phno = request.form['phno']
        email = request.form['user_email']
        pwd = request.form['pwd']
        conf_pwd = request.form['conf_pwd']
        if User.check_email_exists(email) == True:
            return render_template("signup.html", info = "Email already Exits!!!")
        if pwd != conf_pwd:
            return render_template("signup.html", info = "Password and Confirm Password doesn't Match")
        User.add_new_user(name, dob, address, phno, email, pwd)
        record = User.get_user_details(email)
        curr_user.set_user(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
        logged_user = LoginUser(record)
        login_user(logged_user)
        curr_user.user_in()
        return redirect(url_for('index'))
    return render_template("signup.html")

@app.route("/query")
@login_required
def query():
    records = Query.get_app_post()
    return render_template("query.html", logged = curr_user.get_user(), records = records)

@app.route("/post", methods = ['POST', 'GET'])
@login_required
def anonymous():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['msg']
        anony = request.form.get('anony')
        if anony != "True":
            anony = "False"
        Query.add_new_post(curr_user.id, title, desc, anony, curr_user.name, curr_user.email, curr_user.age)
        return render_template("post.html", info = "You post have been sent to moderation. It will be approved in 24 hours.", logged = curr_user.get_user())
    return render_template("post.html", logged = curr_user.get_user())

@app.route("/querypost/<int:postid>", methods = ['POST', 'GET'])
@login_required
def querypost(postid):
    records = Query.get_post_postid(postid)
    comments = Query.get_comments(postid)
    return render_template("querypost.html", logged = curr_user.get_user(), records = records, comments = comments)

@app.route("/comment/<int:postid>", methods = ['POST'])
@login_required
def comment(postid):
    if request.method == "POST":
        comment = request.form["comment"]
        anony = request.form.get("anony")
        if anony != "True":
            anony = "False"
        Query.add_comment(postid, curr_user.id, curr_user.name, curr_user.email, comment, anony)
        return redirect(url_for("querypost", postid = postid))
    return redirect(url_for("querypost", postid = postid))
   
@app.route("/expert", methods=['POST', 'GET'])
@login_required
def expert():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form['email']
        phno = request.form["phno"]
        msg = request.form["msg"]
        res = request.form['res']
        Expreq.add_expert(curr_user.id, name, email, phno, msg, res, "False")
        return render_template("expert.html", logged = curr_user.get_user(), info="You request have been sent to moderation. You will be contacted in 24 hours.")
    return render_template("expert.html", logged = curr_user.get_user())

@app.route('/contact')
def contact():
    return render_template("index.html", scroll = 'foot', logged = curr_user.get_user())

@app.route("/profile")
@login_required
def profile():
    posts = Query.get_posts_profile(curr_user.id)
    posted = False
    if len(posts) > 0:
        posted = True
    return render_template("profile.html", name = curr_user.name, dob = curr_user.dob, age = curr_user.age,
       add = curr_user.add, phno = curr_user.phno, email = curr_user.email, logged = curr_user.get_user(),
       posts = posts, posted = posted)

@app.route("/editprofile/")
@login_required
def editprofile():
    return render_template("edit.html", logged=curr_user.get_user(), name = curr_user.name, dob = curr_user.dob, age = curr_user.age,
       add = curr_user.add, phno = curr_user.phno, email = curr_user.email)

@app.route("/changepassword", methods=['POST', 'GET'])
@login_required
def changepassword():
    if request.method == "POST":
        oldpwd = request.form['oldpwd']
        newpwd = request.form['newpwd']
        confpwd = request.form['confpwd']
        if not curr_user.check_passowrd(oldpwd):
            return render_template("changepassword.html", logged=curr_user.get_user(), info="Old Password doesn't match")
        if newpwd != confpwd:
            return render_template("changepassword.html", logged=curr_user.get_user(), info="Confirm Password doesn't match")
        User.update_password(newpwd, curr_user.id)
        record = User.get_user_details(curr_user.email)
        curr_user.set_user(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
        return redirect(url_for('profile'))
    return render_template("changepassword.html", logged=curr_user.get_user())

@app.route("/delacc")
@login_required
def deleteacc():
    User.delete_acc_posts(curr_user.id)
    User.delete_acc(curr_user.id)
    return redirect(url_for('logout'))

@app.route("/edit", methods = ["POST"])
@login_required
def edit():
    if request.method == "POST":
        name = request.form['name']
        dob = request.form['dob']
        address = request.form['Address']
        phno = request.form['phno']
        email = request.form['user_email']
        User.update_profile(name, dob, address, phno, email, curr_user.id)
        record = User.get_user_details(email)
        curr_user.set_user(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
        return redirect(url_for('profile'))
    return redirect(url_for('editprofile'))

@app.route("/editpost/<int:postid>")
@login_required
def editpost(postid):
    records = Query.get_post_postid(postid)
    return render_template("editpost.html", logged = curr_user.get_user(), records = records)

@app.route("/editquery/<int:postid>", methods = ["POST"])
@login_required
def editquery(postid):
    records = Query.get_post_postid(postid)
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['msg']
        anony = request.form.get('anony')
        if anony != "True":
            anony = "False"
        Query.update_post(title, desc, anony, postid)
        records = Query.get_post_postid(postid)
        return render_template("editpost.html", info = "You post have been updated and sent to moderation. It will be approved in 24 hours.",
                               logged = curr_user.get_user(), records = records)
    return render_template("editpost.html", logged = curr_user.get_user(), records = records)

@app.route("/deletepost/<int:postid>")
@login_required
def deletepost(postid):
    Query.delete_query(postid)
    return redirect(url_for('profile'))

admin_user = AdminUSER()
@app.route("/adminlogin")
@login_required
def adminLogin():
    records = Admin.get_admin()
    for record in records:
        if curr_user.id in record:
            admin_user.set_login()
            return redirect("admin")
    return redirect(url_for("index"))

@app.route("/approve/<int:postid>", methods = ["POST"])
@login_required
def approve(postid):
    if request.method == "POST":
        ageres = request.form.get('ageres')
        if ageres != "True":
            ageres = "False"
        Admin.post_approve(postid, "False", "True", ageres)
        return redirect(url_for('admin'))
    return redirect(url_for("admin"))

@app.route("/disapprove/<int:postid>")
@login_required
def disapprove(postid):
    Admin.post_approve(postid, "False", "False", "False")
    return redirect(url_for('admin'))

@app.route("/reqdone/<int:reqid>", methods = ["POST"])
@login_required
def reqdone(reqid):
    if request.method == 'POST':
        done = request.form.get('done')
        if done != "True":
            done = "False"
        Admin.req_completed(reqid, done)
        return redirect(url_for("admin"))
    return redirect(url_for("admin"))

@app.route("/admin")
@login_required
def admin():
    if admin_user.get_status():
        records = Admin.get_posts()
        req = Expreq.get_expert_req()
        return render_template("admin.html", logged = curr_user.get_user(), records = records, req = req)
    else:
        return redirect(url_for('index'))

@app.route("/adminlogout")
@login_required
def adminLogout():
    admin_user.set_logout()
    return redirect(url_for("index"))

@app.route('/logout')
def logout():
    logout_user()
    curr_user.user_out()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(userid):
    return LoginUser(userid)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)
    session.modified = True
    g.user = current_user

if __name__=='__main__':
    app.run(debug=True)