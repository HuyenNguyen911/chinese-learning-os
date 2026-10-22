"""Máy chủ nhỏ cho trang chủ đề (NN/NN_<tên>.html) của Talk series.

Bấm đúp `Mo-Talk-series.bat` (thư mục Talk series) → script này:
  1. git pull (lấy tiến độ mới nhất từ máy khác)
  2. mở trang chủ đề mới nhất trên trình duyệt qua http://localhost:8765
  3. nhận nút "💾 Lưu + đồng bộ": ghi tick + chat vào khối dữ liệu của trang chủ đề,
     rồi commit ĐÚNG file đó + push. Chỉ push khi repo đang đứng nhánh main.
"""
import http.server
import ipaddress
import json
import re
import socket
import subprocess
import sys
import urllib.parse
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TS = ROOT / "output" / "Giáo trình phát triển Hán ngữ" / "Talk series"
PORT = 8765
DATA_RE = re.compile(r'(<script id="data" type="application/json">)(.*?)(</script>)', re.S)


def git(*args):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout + r.stderr).strip()


def on_main():
    return git("branch", "--show-current")[1] == "main"


def pull():
    if not on_main():
        return "Repo không đứng ở nhánh main → bỏ qua pull."
    code, out = git("pull", "--rebase", "--autostash")
    return "Đã lấy bản mới nhất." if code == 0 else "Pull lỗi: " + out[-300:]


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(TS), **k)

    def allowed(self):
        """Chỉ máy này + thiết bị trong mạng nhà (điện thoại cùng Wi-Fi)."""
        ip = ipaddress.ip_address(self.client_address[0])
        if ip.is_loopback or ip.is_private:
            return True
        self.send_error(403)
        return False

    def do_GET(self):
        if not self.allowed():
            return
        if self.path == "/lan":
            return self.reply({"base": f"http://{lan_ip()}:{PORT}"})
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass

    def reply(self, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if not self.allowed():
            return
        if self.path != "/save":
            return self.send_error(404)
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8"))
        page = (TS / urllib.parse.unquote(req["page"]).lstrip("/")).resolve()
        if TS.resolve() not in page.parents or not re.fullmatch(r"\d\d_.+\.html", page.name) or not page.exists():
            return self.reply({"saved": False, "msg": "Đường dẫn trang không hợp lệ."})

        main = on_main()
        if main:
            code, out = git("pull", "--rebase", "--autostash")
            if code != 0:
                return self.reply({"saved": False, "msg": "Pull lỗi, chưa lưu: " + out[-200:]})

        html = page.read_text(encoding="utf-8")
        m = DATA_RE.search(html)
        data = json.loads(m.group(2))
        data["chat"] = req["chat"]
        data["room_state"] = req["room_state"]
        js = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
        page.write_text(html[: m.start(2)] + "\n" + js + "\n" + html[m.end(2):], encoding="utf-8", newline="")

        if not main:
            return self.reply({"saved": True, "msg": "Đã lưu vào file. CHƯA push vì repo không đứng ở nhánh main."})
        rel = page.relative_to(ROOT).as_posix()
        git("add", "--", rel)
        code, out = git("commit", "-m", f"chore(talk-series): luu tien do {page.parent.name}", "--", rel)
        if code != 0:
            return self.reply({"saved": True, "msg": "Không có gì mới để đẩy lên." if "nothing" in out else "Commit lỗi: " + out[-200:]})
        code, out = git("push")
        return self.reply({"saved": True, "msg": "Đã lưu + đẩy lên git ✓" if code == 0 else "Đã lưu + commit, nhưng push lỗi: " + out[-200:]})


def latest_page():
    pages = sorted(f for d in TS.iterdir() if d.is_dir() and re.fullmatch(r"\d\d", d.name) for f in d.glob(d.name + "_*.html"))
    return pages[-1].relative_to(TS).as_posix() if pages else ""


if __name__ == "__main__":
    print(pull())
    url = f"http://localhost:{PORT}/" + urllib.parse.quote(sys.argv[1] if len(sys.argv) > 1 else latest_page())
    try:
        srv = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    except OSError:
        print("Máy chủ đã chạy sẵn → chỉ mở trang.")
        webbrowser.open(url)
        sys.exit(0)
    print("Mở:", url)
    print("Điện thoại (cùng Wi-Fi): bấm nút 📱 trên trang để quét mã.")
    print("Để cửa sổ này mở trong lúc dùng trang. Đóng cửa sổ = tắt.")
    webbrowser.open(url)
    srv.serve_forever()
