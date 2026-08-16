# write-tech-wechat-article

一个把模糊的 AI、Agent、模型、开发者工具或科技产品选题，做成可直接进入微信公众号编辑器的中文深度稿 Codex Skill。

它不只负责“写一篇文章”，还会依次完成选题收敛、资料研究、结构设计、竞品比较、正文写作、统一配图、公众号排版和发布前检查。

## 能做什么

- 在没有初稿时，通过逐题选择确定文章的核心收获、读者、切入点和立场
- 使用官方文档、官方仓库、许可证和原始论文核验现实产品信息
- 按相同维度比较 Codex、Claude Code、DeepSeek 等产品或技术路线
- 把研究结果组织成有观点、有层次的中文科技深度稿
- 改写已有初稿，补足结构、证据、边界和作者判断
- 规划封面、架构图、流程图、对比图和正文插图
- 生成可复制到微信公众号编辑器的 HTML 排版版
- 检查英文产品名、大小写、颜色、链接和图片顺序
- 按需生成 Markdown、HTML、Word 和 ZIP 发布包

## 安装

将仓库克隆到 Codex 的个人 Skills 目录：

```bash
git clone https://github.com/HurmitLI/write-tech-wechat-article.git ~/.codex/skills/write-tech-wechat-article
```

安装后，可在 Codex 中通过 `$write-tech-wechat-article` 显式调用。

## 使用示例

只有一个模糊选题：

```text
$write-tech-wechat-article 我想写一篇关于多 Agent 开发的公众号文章，但不知道从哪里切入
```

已经确定主题，希望先看提纲：

```text
$write-tech-wechat-article 研究 Codex、Claude Code 和 GitHub Copilot 的多 Agent 路线，先给我一份详细提纲
```

已有初稿，希望补强：

```text
$write-tech-wechat-article 改写这份科技稿，补足事实依据、竞品比较、配图和公众号排版
```

只需要公众号交付物：

```text
$write-tech-wechat-article 把这篇完整稿做成公众号粘贴版 HTML，并生成封面和正文配图
```

## 工作流程

### 1. 确定文章方向

如果用户只有一句想法，Skill 会一次只确认一个会改变文章走向的问题，逐步确定：

1. 读者最重要的收获
2. 最值得展开的产品或架构优势
3. 读者需要理解到的深度
4. 正文从哪个问题或矛盾进入
5. 作者的态度和判断强度
6. 下一步先看提纲还是直接成稿

已有答案会自动跳过，不会重复追问。

### 2. 研究与事实核验

涉及产品版本、开源范围、许可、价格、跑分或公司声明时，会优先使用：

- 官方发布页
- 官方文档
- 官方代码仓库
- 开源许可证
- 原始论文

文章会区分来源事实、合理推断和作者判断，并记录资料检索日期。没有可靠资料时，会缩小结论，不编造数据、引语或用户案例。

### 3. 搭建文章层次

默认结构不是按厂商依次写产品说明书，而是围绕问题和共同维度组织：

1. 用真实问题制造阅读动机
2. 解释核心概念
3. 建立共同比较维度
4. 展开关键差异
5. 落到产品或企业场景
6. 说明代价、限制和适用边界
7. 回答开头问题并给出作者判断

### 4. 写成自然中文

默认面向产品经理和 AI 从业者，避免行业大背景式开场、商业黑话、口号和机械排比。正文让事实、解释和判断交替出现，每一段都必须增加新的信息。

### 5. 统一视觉与排版

一篇 4000–8000 字的深度稿，默认规划 3–5 张正文图和 1 张封面：

- 精确架构图、流程图和对比图优先使用矢量或代码绘图
- 编辑插画和封面使用图像生成能力
- 正文图保持统一画幅、配色、线条和字体体系
- 公众号横版封面默认约为 `2.35:1`

排版会基于仓库中的 `assets/wechat-template.html` 生成微信公众号粘贴版，正文使用内联样式，减少公众号编辑器清理样式后的变化。

## 默认交付物

```text
文章标题_完整稿.md
文章标题_微信公众号粘贴版.html
文章标题_assets/
├── 00-公众号封面.png
├── 01-正文配图.png
├── 02-正文配图.png
└── 03-正文配图.png
```

按用户要求还可以增加：

- `.docx` 审阅版
- `.zip` 完整发布包
- SVG 可编辑信息图源文件

打开生成的 HTML，点击“复制公众号正文”，再粘贴到微信公众号编辑器即可。

## 英文名称与颜色审计

仓库包含公众号 HTML 检查脚本：

```bash
python3 scripts/audit_wechat_html.py path/to/article.html
```

增加本文专有名词：

```bash
python3 scripts/audit_wechat_html.py path/to/article.html \
  --terms "Codex" "Claude Code" "GitHub Copilot" "Agent"
```

脚本会检查产品名和技术词的拼写、空格、大小写与颜色标注。修复所有 `[CASE]` 和 `[UNCOLORED]` 项后，重新运行直到输出 `PASS`。

## 与公众号配图 Skill 配合

如果只想处理封面和正文信息图，可以配合独立的 [`create-wechat-article-visuals`](https://github.com/HurmitLI/create-wechat-article-visuals) Skill：

```text
$write-tech-wechat-article 完成文章研究和正文，再用 $create-wechat-article-visuals 生成统一配图
```

## 仓库结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── icon.svg
│   └── wechat-template.html
├── references/
│   ├── editorial-workflow.md
│   ├── visual-system.md
│   └── delivery-checklist.md
└── scripts/
    └── audit_wechat_html.py
```

- `SKILL.md`：核心工作流、触发条件与交付要求
- `agents/openai.yaml`：Codex 界面展示信息
- `assets/wechat-template.html`：微信公众号粘贴版模板
- `references/editorial-workflow.md`：选题问题库与文章结构方法
- `references/visual-system.md`：封面、正文图与公众号版式规则
- `references/delivery-checklist.md`：发布前检查清单
- `scripts/audit_wechat_html.py`：英文名称、大小写和颜色审计脚本
