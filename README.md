# txt2pdf

[中文](./README.md) | [English](./README.en.md)

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

![txt2pdf demo](./assets/demo.gif)

建议后续继续补充：

- 首页截图
- 上传 TXT 后的预览截图
- 更轻量的演示 GIF / MP4

这样更容易在 GitHub 首页获得点击和 Star。

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

## License

MIT
