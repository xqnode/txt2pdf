"""
Vercel Serverless Function: 合并多个 PDF 片段
前端分片上传时，每片生成一个 PDF，最终调用此接口合并
接收 JSON: { "chunks": ["base64pdf1", "base64pdf2", ...], "filename": "xxx" }
"""

from http.server import BaseHTTPRequestHandler
from pypdf import PdfWriter, PdfReader
import io
import json
import base64
import urllib.parse


def _cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }


class handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_OPTIONS(self):
        self.send_response(200)
        for k, v in _cors_headers().items():
            self.send_header(k, v)
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            # 合并请求最大接受 20MB（多个 PDF base64 编码后约 1.33x 大小）
            if length > 20 * 1024 * 1024:
                self._error(413, '合并数据过大')
                return

            body = json.loads(self.rfile.read(length))
            chunks = body.get('chunks', [])
            filename = body.get('filename', 'document')

            if not chunks:
                self._error(400, '没有提供 PDF 片段')
                return

            writer = PdfWriter()
            for chunk_b64 in chunks:
                pdf_bytes = base64.b64decode(chunk_b64)
                reader = PdfReader(io.BytesIO(pdf_bytes))
                for page in reader.pages:
                    writer.add_page(page)

            out = io.BytesIO()
            writer.write(out)
            pdf_bytes = out.getvalue()

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
            self._error(500, f'合并失败：{str(e)}')

    def _error(self, code, message):
        body = json.dumps({'error': message}, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        for k, v in _cors_headers().items():
            self.send_header(k, v)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
