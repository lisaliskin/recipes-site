#!/usr/bin/env python3
"""Generate PDF via Chrome DevTools Protocol (no header/footer, no margins)."""
import subprocess, json, time, urllib.request, base64, socket, struct, os, sys

CHROME   = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
HTML     = 'file:///Users/lisaliskin/Desktop/recipes-website/scripts/project-overview.html'
OUT      = '/Users/lisaliskin/Desktop/recipes-project-overview.pdf'
PORT     = 9223
TMP_DIR  = '/tmp/chrome-pdf-cdp'


class WS:
    """Minimal WebSocket client (no deps)."""
    def __init__(self, host, port, path):
        self.sock = socket.socket()
        self.sock.settimeout(30)
        self.sock.connect((host, port))
        key = base64.b64encode(os.urandom(16)).decode()
        hs = (f"GET {path} HTTP/1.1\r\n"
              f"Host: {host}:{port}\r\n"
              f"Upgrade: websocket\r\nConnection: Upgrade\r\n"
              f"Sec-WebSocket-Key: {key}\r\n"
              f"Sec-WebSocket-Version: 13\r\n\r\n")
        self.sock.sendall(hs.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.sock.recv(4096)

    def send(self, obj):
        data = json.dumps(obj).encode()
        n = len(data)
        hdr = b'\x81'
        if n < 126:
            hdr += bytes([n | 0x80])
        elif n < 65536:
            hdr += b'\xfe' + struct.pack('>H', n)
        else:
            hdr += b'\xff' + struct.pack('>Q', n)
        mask = os.urandom(4)
        hdr += mask
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        self.sock.sendall(hdr + masked)

    def recv_frame(self):
        def read(n):
            buf = b""
            while len(buf) < n:
                buf += self.sock.recv(n - len(buf))
            return buf
        h = read(2)
        n = h[1] & 0x7f
        if n == 126:
            n = struct.unpack('>H', read(2))[0]
        elif n == 127:
            n = struct.unpack('>Q', read(8))[0]
        return json.loads(read(n))

    def recv_until_id(self, msg_id):
        while True:
            frame = self.recv_frame()
            if frame.get('id') == msg_id:
                return frame

    def close(self):
        self.sock.close()


def wait_for_chrome(port, retries=20):
    for _ in range(retries):
        try:
            urllib.request.urlopen(f'http://localhost:{port}/json/version', timeout=1)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def main():
    proc = subprocess.Popen(
        [CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
         f'--remote-debugging-port={PORT}', f'--user-data-dir={TMP_DIR}'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    try:
        if not wait_for_chrome(PORT):
            print("Chrome не запустился", file=sys.stderr); return

        with urllib.request.urlopen(f'http://localhost:{PORT}/json/list') as r:
            tabs = json.loads(r.read())
        if not tabs:
            with urllib.request.urlopen(f'http://localhost:{PORT}/json/new') as r:
                tabs = [json.loads(r.read())]

        ws_url = tabs[0]['webSocketDebuggerUrl']
        path   = ws_url.split(f'localhost:{PORT}')[1]
        ws     = WS('localhost', PORT, path)

        ws.send({'id': 1, 'method': 'Page.enable'})
        ws.recv_until_id(1)

        ws.send({'id': 2, 'method': 'Page.navigate', 'params': {'url': HTML}})
        ws.recv_until_id(2)

        # Ждём полной загрузки (включая Google Fonts)
        time.sleep(5)

        ws.send({
            'id': 3,
            'method': 'Page.printToPDF',
            'params': {
                'printBackground': True,
                'displayHeaderFooter': False,
                'marginTop': 0,
                'marginBottom': 0,
                'marginLeft': 0,
                'marginRight': 0,
                'paperWidth': 8.27,    # A4 inches
                'paperHeight': 11.69,
                'scale': 1,
            }
        })
        result = ws.recv_until_id(3)
        ws.close()

        if 'error' in result or 'result' not in result:
            print(f"CDP response: {json.dumps(result)}", file=sys.stderr)
            return

        pdf = base64.b64decode(result['result']['data'])
        with open(OUT, 'wb') as f:
            f.write(pdf)
        print(f'Готово: {OUT}  ({len(pdf):,} байт)')

    finally:
        proc.terminate()
        proc.wait()


if __name__ == '__main__':
    main()
