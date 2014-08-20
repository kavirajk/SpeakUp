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


def insert_post(title,content):
    try:
        db.insert('entries',content=content,posted_on=datetime.datetime.utcnow(),title=title)
    except:
        return False

    return True
