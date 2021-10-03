from .app import db, app
from .models.posts import Post
from .models.users import Users


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'user': Users, 'post': Post}
