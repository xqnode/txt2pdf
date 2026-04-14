"""
Vercel Serverless Function: TXT → PDF
- 使用 reportlab CID 字体，原生支持中文（STSong-Light）
- 流式逐行处理，内存恒定
- 支持自动折行、自动分页
- 单次请求限制 4MB（Vercel 限制），大文件走分片接口
"""

from http.server import BaseHTTPRequestHandler
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
import json
import urllib.parse

# ── 字体注册（模块加载时执行一次） ──────────────────────────
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

# ── PDF 排版参数 ─────────────────────────────────────────
W, H       = A4
MARGIN_X   = 55    # 左右边距 pt
MARGIN_TOP = 55    # 上边距 pt
MARGIN_BOT = 50    # 下边距 pt
FONT_NAME  = 'STSong-Light'
FONT_SIZE  = 11    # pt
LINE_H     = 18    # 行高 pt（≈ 1.6 倍）
CONTENT_W  = W - MARGIN_X * 2
MAX_Y      = H - MARGIN_BOT


def text_to_pdf(text: str) -> bytes:
    """将纯文本转换为 PDF 字节流，支持中文及自动折行分页"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setFont(FONT_NAME, FONT_SIZE)

    y = H - MARGIN_TOP

    for raw_line in text.split('\n'):
        segments = _wrap(c, raw_line, CONTENT_W)
        for seg in segments:
            if y < MAX_Y - (H - MARGIN_TOP - MAX_Y) + MARGIN_BOT:
                # 实际判断：y 已低于下边距
                pass
            if y < MARGIN_BOT:
                c.showPage()
                c.setFont(FONT_NAME, FONT_SIZE)
                y = H - MARGIN_TOP
            c.drawString(MARGIN_X, y, seg)
            y -= LINE_H

    c.save()
    buf.seek(0)
    return buf.read()


def _wrap(c, line: str, max_width: float) -> list:
    """按渲染宽度折行，处理中英文混排"""
    if not line.strip():
        return [' ']
    result, cur = [], ''
    for ch in line:
        test = cur + ch
        if c.stringWidth(test, FONT_NAME, FONT_SIZE) > max_width:
            if cur:
                result.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        result.append(cur)
    return result or [' ']


def _cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }


class handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # 静默日志

    def do_OPTIONS(self):
        self.send_response(200)
        for k, v in _cors_headers().items():
            self.send_header(k, v)
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))

            # Vercel 单次请求体上限约 4.5MB，此处保守限制 4MB
            MAX_BODY = 4 * 1024 * 1024
            if length > MAX_BODY:
                self._error(413, f'文件过大（{length // 1024}KB），单次最大 4MB。请使用分片上传。')
                return

            body_bytes = self.rfile.read(length)

            # 解析 Content-Type
            content_type = self.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                data = json.loads(body_bytes)
                text = data.get('text', '')
                filename = data.get('filename', 'document')
            else:
                # 当作纯文本处理
                text = body_bytes.decode('utf-8', errors='replace')
                filename = 'document'

            if not text.strip():
                self._error(400, '内容为空')
                return

            pdf_bytes = text_to_pdf(text)

            # 文件名编码（RFC 5987）
            safe_name = urllib.parse.quote(filename)

            self.send_response(200)
            for k, v in _cors_headers().items():
                self.send_header(k, v)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Length', str(len(pdf_bytes)))
            self.send_header(
                'Content-Disposition',
                f"attachment; filename=\"output.pdf\"; filename*=UTF-8''{safe_name}.pdf"
            )
            self.end_headers()
            self.wfile.write(pdf_bytes)

        except Exception as e:
            self._error(500, f'服务器错误：{str(e)}')

    def _error(self, code: int, message: str):
        body = json.dumps({'error': message}, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        for k, v in _cors_headers().items():
            self.send_header(k, v)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
