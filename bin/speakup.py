import web
import hashlib
from db_model import *
import datetime

web.config.debug=False

urls=(
    '/','Index',
    '/login','Login',
    '/signup','Signup',
    '/create','Create',
    '/show/(\d+)','Show',
    '/edit/(\d+)','Edit',
    '/delete/(\d+)','Delete',
    '/logout','Logout',
    '/comment/(\d+)','Comment'
)


app=web.application(urls,globals())
store=web.session.DiskStore('sessions')
session=web.session.Session(app,store,initializer={'login':False,'username':None})
globals_render_t = {
    'session':session
}
render_t=web.template.render("templates",globals=globals_render_t)

globals_t= {
    'datetime': datetime,
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
            return render.create(message=None,title=None,content=None)
        else:
            return "Login before submitting your story"

    def POST(self):
        title=web.input().title
        content=web.input().content

        actual_title=''.join(title.split())
        actual_content=''.join(content.split())

        if(actual_title == '' or actual_content == ''):
            return render.create("Title/Content can't be empty.",title=title,content=content)

        status=insert_post(title,content,session.username)
        if status:
            raise web.seeother("/")
        else:
            return "Something went wrong!"

class Show:
    def GET(self,id):
        post=get_post_by_id(int(id))
        comments=get_comments_by_post_id(int(id))
        return render.show(post=post,comments=comments,message=None)
class Edit:
        
    def GET(self,id):
        if session.login == False:
            return "UnAuthorized"

        post=get_post_by_id(int(id));
        return render.edit(post=post,message=None)

    def POST(self,id):
        if session.login == False:
            return "UnAuthorized"
            
        title=web.input().title
        content=web.input().content
        
        actual_title=''.join(title.split())
        actual_content=''.join(content.split())

        post=get_post_by_id(int(id))

        if(actual_title == '' or actual_content==''):
            return render.edit(post=post,message="Title/Content can't be empty")

        status=update_post_by_id(id=id,title=title,content=content)

        if status is False:
            return "Something went wrong while updating '%s'",title

        raise web.seeother("/")

class Delete:
    def GET(self,id):
        if session.login == False:
            return "UnAuthorized"
        post=get_post_by_id(int(id))
        return render.delete(post=post,message=None)

    def POST(self,id):
        if session.login == False:
            return "UnAuthorized"
        post=get_post_by_id(int(id))
        status=delete_post_by_id(int(id))
        if status is False:
            return "Something went wrong while deleting '%s' " %post.title
        raise web.seeother("/")

class Comment:
    def POST(self,post_id):
        if session.login == False:
            return "UnAuthorized"
        comment=web.input().comment
        status=insert_comment_by_post_id(comment,post_id,session.username)

        if status == False:
            return "Something wrong while inserting comment in db"
            
        path="/show/%d#comments" % int(post_id)
        raise web.seeother(path)

class Logout:
    def GET(self):
        session.kill()
        raise web.seeother("/")

if __name__=='__main__':
    app.run()
