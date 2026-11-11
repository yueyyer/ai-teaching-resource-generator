<div align="center">

# AI 智能教学资源生成系统

**简体中文** | [English](README.en.md)

面向乡村教育场景的 AI 教学辅助平台：帮助教师快速生成教案、试卷与多媒体素材，为学生提供讲解、练习与个性化学习路径。

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.46-FF4B4B?logo=streamlit&logoColor=white)
![DashScope](https://img.shields.io/badge/LLM-DashScope-FF6A00)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 它解决什么问题

乡村学校普遍面临师资紧张、备课负担重、优质资源匮乏的问题。教师往往一个人横跨多个学科，写教案、出考题、做课件都要从零开始。这个系统把大模型能力整合成两条工作流：

- **教师端**——输入一个主题，几分钟内拿到结构化的课程大纲、教学 PPT 大纲、练习题、案例分析或实验指导，配套 AI 生成插图、语音朗读素材，一键导出 PDF 并沉淀到资源库；
- **学生端**——提供知识点讲解、自测练习和基于知识图谱的个性化学习路径，把「一个老师对几十个学生」变成每人都能获得针对性的学习指引。

## 功能总览

系统采用教师 / 学生双模块切换设计。

### 教师模块

| 功能 | 说明 |
|------|------|
| 教学内容生成 | 支持课程大纲、教学 PPT、练习题目、案例分析、实验指导 5 类资源；可按学科、学段定制 |
| 多模态输入 | 除文本外，支持语音识别（讯飞流式听写）与图片识别（OCR）作为输入 |
| 多媒体制作 | AI 文生图、语音合成（gTTS）、讯飞 OCR 识图 |
| 资源管理 | SQLite 资源库：保存、搜索、分类、删除，支持资源链接共享 |
| 数据统计 | 资源使用情况统计与可视化 |
| 对话互动 | 基于 LLM 的教学问答助手 |

### 学生模块

| 功能 | 说明 |
|------|------|
| 知识讲解 | 面向学生视角的知识点拆解讲解 |
| 自测练习 | 根据知识点自动出题，即时批改反馈 |
| 个性化学习 | 生成个性化学习路径，并以知识图谱形式可视化呈现 |
| 学习资源搜索 | 资源库检索 + Wikipedia 知识增强 |

### 设计上的一些考量

- **提示词工程**：每类资源对应一套独立的 Prompt 模板（`prompts/` 目录），按学科和学段动态注入参数，输出遵循布鲁姆认知分类的渐进式结构；
- **本地资源沉淀**：所有生成结果存入 SQLite，资源不散落在文件系统里，跨会话可检索复用；
- **多模型接入**：LLM 调用走 OpenAI 兼容协议，可通过环境变量切换 DashScope / OpenAI / 其他兼容模型。

## 快速开始

### 环境准备

- Python 3.11+
- 一个 OpenAI 协议兼容的大模型 API Key（如阿里云百炼 DashScope）
- 讯飞开放平台账号（可选，用于语音听写、OCR、文生图）

### 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/yueyyer/ai-teaching-resource-generator.git
cd ai-teaching-resource-generator

# 2. 安装依赖
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. 配置 API Key
cp .env.example .env
# 编辑 .env，填入你的：
#   OpenAI 兼容模型 Key（阿里云 DashScope 等）
#   讯飞开放平台 APPID / APIKEY / APISECRET（语音、生图、OCR）

# 4. 启动
streamlit run exercise.py
```

浏览器访问 `http://localhost:8501` 即可。

### Docker 运行

```bash
docker build -t ai-teaching .
docker run -p 8501:8501 --env-file .env ai-teaching
```

## 项目结构

```plaintext
ai-teaching-resource-generator/
├── exercise.py            # 主应用入口（教师/学生双模块）
├── prompts/               # 提示词模板（大纲/PPT/练习题等）
│   ├── tabler_prompt.py   # 课程大纲生成
│   ├── dictator_prompt.py # 大纲结构化解析
│   └── quizzy_prompt.py   # 练习题生成
├── word2picture.py        # 文生图 API 封装
├── picture1.py            # 图像处理工具
├── ocr_scenes_demo.py     # OCR 识图
├── 大模型中文语音识别.py       # 讯飞流式语音听写
├── sidebar_css.py         # 侧边栏样式
├── teaching_resources.db  # SQLite 资源库
├── requirements.txt
├── Dockerfile
└── .streamlit/config.toml # Streamlit 主题配置
```

> `app.py` 是项目早期版本的英文课程内容生成器（Automated Course Content Generator），保留作为参考，当前主线入口为 `exercise.py`。

## 技术栈

- **前端界面**：Streamlit + 自定义 CSS（渐变卡片式 UI，见 `.streamlit/config.toml` 主题配置）
- **大模型**：OpenAI SDK 兼容协议，默认对接阿里云 DashScope
- **语音**：讯飞语音听写流式 WebAPI、SpeechRecognition、gTTS 语音合成
- **图像**：讯飞文生图、OCR 识图、Pillow
- **存储**：SQLite（资源库 + 操作日志）
- **部署**：Docker（`python:3.11-slim`）

## 效果截图

> 📌 截图待补充。建议放置：
>
> 1. 教师端「教学内容生成」页——展示输入与生成结果
> 2. 学生端「个性化学习」知识图谱可视化
> 3. 资源管理页
>
> ```markdown
> ![教学内容生成](docs/screenshot-teacher.png)
> ![知识图谱](docs/screenshot-graph.png)
> ```

## Roadmap

- [ ] PPT 直接导出为 .pptx 文件（当前生成大纲内容）
- [ ] 练习题自动批改与错题本
- [ ] 多教师账号与班级管理
- [ ] 离线模型支持（适配网络条件有限的乡村学校）

## License

本项目基于 [MIT License](LICENSE) 开源。

---

<div align="center">
如果这个项目对你有帮助，欢迎点一个 ⭐ Star
</div>
