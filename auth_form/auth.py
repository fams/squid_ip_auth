import ssl
from flask import Flask,request,redirect,render_template
import redis




app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)
logins = [('fams','senhafams'),('luis','senhaluis')]

@app.route('/login',methods=["POST","GET"])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'],request.remote_addr,request.form['url'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    url = request.args.get('url') if request.args.get('url') else request.form['url']
    return render_template('login.html', error=error,url=request.args.get('url'))

def valid_login(username,password):
        if((username,password)in logins):
            return True
        else:
            return False
def log_the_user_in(username,remote_addr,url):
    r.set(remote_addr, username)
    return redirect(url, code=302)

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
#ssl.PROTOCOL_SSLv23)
ctx.load_cert_chain('certs/server.crt','certs/server.key')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8443',
            debug=False / True, ssl_context=ctx)


