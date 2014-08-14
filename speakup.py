import web
from db_model import *

urls=(
    '/','Index'
)
app=web.application(urls,globals())
render=web.template.render("templates",base="base")

class Index:
    def GET(self):
        posts=get_all_post()
        return render.index(posts)

if __name__=='__main__':
    app.run()
