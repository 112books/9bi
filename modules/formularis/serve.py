import sys
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, make_server

from app import application


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    #Necessari: wsgiref simple_server atén una petició cada cop. sense fils,
    # mentre s'espera l'SMTP d'un formulari (que pot trigar uns segons) qualsevol
    # altre petició —incloent-hi /health del vigilant— quedaria penjada.
    daemon_threads = True
    allow_reuse_address = True


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8302
    host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
    server = make_server(host, port, application, server_class=ThreadingWSGIServer)
    sys.stderr.write("formularis escoltant a %s:%d\n" % (host, port))
    sys.stderr.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    main()
