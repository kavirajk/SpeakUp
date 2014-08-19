import web
import hashlib
from db_model import *

web.config.debug=False

urls=(
    '/','Index',
    '/login','Login',
    '/signup','Signup',
    '/create','Create',
    '/show/(\d+)','Show',
    '/edit/(\d+)','Edit',
    '/delete/(\d+)','Delete',
    '/logout','Logout'
)


app=web.application(urls,globals())
store=web.session.DiskStore('sessions')
session=web.session.Session(app,store,initializer={'login':False,'user':None})
render_t=web.template.render("templates")
globals_t= {
    'content': session,
    'render_t': render_t
}

render=web.template.render("templates",base="base",globals=globals_t)

class Index:
    def GET(self):
        posts=get_all_post()
        return render.index(posts)

class Login:
    def GET(self):
        if session.login:
            return "Already logged in"
            raise web.seeother("/")
        else:
            return render.login(None)

    def POST(self):
        username=web.input().username
        password=web.input().password

        hexdigest=hashlib.sha1(password).hexdigest()

        hexfromdb=get_hexdigest(username)

        if(hexdigest==hexfromdb):
            session.login=True
            raise web.seeother("/")
        else:
            return render.login("Username/Password invalid. Try again")

class Signup:
    def GET(self):
        return render.signup(None)
    def POST(self):
        username=web.input().username
        password=web.input().password
        repassword=web.input().repassword

        if(password!=repassword):
            return render.signup("Password didn't match. Try again")
        else:
            hexdigest=hashlib.sha1(password).hexdigest()
            signup(username,hexdigest)

        session.login=True
        session.user=username
        raise web.seeother("/")

class Create:
    pass

class Show:
    pass

class Edit:
    pass

class Delete:
    pass

class Logout:
    def GET(self):
        session.kill()
        raise web.seeother("/")

if __name__=='__main__':
    app.run()
