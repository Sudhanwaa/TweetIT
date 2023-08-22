from flask import Flask,render_template,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship,Session,sessionmaker
from flask_restful import Resource,Api
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import UnmappedInstanceError
from datetime import date,datetime
from sqlalchemy.ext.declarative import declarative_base
import random

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///D:/Blog Lite Application/21f1002810/data.sqlite3" 
db=SQLAlchemy(app)

engine = create_engine("sqlite:///D:/Blog Lite Application/21f1002810/data.sqlite3")

class User(db.Model):
    __tablename__="credentials"
    user_id=db.Column(db.Integer,nullable=False,autoincrement=True,primary_key=True)
    username=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    
class Followers(db.Model):
    __tablename__="followers"
    srno=db.Column(db.Integer,nullable=False,autoincrement=True,primary_key=True)
    user_id= db.Column(db.Integer,nullable=False)
    person_id =db.Column(db.Integer,nullable=False)
    
class Post(db.Model):
    __tablename__="posts"
    user_id=db.Column(db.Integer,nullable=False)
    post_id=db.Column(db.Integer,nullable=False,autoincrement=True,primary_key=True)
    post_title=db.Column(db.String,nullable=False)
    post_content=db.Column(db.String,nullable=False)
    time=db.Column(db.String,nullable=False)
    
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/new_acc",methods=["POST","GET"])
def new_account():
    return render_template("new_account.html")
    
@app.route("/add_user",methods=["POST","GET"])
def add_user():
    # Checking if username already exists
    user_name=request.form["user_name"]
    password=request.form["password"]
    user=User.query.filter(User.username==user_name).all()
    
    # if(len(user_name)>10):
    #     return render_template("more_chars.html")    
    try:  
        Session = sessionmaker(bind = engine)
        session=Session()
        data=User(username=user_name,password=password)
        session.add(data)
        session.commit()
        session.close()
    except:
        return render_template("exists.html")
    
    
    return render_template("added_user.html")

@app.route("/home",methods=["POST","GET"])
def home():
    user_name=request.form["user_name"]
    password=request.form["password"]
    user=User.query.filter(User.username==user_name).all()
    if(len(user)==0):
        return render_template("no_account_found.html")
    user_id=user[0].user_id
    
    
    all_posts=Post.query.filter(Post.user_id==user_id).all()
    followers_query=Followers.query.filter(Followers.person_id==user_id).all()
    following_query=Followers.query.filter(Followers.user_id==user_id).all()
    # Finding the number of posts by the user
    if(len(all_posts)==0):
        no_of_posts=0
    if(len(all_posts)!=0):
        no_of_posts=len(all_posts)
        
    # Finding the number of followers that the user has
    if(len(followers_query)==0):
        followers=0
    if(len(followers_query)!=0):
        followers=len(followers_query)
        
    if(len(following_query)==0):
        following=0
    if(len(following_query)!=0):
        following=len(following_query)
    
    
    if(len(user)==0):
        return render_template("no_account_found.html")
    
    today=date.today()
    
    day=today.day
    
    
    
    
    if(user[0].username==user_name and user[0].password==password):
        # From here we go to the homepage
        return render_template("home.html",no_of_posts=no_of_posts,followers=followers,user_id=user_id,posts=all_posts,following=following,day=day)   
    
    if(user[0].username==user_name and user[0].password!=password):
        return render_template("wrong_password.html") 
    

@app.route("/define_post/<int:user_id>",methods=["POST","GET"])
def define_post(user_id):
    return render_template("define_post.html",user_id=user_id)

