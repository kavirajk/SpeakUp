import web
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
session=web.session.Session(app,store,initializer={'login':False,'userid':None})
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
        session.login=True
        raise web.seeother("/")

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
