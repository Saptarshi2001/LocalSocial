from flask import Flask
from flask import Flask
from flask import url_for
from markupsafe import escape
from flask import request
from flask import render_template
from flask import make_response
from flask import abort, redirect, url_for
import praw.exceptions
from setup import consumer_key,consumer_secret,bearer_token,access_secret,access_token,client_id,client_secret,redirect_uri,user_agent,password
import datetime
import argon2
import tweepy
import uuid
import sqlite3
import praw
from createdb import init_db,close_db
app=Flask(__name__,template_folder='templates')
api = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_secret,

)
reddit=praw.Reddit(client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username="DegreeLazy719",
            password=password
            )




@app.route('/socials',methods=['POST','GET'])
def socials():
    return render_template('social.html')




@app.route('/homepage/<username>',methods=['POST','GET'])
def homepage(username):
    #template='templates/home.html'
    
        if request.method=='POST':
            tweet=request.form['twitter']
            name=request.form['heading']
            
            if tweet.isascii() and name.isascii():

                dbconnect=sqlite3.connect("database.db")
                cursors=dbconnect.cursor()
                try:

                    response=api.create_tweet(text=tweet)
                    postid=response.data['id']
                except tweepy.TweepyException as e :
                    return render_template(e)
                cursors.execute('INSERT INTO CREATION VALUES(?,?,?)',(datetime.datetime.now(),username,postid))
                cursors.execute('INSERT INTO POST (POST_ID, POST_NAME, POST_BODY, USERNAME) VALUES (?, ?, ?, ?)',(postid,name,tweet,username))
                dbconnect.commit()
                dbconnect.close()
                return render_template('success.html')
            
            else:

                return '<p>Not a proper tweet</p>'
        else:
            return render_template('homepage.html',username=username)

@app.route('/homepage/reddit/<username>',methods=['POST','GET'])
def homepagereddit(username):
    

    if request.method=='POST':
        print("hello")
        sub=request.form['subreddit']    
        subreddit=reddit.subreddit(sub)
        title=request.form['heading']
        body=request.form['reddit']
        if title.isascii() and body.isascii():
            dbconnect=sqlite3.connect("database.db")
            cursors=dbconnect.cursor()
            try:
                
                submission=subreddit.submit(title,body)
                postid=submission.id
            

            except praw.exceptions.PRAWException as e:
                print(f"Exception {e}")
                return None

            cursors.execute("INSERT INTO REDDITPOST(POST_ID,POST_NAME,POST_BODY,USERNAME) VALUES(?,?,?,?)",(postid,title,body,username))
            cursors.execute("INSERT INTO CREATIONREDDIT(POSTDATE,USERNAME,POSTID) VALUES(?,?,?)",(datetime.datetime.now(),username,postid))
            close_db()
            return render_template("success.html")
            

        return render_template("homereddit.html",username=username)
    else:
        return render_template("homereddit.html",username=username)
    
    



@app.route('/delete',methods=['POST','GET'])
def delete():
    if request.method=='POST':
        post_name=request.form['post_name']
        dbconnect=sqlite3.connect("database.db")
        cursors=dbconnect.cursor()
        cursors.execute('SELECT POST_ID FROM POST WHERE POST_NAME=?',(post_name,))
        acc=cursors.fetchone() 
        if acc:
            cursors.execute('DELETE FROM POST WHERE POST_NAME=?',(post_name,))
            dbconnect.commit()
            close_db(dbconnect)
            id=int(''.join(map(str,acc)))
            try:
                api.delete_tweet(id)
                print("<p>Post deleted</p>")
                return render_template('homepage.html')
            except tweepy.TweepyException as e:
                    return render_template(e)
                    


        close_db(dbconnect)        
        return '<p>Post doesent exists</p>'
    else:
        return render_template('delete.html')

@app.route('/edit',methods=['POST','GET'])
def edit_post():
    if request.method=='POST':
        post_name=request.form['post_name']
        if post_name.isascii():
            dbconnect=sqlite3.connect("database.db")
            cursors=dbconnect.cursor()
            cursors.execute('SELECT POST_ID, POST_BODY FROM POST WHERE POST_NAME=?', (post_name,))
            acc=cursors.fetchone()
            if acc:
                postid,post_body=acc
                print(postid)
                print(post_body)                  
                dbconnect.commit()
                close_db(dbconnect)
                return redirect(url_for('update', postid=postid) + '?post_body=' + post_body)
                
            close_db(dbconnect)            
            return render_template('<p>Post not found</p>')
        else:
            close_db(dbconnect)
            return "<p>Post name not valid </p>"
    else:
        return render_template('update.html')
    