@app.route("/add_post/<int:user_id>",methods=["POST","GET"])
def add_post(user_id):
    dates={1:"January" ,2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
    post_title=request.form["post_title"]
    post_content=request.form["post_content"]
    curr_date=date.today()
    curr_date=str(curr_date)
    temp=curr_date.split("-")
    time=temp[2]+"-"+dates[int(temp[1])]+"-" +temp[0]
    # print(time)
    
    
    try:  
        Session = sessionmaker(bind = engine)
        session=Session()
        new_post=Post(user_id=user_id,post_title=post_title,post_content=post_content,time=time)
        session.add(new_post)
        session.commit()
        session.close()
    except:
        return render_template("error.html")
    
    
    return render_template("post_successfully_added.html",user_id=user_id)

@app.route("/load_posts/<int:user_id>",methods=["POST","GET"])
def load_posts(user_id):
    all_posts=Post.query.filter(Post.user_id==user_id).all()
    followers_query=Followers.query.filter(Followers.person_id==user_id).all()
    following_query=Followers.query.filter(Followers.user_id==user_id).all()
    # Finding the number of posts by the user
    if(len(all_posts)==0):
        no_of_posts=0
    if(len(all_posts)!=0):
        no_of_posts=len(all_posts)
        
    # Finding the number of followers that the user has
    if(len(followers_query)==0):
        followers=0
    if(len(followers_query)!=0):
        followers=len(followers_query)
        
    if(len(following_query)==0):
        following=0
    if(len(following_query)!=0):
        following=len(following_query)
    today=date.today()
    
    day=today.day
    return render_template("home.html",no_of_posts=no_of_posts,followers=followers,user_id=user_id,posts=all_posts ,following=following,day=day)   
    
@app.route("/delete_post/<int:post_id>/<int:user_id>",methods=["POST","GET","PUT"])
def delete_post(post_id,user_id):
    all_posts=Post.query.filter(Post.user_id==user_id).all()
    follow=Followers.query.filter(Followers.user_id==user_id).all()

    # Finding the number of posts by the user
    if(len(all_posts)==0):
        no_of_posts=0
    if(len(all_posts)!=0):
        no_of_posts=len(all_posts)
        
    # Finding the number of followers that the user has
    if(len(follow)==0):
        followers=0
    if(len(follow)!=0):
        followers=len(follow)
        
    try:  
        Session = sessionmaker(bind = engine)
        session=Session()
        post=Post.query.filter(Post.post_id==post_id).first()
        # print(post.post_title)
        db.session.delete(post)
        db.session.commit()

        return render_template("post_successfully_deleted.html",user_id=user_id)  
    
    except:
        return render_template("error.html")


@app.route("/update_post_form/<int:post_id>",methods=["POST","GET","PUT"])
def update_post_form(post_id):
    # print("Sudhanwa")
    
    all_posts=Post.query.filter(Post.post_id==post_id).all()
    prev_title=all_posts[0].post_title
    prev_content=all_posts[0].post_content
    user_id=all_posts[0].user_id
    return render_template("update_post.html",post_id=post_id,prev_title=prev_title,prev_content=prev_content,user_id=user_id)
    
@app.route("/update_post/<int:post_id>",methods=["POST","GET","PUT"])
def update_post(post_id):
    
    all_posts=Post.query.filter(Post.post_id==post_id).all()
    user_id=all_posts[0].user_id
    
    new_title=request.form["new_post_title"]
    new_content=request.form["new_post_content"]
    
    all_posts=Post.query.filter(Post.user_id==user_id).all()
    followers_query=Followers.query.filter(Followers.person_id==user_id).all()
    following_query=Followers.query.filter(Followers.user_id==user_id).all()
    # Finding the number of posts by the user
    if(len(all_posts)==0):
        no_of_posts=0
    if(len(all_posts)!=0):
        no_of_posts=len(all_posts)
        
    # Finding the number of followers that the user has
    if(len(followers_query)==0):
        followers=0
    if(len(followers_query)!=0):
        followers=len(followers_query)
        
    if(len(following_query)==0):
        following=0
    if(len(following_query)!=0):
        following=len(following_query)
    today=date.today()
    
    day=today.day
    try:
        Session = sessionmaker(bind = engine)
        session=Session()
        post=Post.query.filter(Post.post_id==post_id).first()
        post.post_title=new_title
        post.post_content=new_content
        db.session.commit()
        return render_template("home.html",no_of_posts=no_of_posts,followers=followers,user_id=user_id,posts=all_posts,following=following,day=day)  

    except:
        return render_template("error.html")
    
@app.route("/search/<int:user_id>",methods=["POST","GET"])
def search(user_id):
    search_username=request.form["search_name"]
    
    users=User.query.all()
    users_list=[]
    
    for i in range(len(users)):
        if search_username in users[i].username:
            users_list.append(users[i])
    
    followers=Followers.query.filter(Followers.user_id==user_id).all()
    following_list=[]
    
    for i in followers:
        following_list.append(i.person_id)
    
    # print(following_list)

    return render_template("searches.html",users_list=users_list,user_id=user_id,followers=followers,following_list=following_list,search_username=search_username)

@app.route("/follow_user/<int:user_id>/<int:person_id>/<string:search_username>",methods=["POST","GET"])
def follow_user(user_id,person_id,search_username):
    try:  
        Session = sessionmaker(bind = engine)
        session=Session()
        new_follower=Followers(user_id=user_id,person_id=person_id)
        session.add(new_follower)
        session.commit()
        session.close()
    except:
        return render_template("error.html")
    
    users=User.query.all()
    users_list=[]
    for i in range(len(users)):
        if search_username in users[i].username:
            users_list.append(users[i])
    
    followers=Followers.query.filter(Followers.user_id==user_id).all()
    following_list=[]
    for i in followers:
        following_list.append(i.person_id)
    
    # print(following_list)

    return render_template("searches.html",users_list=users_list,user_id=user_id,followers=followers,following_list=following_list,search_username=search_username)

@app.route("/unfollow_user/<int:user_id>/<int:person_id>/<string:search_username>",methods=["POST","GET"])
def unfollow_user(user_id,person_id,search_username):
    
    try:
        Session = sessionmaker(bind = engine)
        session=Session()
        q=Followers.query.filter(Followers.user_id==user_id).filter(Followers.person_id==person_id).first()
        db.session.delete(q)
        db.session.commit()
    
    except:
        return render_template("error.html")
    
    
    users=User.query.all()
    users_list=[]
    for i in range(len(users)):
        if search_username in users[i].username:
            users_list.append(users[i])
    
    followers=Followers.query.filter(Followers.user_id==user_id).all()
    following_list=[]
    for i in followers:
        following_list.append(i.person_id)
    
    # print(following_list)

    return render_template("searches.html",users_list=users_list,user_id=user_id,followers=followers,following_list=following_list,search_username=search_username)

@app.route("/my_feed/<int:user_id>",methods=["GET"])
def my_feed(user_id):
    
    followers=Followers.query.filter(Followers.user_id==user_id).all()
    # print(followers)
    following_users=[]
    post_content=[]
    for i in followers:
        following_users.append(i.person_id)
        
    
    following_post=[]
    for p_id in following_users:
        following_post.append(Post.query.filter(Post.user_id==p_id).all())
    
    
    temp=[]
    
    for i in following_post:
        for j in i:
            temp.append(j)
            
    following_post=temp
    
    # print(following_post,"following post")
    
    post_content=[]
    acc_info=[]
    temp=[]
    feed_content=[]
    # print(following_post)
    # feed_content--> [[[title,content,time],[username,p_id,user_id]],.....]
    
    for i in following_post:
        # print("sudi")
        post_content.append(i.post_title)
        post_content.append(i.post_content)
        post_content.append(i.time)
        
        
        user=User.query.filter(User.user_id==i.user_id).first()

        user_name=user.username
        acc_info.append(user_name)
        
        acc_info.append(i.user_id)
        acc_info.append(user_id)
        
        temp.append(post_content)
        temp.append(acc_info)
        
        feed_content.append(temp)
        
        post_content=[]
        acc_info=[]
        temp=[]
        
    # print(feed_content,"suadsd")
    
    feed_content.reverse()

    return render_template("my_feed.html",feed_content=feed_content,user_id=user_id)


@app.route("/visit_acc/<int:p_id>/<int:user_id>",methods=["GET"])
def visit_acc(user_id,p_id):
    
    all_posts=Post.query.filter(Post.user_id==p_id).all()
    followers_query=Followers.query.filter(Followers.person_id==p_id).all()
    following_query=Followers.query.filter(Followers.user_id==p_id).all()
    # Finding the number of posts by the user
    if(len(all_posts)==0):
        no_of_posts=0
    if(len(all_posts)!=0):
        no_of_posts=len(all_posts)
        
    # Finding the number of followers that the user has
    if(len(followers_query)==0):
        followers=0
    if(len(followers_query)!=0):
        followers=len(followers_query)
        
    if(len(following_query)==0):
        following=0
    if(len(following_query)!=0):
        following=len(following_query)
    
    username=User.query.filter(User.user_id==p_id).first()
    username=username.username
    
    posts=Post.query.filter(Post.user_id==p_id).all()
    
    return render_template("visit_acc.html",no_of_posts=no_of_posts,followers=followers,following=following,username=username,posts=posts,user_id=user_id)
    
@app.route("/go_home/<int:user_id>",methods=["GET"])
def go_home(user_id):
    
    all_posts=Post.query.filter(Post.user_id==user_id).all()
    followers_query=Followers.query.filter(Followers.person_id==user_id).all()
    following_query=Followers.query.filter(Followers.user_id==user_id).all()
    # Finding the number of posts by the user
    if(len(all_posts)==0):
        no_of_posts=0
    if(len(all_posts)!=0):
        no_of_posts=len(all_posts)
        
    # Finding the number of followers that the user has
    if(len(followers_query)==0):
        followers=0
    if(len(followers_query)!=0):
        followers=len(followers_query)
        
    if(len(following_query)==0):
        following=0
    if(len(following_query)!=0):
        following=len(following_query)
    
    today=date.today()
    day=today.day
    
    
    return render_template("home.html",no_of_posts=no_of_posts,followers=followers,user_id=user_id,posts=all_posts,following=following)

@app.route("/view_followers/<int:user_id>",methods=["GET"])
def view_followers(user_id):
    
    foll=Followers.query.filter(Followers.person_id==user_id).all()
    
    followers_list=[]
    temp=[]
    
        # followers_list--> [[username,user_id],..]
    
    for i in foll:
        temp.append(i.user_id)
        
    temp2=[]
    for i in temp:
        temp2.append((User.query.filter(User.user_id==i).first()).username)
        temp2.append(i)
        followers_list.append(temp2)
        temp2=[]
    
    return render_template("followers.html",followers_list=followers_list,user_id=user_id)


@app.route("/remove_follower/<int:user_id>/<int:person_id>",methods=["GET","POST"])
def remove_follower(user_id,person_id):
    
    
    try:  
        Session = sessionmaker(bind = engine)
        session=Session()
        record=Followers.query.filter(Followers.user_id==person_id).filter(Followers.person_id==user_id).first()
        # print(post.post_title)
        db.session.delete(record)
        db.session.commit()
        foll=Followers.query.filter(Followers.person_id==user_id).all()
    
        followers_list=[]
        temp=[]
        
        # followers_list--> [[username,user_id],..]
        
        for i in foll:
            temp.append(i.user_id)
            
        temp2=[]
        for i in temp:
            temp2.append((User.query.filter(User.user_id==i).first()).username)
            temp2.append(i)
            followers_list.append(temp2)
            temp2=[]

        return render_template("followers.html",followers_list=followers_list,user_id=user_id)
    
    except:
        return render_template("error.html")
    
@app.route("/view_following/<int:user_id>",methods=["GET"])
def view_following(user_id):
    
    foll=Followers.query.filter(Followers.user_id==user_id).all()
    temp=[]
    temp2=[]
    following_list=[]
    
     # following_list--> [[username,user_id],..]
     
    for i in foll:
        temp.append(i.person_id)
    
    for i in temp:
        name=(User.query.filter(User.user_id==i).first()).username
        temp2.append(name)
        temp2.append(i)
        following_list.append(temp2)
        temp2=[]
        
    return render_template("following.html",following_list=following_list,user_id=user_id)


@app.route("/remove_following/<int:user_id>/<int:person_id>",methods=["GET","POST"])
def remove_following(user_id,person_id):
    
    
    try:  
        Session = sessionmaker(bind = engine)
        session=Session()
        record=Followers.query.filter(Followers.person_id==person_id).filter(Followers.user_id==user_id).first()
        # print(post.post_title)
        db.session.delete(record)
        db.session.commit()
        
        foll=Followers.query.filter(Followers.user_id==user_id).all()
        temp=[]
        temp2=[]
        following_list=[]
        
        # following_list--> [[username,user_id],..]
        
        for i in foll:
            temp.append(i.person_id)
        
        for i in temp:
            name=(User.query.filter(User.user_id==i).first()).username
            temp2.append(name)
            temp2.append(i)
            following_list.append(temp2)
            temp2=[]
        
        return render_template("following.html",following_list=following_list,user_id=user_id)
    
    except:
        return render_template("error.html")

@app.route("/delete_account_confirmation/<int:user_id>",methods=["GET","POST"])
def delete_account_confirmation(user_id):
    return render_template("account_delete_confirmation.html",user_id=user_id)

@app.route("/delete_account/<int:user_id>",methods=["GET","POST"])
def delete_account(user_id):
    
    acc=User.query.filter(User.user_id==user_id).first() #Single element
    post=Post.query.filter(Post.user_id==user_id).all()  #Multiple elememts in a list
    follower=Followers.query.filter(Followers.user_id==user_id).all() #Multiple elememts in a list
    following=Followers.query.filter(Followers.person_id==user_id).all() #Multiple elememts in a list
    
    try:
        Session = sessionmaker(bind = engine)
        session=Session()
        # print(post.post_title)
        db.session.delete(acc)
        for obj in post:
            db.session.delete(obj)
        
        for obj in follower:
            db.session.delete(obj)
            
        for obj in following:
            db.session.delete(obj)
            
        db.session.commit()
        
    except:
        return render_template("error.html")
        
    return render_template("account_deleted.html",user_id=user_id)
        
@app.route("/people_you_may_know/<int:user_id>",methods=["GET","POST"])
def people_you_may_know(user_id):
    users=User.query.filter(User.user_id!=user_id).all()
    
    users_list=[]
    
    for i in users:
        users_list.append(i.user_id)
        
    follow=Followers.query.all()
    temp=[]
    
    for i in users_list:
        flag=True
        for j in follow:
            if i==j.person_id and user_id==j.user_id:
                flag=False
                break
        
        if flag:
            temp.append(i)
            
    
    final_user_list=[]
    
    for i in temp:
        q=User.query.filter(User.user_id==i).first()
        final_user_list.append(q)
            
    
    
    return render_template("people_you_may_know.html",users=final_user_list,user_id=user_id)

@app.route("/people_you_may_know_follow/<int:user_id>/<int:p_id>",methods=["GET","POST"])
def people_you_may_know_follow(user_id,p_id):
    
    try:  
        Session = sessionmaker(bind = engine)
        session=Session()
        new_follower=Followers(user_id=user_id,person_id=p_id)
        session.add(new_follower)
        session.commit()
        session.close()
    except:
        return render_template("error.html")
    
    users=User.query.filter(User.user_id!=user_id).all()
    
    users_list=[]
    
    for i in users:
        users_list.append(i.user_id)
        
    follow=Followers.query.all()
    temp=[]
    
    for i in users_list:
        flag=True
        for j in follow:
            if i==j.person_id and user_id==j.user_id:
                flag=False
                break
        
        if flag:
            temp.append(i)
            
    
    final_user_list=[]
    
    for i in temp:
        q=User.query.filter(User.user_id==i).first()
        final_user_list.append(q)
            
    
    return render_template("people_you_may_know.html",users=final_user_list,user_id=user_id)


@app.route("/change_username_form/<int:user_id>",methods=["GET","POST"])
def change_username_form(user_id):
     return render_template("change_username_form.html",user_id=user_id)
 

@app.route("/change_username",methods=["GET","POST"])
def change_username():
    old_username=request.form["previous_username"]
    new_username=request.form["new_username"]
    password=request.form["password"]
    
    user=User.query.filter(User.username==old_username).all()
    
    if(len(user)==0):
        return "No user Found"
    
    if(user[0].password!=password):
        return "Incorrect Password"
    
    else:
        try:
            Session = sessionmaker(bind = engine)
            session=Session()
            user[0].username=new_username
            db.session.commit()
            
        except:
            return "ERROR"
   
    return "USERNAME SUCCESSFULLY CHANGED"
            
        
    
    

    


####################FOR API############################
# CRUD ON USERS
@app.route("/api_add_user/<string:username>/<string:password>",methods=["POST","GET"])
def api_add_user(username,password):
    # Checking if username already exists

    try:  
        Session = sessionmaker(bind = engine)
        session=Session()
        data=User(username=username,password=password)
        session.add(data)
        session.commit()
        session.close()
    except:
        return "ERROR"
    
    
    return "SUCCESS"

@app.route("/api_show_user/<int:user_id>",methods=["POST","GET"])
def api_show_users(user_id):
    
    try:
        user=User.query.filter(User.user_id==user_id).first()
        
        result={
            "Password":user.password,
            "Username":user.username
        }
        
    except:
        return "USERNAME NOT FOUND"
    
    return jsonify(result)

@app.route("/api_update_username/<int:user_id>/<string:new_user_name>",methods=["POST","GET"])
def api_update_username(user_id,new_user_name):
    try:
        Session = sessionmaker(bind = engine)
        session=Session()
        user=User.query.filter(User.user_id==user_id).first()
        user.username=new_user_name
        db.session.commit()
        
    except:
        return "USER NOT FOUND"
   
    return "SUCCESS"

@app.route("/api_delete_account/<int:user_id>",methods=["GET","POST"])
def api_delete_account(user_id):
    
    acc=User.query.filter(User.user_id==user_id).first() #Single element
    post=Post.query.filter(Post.user_id==user_id).all()  #Multiple elememts in a list
    follower=Followers.query.filter(Followers.user_id==user_id).all() #Multiple elememts in a list
    following=Followers.query.filter(Followers.person_id==user_id).all() #Multiple elememts in a list
    
    try:
        Session = sessionmaker(bind = engine)
        session=Session()
        # print(post.post_title)
        db.session.delete(acc)
        for obj in post:
            db.session.delete(obj)
        
        for obj in follower:
            db.session.delete(obj)
            
        for obj in following:
            db.session.delete(obj)
            
        db.session.commit()
        
    except:
        return "ERROR"
        
    return "SUCCESS"


# CRUD ON BLOGS
@app.route("/api_add_post/<string:username>/<string:post_title>/<string:post_content>",methods=["POST","GET"])
def api_add_post(username,post_title,post_content):
    dates={1:"January" ,2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
    curr_date=date.today()
    curr_date=str(curr_date)
    temp=curr_date.split("-")
    time=temp[2]+"-"+dates[int(temp[1])]+"-" +temp[0]
    # print(time)
    users=User.query.filter(User.username==username).all()
    user_id=users[0].user_id
    
    if(len(users)==0):
        return "User not found"
    
    try:  
        Session = sessionmaker(bind = engine)
        session=Session()
        new_post=Post(user_id=user_id,post_title=post_title,post_content=post_content,likes=0,dislikes=0,time=time)
        session.add(new_post)
        session.commit()
        session.close()
        return "SUCCESS"
    except:
        return "Error"

@app.route("/api_show_post/<string:username>",methods=["POST","GET"])
def api_show_post(username):
    users=User.query.filter(User.username==username).all()
    user_id=users[0].user_id
    posts=Post.query.filter(Post.user_id==user_id).all()
    post_titles=[]
    post_contents=[]
    post_dates=[]
    
    for i in posts:
        post_titles.append(i.post_title)
        post_contents.append(i.post_content)
        post_dates.append(i.time)
    
    result={
        "All_Titles": post_titles,
        "All Content": post_contents,
        "All_dates" : post_dates
    }
    

    if(len(users)==0):
        return "User not found"

    return jsonify(result)

@app.route("/api_delete_post/<int:post_id>",methods=["POST","GET","PUT"])
def api_delete_post(post_id):

    try:  
        Session = sessionmaker(bind = engine)
        session=Session()
        post=Post.query.filter(Post.post_id==post_id).first()
        # print(post.post_title)
        db.session.delete(post)
        db.session.commit()

        return "SUCCESS"
        
    except:
        return "ERROR"

@app.route("/api_update_post/<int:post_id>/<string:post_title>/<string:post_content>",methods=["POST","GET","PUT"])
def api_update_post(post_id,post_title,post_content):
    # print("Sudhanwa")
    try:
        Session = sessionmaker(bind = engine)
        session=Session()
        post=Post.query.filter(Post.post_id==post_id).first()
        post.post_title=post_title
        post.post_content=post_content
        db.session.commit()
        
    except:
        return "ERROR"
    
    return "SUCCESS"

######################################################################################

if __name__=='__main__':
    app.debug=True
    app.run()





    
    