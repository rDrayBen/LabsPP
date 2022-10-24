from waitress import serve
import hello
serve(hello.app, host='127.0.0.1', port=10000)
