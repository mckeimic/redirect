import redis
import flask
import re

REDIS_HOST = "localhost"
REDIS_PORT = 6379
AUTH_TOKEN = 'SuperSecureSecretAuthorizationTokenOfSecrecyPlaceholder'

def main():
    redirector = Redirector()
    app = flask.Flask(__name__)

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

    @app.route("/add", methods=["POST", "GET"])
    def addpath():
        if flask.request.method == "GET":
            return flask.render_template("add.html")
        else:
            security_token = flask.request.form['auth_token']
            if authorize(security_token):
                url = "http://{}".format(flask.request.form['url'])
                new_path = flask.request.form['new_path']
                timeout = int(flask.request.form['expire_time'])
                redirector.map_path(new_path, url, expire_time=timeout)
                return "Success! {} now directs to {} and will expire after {} seconds".format(
                        new_path, url, timeout, security_token)
            else:
                return "Bad authorization token", 403

    @app.errorhandler(404)
    def page_not_found(e):
        return "404, this page or resource doesn't exist. Major bummer dude.", 404

    app.run(host="0.0.0.0", port=80)

def authorize(auth_token):
    return auth_token == AUTH_TOKEN

class Redirector(object):
    def __init__(self):
        self.db = redis.StrictRedis(host="localhost", port=6379)
        self.db.ping()

    def map_path(self, path, url, expire_time=0):
        path, url = self.filter(str(path)), self.filter(str(url))
        key = "redirect:{}".format(path)
        self.db.set(key, url)
        if expire_time != 0:
           self.db.expire(key, expire_time)
        self.db.save()

    def get_url_for(self, path):
        path = self.filter(str(path))
        url = self.db.get("redirect:{}".format(path))
        return url

    def filter(self, input_string):
        if re.match('^[^\w-]+$', input_string) is not None:
            raise PathDoesNotExist
        return input_string

class PathDoesNotExist(Exception):
    pass

if __name__ == "__main__":
    main()
