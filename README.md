# TXT 转 PDF — Vercel 部署版

中文完整支持，后端用 reportlab CID 字体渲染，支持 30MB 大文件分片上传。

## 项目结构

```
txt2pdf/
├── api/
│   ├── convert.py      # 单片转换接口（< 3MB/次）
│   └── merge.py        # 多片合并接口
├── public/
│   └── index.html      # 前端页面
├── requirements.txt    # Python 依赖
└── vercel.json         # Vercel 配置
```

## 本地运行（调试用）

```bash
# 安装依赖
pip install reportlab pypdf

# 安装 Vercel CLI
npm i -g vercel

# 本地启动
vercel dev
```

访问 http://localhost:3000 即可使用。

## 部署到 Vercel

### 方式一：命令行（推荐）

```bash
# 首次登录
vercel login

# 部署
vercel

# 生产部署
vercel --prod
```

### 方式二：GitHub 自动部署

1. 把项目推送到 GitHub
2. 打开 https://vercel.com/new
3. 导入仓库，Vercel 自动识别配置，点击 Deploy

## 技术说明

### 中文支持
使用 reportlab 内置 **STSong-Light CID 字体**，无需上传字体文件，
PDF 查看器（Adobe、浏览器、系统预览）均可正确显示中文。

### 大文件处理流程
```
前端读取文件（ArrayBuffer 分片，不冻结 UI）
    ↓
按 3MB 切片，逐片 POST /api/convert
    ↓ 每片独立生成 PDF（Vercel 单次限制 4.5MB）
所有片完成后，POST /api/merge 合并
    ↓ pypdf 按顺序拼接页面
触发浏览器下载最终 PDF
```

### Vercel 限制说明

| 限制项 | 免费版 | Pro 版 |
|--------|--------|--------|
| 函数超时 | 10s | 60s（已在 vercel.json 配置） |
| 请求体大小 | 4.5MB | 4.5MB |
| 分片大小 | 3MB/片 | 3MB/片 |

> **注意**：免费版函数超时为 10 秒，处理单片约 1-2MB 文本没问题。
> 如需处理更大单片，升级 Hobby 计划（$5/月）将超时延长至 60 秒。
