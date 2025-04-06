from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os

class ChatHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/list_chats':
            # Get list of chat files
            chat_files = [f for f in os.listdir('chats') if f.endswith('.json')]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(chat_files).encode())
        elif self.path.startswith('/chats/'):
            # Handle request for specific chat
            chat_file = self.path[7:]  # Remove '/chats/' from path
            chat_path = os.path.join('chats', chat_file)
            
            if os.path.exists(chat_path):
                with open(chat_path, 'r', encoding='utf-8') as f:
                    chat_data = json.load(f)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(chat_data).encode())
            else:
                self.send_error(404, "Chat not found")
        else:
            # Use default handler for all other requests
            return SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        # Добавляем CORS заголовки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        SimpleHTTPRequestHandler.end_headers(self)

def run(server_class=HTTPServer, handler_class=ChatHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Запуск сервера на порту {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run() 