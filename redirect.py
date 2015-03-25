import redis
import flask
import re

REDIS_HOST = "localhost"
REDIS_PORT = 6379
AUTH_TOKEN = 'SuperSecureSecretAuthorizationTokenOfSecrecyPlaceholder'

def main():
    app = flask.Flask(__name__)
    redirector = Redirector()

    @app.route('/<path>')
    def routepath(path):
        redirect_to = redirector.get_url_for(path)
        if redirect_to == None:
            flask.abort(404)
        else:
            return flask.redirect(redirect_to, code=303)

    @app.route('/')
    def index():
        return "Hello! Now go away!"

    @app.route("/addpath", methods=["POST", "GET"])
    def addpath():
        url = flask.request.form['url']
        new_path = flask.request.form['new_path']
        security_token = flask.request.form['auth_token']
        redirector.map_path(new_path, url)

    @app.errorhandler(404)
    def page_not_found(e):
        return "404, this page or resource doesn't exist. Major bummer dude.", 404

    app.run()

class Redirector(object):
    def __init__(self):
        self.db = redis.StrictRedis(host="localhost", port=6379)
        self.db.ping()

    def map_path(self, path, url):
        path, url = self.filter(path), self.filter(url)
        self.db.hset("redirects", path, url)
        self.db.save()

    def get_url_for(self, path):
        return self.db.hget("redirects", path)

    def filter(self, input_string):
        if re.match('^[^\w-]+$', input_string) is not None:
            raise PathDoesNotExist

class PathDoesNotExist(Exception):
    pass

if __name__ == "__main__":
    main()
