import sys
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, make_server

from app import application


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8301
    host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
    server = make_server(host, port, application, server_class=ThreadingWSGIServer)
    sys.stderr.write("votacio escoltant a %s:%d\n" % (host, port))
    sys.stderr.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    main()