@app.route('/editreddit',methods=['POST','GET'])
def edit_post_reddit():
    if request.method=='POST':
        post_name=request.form['post_name']
        if post_name.isascii():
            dbconnect=sqlite3.connect("database.db")
            cursors=dbconnect.cursor()
            cursors.execute('SELECT POST_ID, POST_BODY FROM REDDITPOST WHERE POST_NAME=?', (post_name,))
            acc=cursors.fetchone()
            if acc:
                postid,post_body=acc
                print(postid)
                print(post_body)                  
                dbconnect.commit()
                close_db(dbconnect)
                return redirect(url_for('updateredditpost', postid=postid) + '?post_body=' + post_body)
                
            close_db(dbconnect)            
            return render_template('<p>Post not found</p>')
        else:
            close_db(dbconnect)
            return "<p>Post name not valid </p>"
    else:
        return render_template('update.html')


@app.route('/update/<postid>', methods=['POST', 'GET'])
def update(postid):
    print(postid)
    post_body=request.args.get('post_body')
    
    if request.method=='POST':
        
        newbody=request.form['tweet']
        
        if newbody.isascii():
            dbconnect=sqlite3.connect("database.db")
            cursors=dbconnect.cursor()
            cursors.execute("UPDATE POST SET POST_BODY=? WHERE POST_ID=? ",(newbody,postid))
            dbconnect.commit()
            close_db(dbconnect)
            api.delete_tweet(postid)
            api.create_tweet(newbody)
            
            return '<p>Post edited</p>'
                 
        else:
            return '<p>Not a valid body </p>'
    
    else:
        return render_template("updatetweet.html",postid=postid,post_body=post_body)
    
@app.route('/updatereddit/<postid>', methods=['POST', 'GET'])
def updateredditpost(postid):
    print(postid)
    post_body=request.args.get('post_body')
    
    if request.method=='POST':
        
        newbody=request.form['reddit']
        
        if newbody.isascii():
            dbconnect=sqlite3.connect("database.db")
            cursors=dbconnect.cursor()
            cursors.execute("UPDATE REDDITPOST SET POST_BODY=? WHERE POST_ID=? ",(newbody,postid))
            dbconnect.commit()
            close_db(dbconnect)
            api.delete_tweet(id=postid)
            api.create_tweet(text=newbody)
            
            return '<p>Post edited</p>'
                 
        else:
            return '<p>Not a valid body </p>'
    
    else:
        return render_template("updatetweet.html",postid=postid,post_body=post_body)


@app.route('/options/<username>',methods=['POST','GET'])
def options(username):
    return render_template("options.html",username=username)

@app.route('/create',methods=['POST','GET'])
def create_account():
    if request.method=='POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email=request.form['email']
        username=request.form['Username']
        password=request.form['Password']
        hshpass=argon2.hash_password(password.encode())
        if first_name.isascii() and last_name.isascii() and email.isascii() and username.isascii() and password.isascii():
            dbconnect=sqlite3.connect("database.db")
            cursors=dbconnect.cursor()
            cursors.execute('INSERT INTO USERS VALUES(?,?,?,?,?)',(first_name,last_name,email,username,hshpass))
            acc=cursors.fetchone()
            dbconnect.commit()
            close_db(dbconnect)
            if acc:
                render_template("<p>Account already present</p>")
                return redirect(url_for('login'))
            
            return redirect(url_for('login'))
        else:
            
            return '<p> Error!! Account not created</p>'
    else:
        return render_template('createaccount.html')




@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        hshpass=argon2.hash_password(password.encode())
        dbconnect=sqlite3.connect("database.db")
        cursors=dbconnect.cursor()
        cursors.execute('SELECT USERNAME FROM USERS WHERE USERNAME=?',(username,))
        acc=cursors.fetchone()
        dbconnect.commit()
        close_db(dbconnect)
        
        if acc:
            return redirect(url_for('options',username=username))
        else:
            
            return '<p> Account not present.Please create an account</p>'

    else:
        return render_template('login.html')

@app.route('/logout',methods=['POST','GET'])    
def logout():

    return render_template('login.html')

