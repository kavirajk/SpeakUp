import web
import datetime

db=web.database(dbn='mysql',db='SpeakUp',user='root')

def get_all_post():
    result=db.select('entries',order='posted_on DESC')
    return result

def signup(username,hexdigest):
    try:
        db.insert('users',username=username,password=hexdigest)
    except:
        return False
    return True
    
def get_hexdigest(username):
    rows=db.select('users',where='username=$username',vars=locals())
    for row in rows:
        return row.password


def insert_post(title,content,username):
    try:
        db.insert('entries',content=content,posted_on=datetime.datetime.now(),title=title,username=username)
    except:
        return False

    return True

def get_post_by_id(id):
    rows=db.select('entries',where='id=$id',vars=locals())
    for row in rows:
        return row


def update_post_by_id(id,title,content):
    try:
        db.update('entries',where='id=$id',title=title,content=content,vars=locals())
    except:
        return False

    return True


def delete_post_by_id(id):
    try:
        db.delete('entries',where='id=$id',vars=locals())
    except:
        return False

    return True


def get_comments_by_post_id(post_id):
    comments=db.select('comments',where='post_id=$post_id',order='posted_on DESC',vars=locals())
    return comments;


def insert_comment_by_post_id(comment,post_id,username):
    try:
        db.insert('comments',comment=comment,post_id=post_id,posted_on=datetime.datetime.now(),username=username)
    except:
        return False

    return True
