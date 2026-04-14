# txt2pdf

[中文](./README.md) | [English](./README.en.md)

An online `TXT -> PDF` tool built for Chinese text, source code, and large plain-text files.

It supports Chinese rendering, code-friendly layout, chunked conversion for large files, and browser-side PDF merging to avoid common Serverless payload limits.

Live demo:

- https://txt2pdf.vercel.app/

Repository:

- https://github.com/xqnode/txt2pdf

Author:

- 程序员青戈

## Why this project

Many online `txt to pdf` tools fail in real-world scenarios such as:

- broken Chinese text rendering
- large TXT files failing to process
- poor formatting for code and mixed text
- Serverless deployments breaking on large merge requests

This project is built to solve those problems with a lightweight deployable architecture.

## Highlights

- Proper Chinese PDF rendering using `STSong-Light CID`
- Chunked conversion flow for large text files
- Browser-side PDF merge to avoid oversized backend payloads
- Simple deployment model: static frontend + Python functions
- Upload, preview, convert, and download in one page

## Best for

- readers converting TXT novels to PDF
- developers exporting code or logs as PDF
- builders who want a deployable `txt2pdf` tool on Vercel

## Preview

![txt2pdf demo](./assets/demo.gif)

Recommended future additions:

- homepage screenshot
- uploaded TXT preview screenshot
- a lighter demo GIF / MP4

These assets can improve click-through and GitHub stars significantly.

## How it works

Large file flow:

```text
Frontend reads the file in chunks
    ↓
Split text into 3MB chunks
    ↓
POST each chunk to /api/convert
    ↓
Each chunk becomes a PDF
    ↓
Browser merges all PDFs with pdf-lib
    ↓
Final PDF download
```

Project structure:

```text
txt2pdf/
├── api/
│   ├── convert.py      # Convert a text chunk into PDF
│   └── merge.py        # Legacy/manual merge endpoint
├── public/
│   └── index.html      # Frontend page
├── requirements.txt    # Python dependencies
└── vercel.json         # Vercel config
```

## Local development

```bash
pip install -r requirements.txt
npm i -g vercel
vercel dev
```

Open:

- http://localhost:3000

## Deploy to Vercel

Option 1: CLI

```bash
vercel
vercel --prod
```

Option 2: GitHub integration

1. Push the repository to GitHub
2. Import it into Vercel
3. Let Vercel build and deploy automatically

## Notes about Vercel

| Item | Notes |
|------|------|
| Request body limit | Vercel Functions have request payload limits |
| Chunk strategy | This project currently uses `3MB` chunks |
| Large-file merge strategy | Final PDF merge happens in the browser to avoid `FUNCTION_PAYLOAD_TOO_LARGE` |

If you need:

- much larger files
- longer processing time
- more reliable huge-text export

you should consider evolving this into:

- object storage
- job queues
- a dedicated backend service

## Version

- Current version: `v1.0.0`

## License

MIT
