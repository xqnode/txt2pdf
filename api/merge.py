"""
Vercel Serverless Function: 合并多个 PDF 片段
前端分片上传时，每片生成一个 PDF，最终调用此接口合并
优先接收 multipart/form-data:
  - filename: xxx
  - chunks: <pdf blob> (可重复多次)
也兼容旧版 JSON: { "chunks": ["base64pdf1", "base64pdf2", ...], "filename": "xxx" }
"""

from http.server import BaseHTTPRequestHandler
from pypdf import PdfWriter, PdfReader
import io
import json
import base64
import urllib.parse
import cgi


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
            # 合并请求最大接受 20MB
            if length > 20 * 1024 * 1024:
                self._error(413, '合并数据过大')
                return

            content_type = self.headers.get('Content-Type', '')
            filename = 'document'
            chunk_streams = []

            if 'multipart/form-data' in content_type:
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={
                        'REQUEST_METHOD': 'POST',
                        'CONTENT_TYPE': content_type,
                        'CONTENT_LENGTH': str(length),
                    },
                )
                filename = form.getfirst('filename', 'document')
                files = form['chunks'] if 'chunks' in form else []
                if not isinstance(files, list):
                    files = [files]
                chunk_streams = [f.file.read() for f in files if getattr(f, 'file', None)]
            else:
                body = json.loads(self.rfile.read(length))
                filename = body.get('filename', 'document')
                chunk_streams = [
                    base64.b64decode(chunk_b64)
                    for chunk_b64 in body.get('chunks', [])
                ]

            if not chunk_streams:
                self._error(400, '没有提供 PDF 片段')
                return

            writer = PdfWriter()
            for pdf_bytes in chunk_streams:
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
