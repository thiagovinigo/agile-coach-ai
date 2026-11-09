import http.server, socketserver, webbrowser, os, threading
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class Server(socketserver.TCPServer): allow_reuse_address=True
with Server(("127.0.0.1", 0), http.server.SimpleHTTPRequestHandler) as server:
    url="http://127.0.0.1:%d/" % server.server_address[1]
    print("Apresentação: " + url + "\nMantenha esta janela aberta. Feche-a para encerrar.", flush=True)
    threading.Timer(.5,lambda:webbrowser.open(url)).start()
    try: server.serve_forever()
    except KeyboardInterrupt: pass
