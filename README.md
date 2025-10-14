# SellSysInsurance - 保险销售智能助手

一个本地安全的保险销售辅助系统，支持从PPT/Excel/Word/PDF文档中提取信息，使用Claude AI进行智能分析，生成销售脚本、话术和推荐方案。

## 核心特性

- **本地文档解析** - 支持 Excel (.xlsx), Word (.docx), PowerPoint (.pptx), PDF 格式
- **数据安全** - 文档仅在本地解析，只将文本内容发送给AI，原文件不上传
- **Claude AI智能分析** - 产品比较、优势分析、客户定制推荐
- **多种输出** - 销售话术、演示大纲、客户推荐、销售邮件

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置API密钥

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，设置你的 Anthropic API Key
# ANTHROPIC_API_KEY=your_api_key_here
```

在 [Anthropic Console](https://console.anthropic.com/) 获取API密钥

### 3. 准备文档

将你的产品文档、客户信息等文件放入 `data/` 目录：

```
data/
├── product.xlsx          # 产品信息
├── competitor.xlsx       # 竞品信息
├── customer.xlsx         # 客户信息
└── catalog.xlsx          # 产品目录
```

### 4. 运行应用

```bash
# 查看帮助
python src/main.py --help

# 产品分析
python src/main.py analysis --product data/product.xlsx --competitor data/competitor.xlsx

# 生成销售话术
python src/main.py script --product data/product.xlsx --tone professional

# 生成演示大纲
python src/main.py presentation --product data/product.xlsx --customer data/customer.xlsx

# 客户推荐方案
python src/main.py recommendation --customer data/customer.xlsx --catalog data/catalog.xlsx

# 生成销售邮件
python src/main.py email --purpose introduction --product data/product.xlsx
```

## 项目结构

```
insuranceAi/
├── .env.example           # 环境变量模板
├── requirements.txt       # Python依赖
├── README.md             # 项目文档
├── CLAUDE.md             # Claude Code开发规则
├── src/                  # 源代码
│   ├── core/             # 核心模块
│   │   ├── document_parser.py    # 文档解析
│   │   ├── ai_analyzer.py        # AI分析
│   │   ├── sales_generator.py    # 销售脚本生成
│   │   └── encryption.py         # 加密工具（可选）
│   ├── config/           # 配置管理
│   │   └── settings.py   # 配置加载
│   └── main.py           # 主入口
├── data/                 # 数据目录
│   ├── encrypted/        # 加密文件（可选）
│   └── templates/        # 模板
├── output/               # 输出目录
│   └── sales_scripts/    # 生成的脚本
└── tests/                # 测试文件
```

## 功能详解

### 1. 产品分析 (analysis)

分析产品特点，对比竞品，识别优势和改进点。

```bash
python src/main.py analysis \
  --product data/product.xlsx \
  --competitor data/competitor.xlsx \
  --output my_analysis.txt
```

**输出内容：**
- 产品核心特点
- 竞品对比分析
- 竞争优势
- 改进建议

### 2. 销售话术 (script)

生成结构化的销售话术，包含开场白、异议处理、促成成交。

```bash
python src/main.py script \
  --product data/product.xlsx \
  --customer data/customer.xlsx \
  --tone professional  # 可选: professional, friendly, consultative
```

**语气风格：**
- `professional` - 专业正式
- `friendly` - 亲切友好
- `consultative` - 咨询式

### 3. 演示大纲 (presentation)

为客户演示生成定制化大纲和PPT建议。

```bash
python src/main.py presentation \
  --product data/product.xlsx \
  --customer data/customer.xlsx \
  --type standard  # 可选: standard, detailed, executive
```

**演示类型：**
- `standard` - 标准演示 (15-20分钟)
- `detailed` - 详细演示 (30-45分钟)
- `executive` - 高管演示 (10分钟以内)

### 4. 客户推荐 (recommendation)

基于客户需求推荐合适产品。

```bash
python src/main.py recommendation \
  --customer data/customer.xlsx \
  --catalog data/catalog.xlsx
```

**输出内容：**
- 客户需求分析
- 产品推荐（最多3个）
- 保额建议
- 缴费方案

### 5. 销售邮件 (email)

生成专业的销售邮件模板。

```bash
python src/main.py email \
  --purpose introduction \  # 可选: introduction, follow_up, proposal, thank_you
  --product data/product.xlsx \
  --recipient data/recipient.xlsx
```

## 安全说明

**本应用如何保护您的数据：**

1. **本地处理** - 所有文档在本地解析，不会上传原文件
2. **仅文本提取** - 只提取文本内容发送给Claude API进行分析
3. **可选加密** - 提供文件加密工具（encryption.py），可加密敏感文档
4. **无数据存储** - Claude API不会永久存储您的数据

**推荐做法：**
- 将API密钥保存在 `.env` 文件中（已在 .gitignore 中）
- 不要将敏感文档提交到Git仓库
- 使用加密功能保护本地敏感文件

## 依赖库

- **anthropic** - Claude API客户端
- **openpyxl** - Excel文件解析
- **python-docx** - Word文件解析
- **python-pptx** - PowerPoint文件解析
- **PyPDF2** - PDF文件解析
- **cryptography** - 文件加密（可选）

## 开发指南

如果您需要开发或定制功能，请先阅读 `CLAUDE.md` 文档。

### 开发规则

- **Read CLAUDE.md first** - 包含重要的开发规则
- **技术债务预防** - 创建新文件前先搜索现有实现
- **单一数据源** - 避免重复功能
- **频繁提交** - 每个功能完成后提交
- **GitHub备份** - 每次提交后推送到远程仓库

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行测试并查看覆盖率
python -m pytest tests/ --cov=src
```

## 故障排除

### 问题: ModuleNotFoundError

```bash
# 确保已安装所有依赖
pip install -r requirements.txt
```

### 问题: API Key错误

```bash
# 检查 .env 文件是否正确配置
cat .env

# 确保设置了 ANTHROPIC_API_KEY
```

### 问题: 文档解析失败

- 确保文档格式正确（.xlsx, .docx, .pptx, .pdf）
- 检查文件是否损坏
- 查看详细错误信息

## 许可证

本项目使用开源许可证。

## 致谢

**Project Template by Chang Ho Chien | HC AI 說人話channel | v1.0.0**
📺 Tutorial: https://youtu.be/8Q1bRZaHH24

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。
