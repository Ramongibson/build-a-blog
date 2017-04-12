import webapp2
import os
import jinja2
from google.appengine.ext import db



template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                        autoescape = True)
                        
class Post(db.Model):
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
class BlogHandler(webapp2.RequestHandler):
 def get(self):
        t = jinja_env.get_template("blog.html")
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        content = t.render(posts = posts)
        self.response.write(content)

class PostHandler(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template("newpost.html")
        content = t.render()
        self.response.write(content)
        
        
    def post(self):
        
        title = self.request.get("title")
        post = self.request.get("post")
        
        if post and title:
            a = Post(title = title, post = post)
            a.put()
            blog_post = a.key().id()
            self.redirect("/blog/%s" % blog_post)
        else:
            error = "Title and body required!"
            t = jinja_env.get_template("newpost.html")
            content = t.render(error = error, title = title, post = post)
            self.response.write(content)
            
class ViewPostHandler(webapp2.RequestHandler):
    def renderError(self, error_code):
        self.error(error_code)
        self.response.write("Oops! Something went wrong.")
        
    def get(self, id):
        posts = Post.get_by_id(int(id))
        if posts:
            t = jinja_env.get_template("blog.html")
            content = t.render(posts = [posts])
            self.response.write(content)
        else:
            self.renderError(400)
        
        

        
       
        
    
      
        
            

app = webapp2.WSGIApplication([
    ('/blog/newpost', PostHandler),("/blog", BlogHandler),webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
