import http.server
import socketserver

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    port = 8080
    handler = NoCacheHTTPRequestHandler
    with socketserver.TCPServer(('', port), handler) as httpd:
        print(f'Serving at port {port} with no cache')
        httpd.serve_forever()
