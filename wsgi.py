# hello world uwsgi file

def application(env, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	return [b"<h1 style='color:blue'>Hello World</h1>"] #the b is needed for python3, bytes()
