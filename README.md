# txt2pdf

[中文](./README.md) | [English](./README.en.md)

![Version](https://img.shields.io/badge/version-v1.0.0-2563eb)
![License](https://img.shields.io/badge/license-MIT-16a34a)
![Deploy](https://img.shields.io/badge/deploy-vercel-000000)
![Chinese Support](https://img.shields.io/badge/chinese-supported-f97316)

一个适合中文内容的在线 `TXT -> PDF` 工具。

支持中文、代码、多语言排版，支持大文件分片转换，并通过浏览器端合并 PDF 来绕开常见 Serverless 请求体限制。

在线体验：

- https://txt2pdf.vercel.app/

仓库地址：

- https://github.com/xqnode/txt2pdf

作者：

- 程序员青戈

## 为什么做这个

很多在线 `txt 转 pdf` 工具在下面这些场景里体验并不好：

- 中文乱码
- 超大 TXT 文件直接失败
- 代码和纯文本混排后样式难看
- 部署到 Serverless 平台后，大文件合并容易撞限制

这个项目就是为了解决这些问题。

## 亮点

- 支持中文 PDF 渲染，默认使用 `STSong-Light CID` 字体
- 支持大文件分片转换，减少单次请求压力
- 浏览器端合并 PDF，避免服务端 merge 请求过大
- 纯前端页面 + Python Function，部署结构简单
- 上传、预览、导出一条龙完成

## 适合谁

- 想把小说 TXT 导出为 PDF 的用户
- 想把代码或日志文本整理成 PDF 的开发者
- 想快速部署一个可在线使用的 `txt2pdf` 工具的人

## 效果预览

![txt2pdf home](./assets/home.png)

![txt2pdf demo](./assets/demo.gif)

项目当前已经包含首页截图与操作演示，后续仍建议补充上传后预览截图与更轻量的视频资源。

## Use Cases

- 将中文小说 TXT 导出为适合阅读或打印的 PDF
- 将代码片段、脚本文件、日志文本整理成 PDF 归档
- 将纯文本资料转换成更适合分享的固定版式文档
- 快速搭建一个可在线使用的 `txt2pdf` 工具站

## 技术方案

大文件处理流程：

```text
前端读取文件（ArrayBuffer 分片，不冻结 UI）
    ↓
按 3MB 切片，逐片 POST /api/convert
    ↓
每片独立生成 PDF
    ↓
浏览器端使用 pdf-lib 合并所有 PDF
    ↓
触发下载最终 PDF
```

核心目录：

```text
txt2pdf/
├── api/
│   ├── convert.py      # 单片文本转 PDF
│   └── merge.py        # 兼容旧合并接口 / 手动合并入口
├── public/
│   └── index.html      # 前端页面
├── requirements.txt    # Python 依赖
└── vercel.json         # Vercel 配置
```

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 安装 Vercel CLI
npm i -g vercel

# 启动本地开发环境
vercel dev
```

打开：

- http://localhost:3000

## 部署到 Vercel

方式一：命令行部署

```bash
vercel
vercel --prod
```

方式二：GitHub 自动部署

1. 推送到 GitHub
2. 在 Vercel 导入仓库
3. 连接项目后自动部署

## Vercel 注意事项

| 项目 | 说明 |
|------|------|
| 单次请求体限制 | Vercel Function 存在请求体大小限制 |
| 单片转换策略 | 当前默认按 `3MB` 切片 |
| 大文件合并策略 | 改为浏览器端合并，避免 `FUNCTION_PAYLOAD_TOO_LARGE` |

如果你的目标是：

- 更大的单文件
- 更长的处理时间
- 更稳定的超大文本导出

建议后续演进到：

- 对象存储
- 队列任务
- 独立后端服务

## 版本

- 当前版本：`v1.0.0`

## Roadmap

- `v1.0.x` 持续优化 README、展示素材与线上体验
- `v1.1.0` 支持更多 PDF 导出样式选项，例如边距、字号、行距
- `v1.2.0` 支持页眉页脚、页码、封面等增强能力
- `v1.3.0` 支持更多文本格式和更细粒度的导出控制
- `v2.0.0` 评估对象存储、任务队列与超大文件后端化处理方案

## License

MIT
