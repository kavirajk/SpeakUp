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
session=web.session.Session(app,store,initializer={'login':False,'username':None})
globals_render_t = {
    'session':session
}
render_t=web.template.render("templates",globals=globals_render_t)

globals_t= {
    'session': session,
    'render_t': render_t,
    'datestr':web.datestr
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

        print hexfromdb,hexdigest

        if(hexdigest==hexfromdb):
            print "inside if"
            session.login=True
            session.username=username
            raise web.seeother("/")
        else:
            print "inside else"
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
            status=signup(username,hexdigest)
            print status
            if status==False:
                return render.signup("Username already Exist")

        session.login=True
        session.username=username
        raise web.seeother("/")

class Create:
    def GET(self):
        if session.login:
            return render.create()
        else:
            return "Login before submitting your story"

    def POST(self):
        title=web.input().title
        content=web.input().content

#        print title,content

        status=insert_post(title,content)
        if status:
            raise web.seeother("/")
        else:
            return "Something went wrong!"

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
