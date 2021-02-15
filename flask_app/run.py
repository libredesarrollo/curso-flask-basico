from my_app import app

#app.config.from_pyfile('config.py')

app.run(ssl_context='adhoc')#debug=True ssl_context=('cert.pem','key.pem')
#app.config['debug']=True
#app.debug=True
