import web

db=web.database(dbn='mysql',db='SpeakUp',user='root')

def get_all_post():
    result=db.select('entries')
    return result

def signup(user,hexdigest):
    db.insert('users',userid=user,password=hexdigest)
    
