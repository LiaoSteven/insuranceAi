# SellSysInsurance - 使用示例

## 📚 目录

1. [快速开始](#快速开始)
2. [数据格式说明](#数据格式说明)
3. [目录结构说明](#目录结构说明)
4. [功能使用示例](#功能使用示例)
5. [常见问题](#常见问题)

---

## 🚀 快速开始

### 第一步: 准备文件

将你的文档放入 `data/` 目录下的对应分类文件夹:

```
data/
├── product/      # 产品文档 (产品说明、产品方案等)
├── competitor/   # 竞品文档 (竞品分析、竞争对手资料等)
├── customer/     # 客户信息 (客户画像、客户需求等)
└── catalog/      # 产品目录 (所有产品列表)
```

支持的文件格式: `.xlsx`, `.docx`, `.pptx`, `.pdf`

### 第二步: 运行命令

```bash
# 产品分析 (最简单的用法)
python src/main.py analysis --product data/product/my_product.xlsx

# 带竞品对比的产品分析
python src/main.py analysis --product data/product/my_product.xlsx --competitor data/competitor/competitor.xlsx

# 生成销售话术
python src/main.py script --product data/product/my_product.xlsx --tone professional
```

---

## 📊 数据格式说明

### Python字典 vs CSV vs JSON - 为什么使用JSON?

| 格式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Python字典** | 处理快速、灵活 | 不持久化、不可查看 | 内存中临时处理 |
| **CSV** | 通用、Excel可打开 | 只支持表格、不支持嵌套 | 简单表格数据 |
| **JSON** | 结构化、可读、持久化 | 体积稍大 | **所有类型文档** ✅ |

**系统设计:**
- **内存处理**: 使用Python字典 (快速灵活)
- **数据保存**: 使用JSON格式 (结构完整、可查看)
- **Excel导出**: 同时提供CSV格式 (方便Excel打开)

---

## 📁 目录结构说明

### 输入目录 (data/)

系统会自动创建并管理以下目录:

```
data/
├── product/      # 📦 产品文档
│   └── (放置产品说明、方案等文件)
├── competitor/   # 🎯 竞品文档
│   └── (放置竞品分析文件)
├── customer/     # 👤 客户信息
│   └── (放置客户画像、需求文件)
└── catalog/      # 📋 产品目录
    └── (放置产品列表文件)
```

**文件命名提示:**
- 包含关键词会自动分类: `产品`、`竞品`、`客户`、`目录`
- 示例: `产品说明_2024.xlsx` → 自动识别为产品文档

### 输出目录 (output/)

所有生成的文件都会自动分类保存:

```
output/
├── extracted_data/      # 📂 提取的原始数据 (JSON + CSV)
│   ├── product_data_20241016_143022.json
│   └── product_data_20241016_143022.csv
│
├── analysis_reports/    # 📊 AI分析报告
│   └── product_analysis_20241016_143045.txt
│
├── sales_scripts/       # 💬 销售话术
│   └── sales_script_professional_20241016_143120.txt
│
├── presentations/       # 📽️ 演示大纲
│   └── presentation_standard_20241016_143150.txt
│
├── recommendations/     # 🎯 客户推荐
│   └── recommendation_20241016_143210.txt
│
└── emails/              # 📧 销售邮件
    └── email_introduction_20241016_143240.txt
```

**分类说明:**
1. **extracted_data** - 文档提取的原始数据,保留完整结构
2. **analysis_reports** - AI生成的分析报告
3. **sales_scripts** - 销售话术脚本
4. **presentations** - 客户演示大纲
5. **recommendations** - 客户产品推荐方案
6. **emails** - 销售邮件模板

---

## 💡 功能使用示例

### 1. 产品分析报告

**场景:** 分析自家产品特点,或与竞品对比

```bash
# 基础分析
python src/main.py analysis --product data/product/重疾险A.xlsx

# 竞品对比分析
python src/main.py analysis \
  --product data/product/重疾险A.xlsx \
  --competitor data/competitor/XX公司重疾险.xlsx
```

**生成文件:**
- `output/extracted_data/重疾险A_20241016_143022.json` (提取的数据)
- `output/analysis_reports/product_analysis_20241016_143045.txt` (分析报告)

### 2. 销售话术生成

**场景:** 为销售团队准备话术脚本

```bash
# 专业风格
python src/main.py script --product data/product/重疾险A.xlsx --tone professional

# 友好风格
python src/main.py script --product data/product/重疾险A.xlsx --tone friendly

# 咨询风格
python src/main.py script --product data/product/重疾险A.xlsx --tone consultative

# 针对特定客户群体
python src/main.py script \
  --product data/product/重疾险A.xlsx \
  --customer data/customer/高净值客户画像.xlsx \
  --tone consultative
```

**生成文件:**
- `output/extracted_data/` (提取的数据)
- `output/sales_scripts/sales_script_professional_20241016_143120.txt` (话术脚本)

### 3. 客户演示大纲

**场景:** 准备客户演示PPT

```bash
# 标准演示 (15-20分钟)
python src/main.py presentation \
  --product data/product/重疾险A.xlsx \
  --customer data/customer/张总.docx \
  --type standard

# 详细演示 (30-45分钟)
python src/main.py presentation \
  --product data/product/重疾险A.xlsx \
  --customer data/customer/张总.docx \
  --type detailed

# 高管演示 (10分钟以内)
python src/main.py presentation \
  --product data/product/重疾险A.xlsx \
  --customer data/customer/张总.docx \
  --type executive
```

**生成文件:**
- `output/extracted_data/` (提取的数据)
- `output/presentations/presentation_standard_20241016_143150.txt` (演示大纲)

### 4. 客户推荐方案

**场景:** 根据客户需求推荐合适的产品

```bash
python src/main.py recommendation \
  --customer data/customer/李女士_35岁_三口之家.xlsx \
  --catalog data/catalog/2024产品目录.xlsx
```

**生成文件:**
- `output/extracted_data/` (提取的数据)
- `output/recommendations/recommendation_20241016_143210.txt` (推荐方案)

### 5. 销售邮件生成

**场景:** 快速生成专业的销售邮件

```bash
# 首次接触邮件
python src/main.py email \
  --purpose introduction \
  --product data/product/重疾险A.xlsx

# 跟进邮件
python src/main.py email \
  --purpose follow_up \
  --product data/product/重疾险A.xlsx \
  --recipient data/customer/王先生.docx

# 方案邮件
python src/main.py email \
  --purpose proposal \
  --product data/product/重疾险A.xlsx \
  --recipient data/customer/王先生.docx

# 感谢邮件
python src/main.py email \
  --purpose thank_you \
  --product data/product/重疾险A.xlsx
```

**生成文件:**
- `output/extracted_data/` (提取的数据)
- `output/emails/email_introduction_20241016_143240.txt` (邮件内容)

---

## 🔧 高级功能

### 使用Python API直接调用

```python
from src.core.sales_generator import SalesGenerator
from src.core.file_manager import FileManager

# 1. 使用文件管理器查找文件
manager = FileManager()
manager.print_file_summary()  # 打印所有文件摘要

# 获取最新的产品文档
product_file = manager.get_latest_file('product')

# 根据名称查找文件
competitor_file = manager.get_file_by_name_pattern('competitor', '平安')

# 2. 生成销售材料
generator = SalesGenerator()

# 生成产品分析
output = generator.generate_product_analysis_report(
    product_file=str(product_file),
    competitor_file=str(competitor_file) if competitor_file else None
)

print(f"报告已生成: {output}")
```

### 查看提取的JSON数据

提取的JSON文件包含完整的文档结构,可以直接查看:

```python
import json

# 读取提取的数据
with open('output/extracted_data/重疾险A_20241016_143022.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 查看元数据
print(data['metadata'])

# 查看提取的内容
print(data['data'])
```

### Excel数据导出为CSV

如果是Excel文件,系统会同时生成CSV格式:

```
output/extracted_data/
├── 产品列表_20241016_143022.json  # JSON格式 (完整数据)
├── 产品列表_Sheet1.csv            # Sheet1的CSV
└── 产品列表_Sheet2.csv            # Sheet2的CSV
```

---

## ❓ 常见问题

### Q1: 为什么不用手动指定文件路径?

**A:** 系统已经实现了智能文件管理:
- 自动扫描 `data/` 目录
- 根据文件名和位置自动分类
- 支持通过模式匹配查找文件

### Q2: 提取的数据保存在哪里?

**A:** 所有提取的原始数据都保存在 `output/extracted_data/` 目录:
- JSON格式 (所有文件类型)
- CSV格式 (仅Excel文件)

### Q3: 如何查看提取的数据?

**A:**
- **JSON**: 使用任何文本编辑器或JSON查看器
- **CSV**: 使用Excel、Google Sheets等工具直接打开

### Q4: 文件会上传到网络吗?

**A:** **不会!**
- 文档仅在本地解析提取文本
- 只有提取的**文本内容**会发送给Claude API进行分析
- 原始文件永远不会上传

### Q5: 可以自定义输出目录吗?

**A:** 可以通过修改 `src/config/settings.py` 中的目录配置实现。

---

## 📈 最佳实践

### 1. 文件命名规范

建议使用清晰的命名:
```
✅ 产品_重疾险A_2024.xlsx
✅ 竞品_平安福_分析.xlsx
✅ 客户_李女士_35岁.docx

❌ 文件1.xlsx
❌ 新建Microsoft Excel工作表.xlsx
```

### 2. 目录组织

按照功能分类存放:
```
data/product/      → 所有产品相关文档
data/competitor/   → 所有竞品相关文档
data/customer/     → 所有客户相关文档
data/catalog/      → 产品目录
```

### 3. 定期清理

系统会自动生成带时间戳的文件,建议定期清理旧文件:
```bash
# 定期备份重要分析报告
# 删除过期的临时文件
```

---

## 🎓 教程视频

更多详细教程,请访问:
📺 https://youtu.be/8Q1bRZaHH24

---

**Created by Chang Ho Chien | HC AI 说人话channel**
