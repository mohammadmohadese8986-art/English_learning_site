# سرور ساده پایتون برای پروژه آموزش زبان
# اجرا: python app.py
# آدرس: http://localhost:8000
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pathlib import Path

folder = Path(__file__).parent
page = (folder / "index.html").read_text(encoding="utf-8")

class Handler(BaseHTTPRequestHandler):
    def send_data(self, data, kind):
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.send_data(page.encode("utf-8"), "text/html; charset=utf-8")

    def do_POST(self):
        if self.path != "/quiz":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(length).decode("utf-8"))
        answer = form.get("answer", [""])[0]
        msg = "آفرین! پاسخ درست است." if answer == "کتاب" else "پاسخ درست «کتاب» است. دوباره تمرین کن."
        result = f"""<!doctype html><html lang="fa" dir="rtl"><meta charset="utf-8">
        <body style="font-family:Tahoma;text-align:center;padding:50px;color:#102a56">
        <h2>نتیجه آزمون</h2><p>{msg}</p><a href="/">بازگشت به سایت</a></body></html>"""
        self.send_data(result.encode("utf-8"), "text/html; charset=utf-8")

print("سایت اجرا شد: http://localhost:8000")
HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
