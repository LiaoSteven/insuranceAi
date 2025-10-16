"""
SellSysInsurance - 使用示例
演示如何使用新的文件管理和数据导出功能
"""

import sys
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.file_manager import FileManager
from core.document_parser import DocumentParser, DataExporter
from core.sales_generator import SalesGenerator
from config.settings import settings


def example_1_file_manager():
    """示例1: 使用文件管理器"""
    print("\n" + "=" * 70)
    print("示例1: 文件管理器 - 自动扫描和分类")
    print("=" * 70)

    manager = FileManager()

    # 打印文件摘要
    manager.print_file_summary()

    # 获取最新的产品文档
    latest_product = manager.get_latest_file('product')
    if latest_product:
        print(f"\n最新产品文档: {latest_product}")
    else:
        print("\n暂无产品文档,请将文件放入 data/product/ 目录")

    # 根据名称模式查找文件
    # competitor_file = manager.get_file_by_name_pattern('competitor', '平安')
    # if competitor_file:
    #     print(f"找到竞品文件: {competitor_file}")


def example_2_data_export():
    """示例2: 数据导出 - JSON和CSV"""
    print("\n" + "=" * 70)
    print("示例2: 数据导出 - 提取并保存为JSON/CSV")
    print("=" * 70)

    manager = FileManager()
    product_file = manager.get_latest_file('product')

    if not product_file:
        print("⚠️  暂无产品文档,请将文件放入 data/product/ 目录")
        print("示例: 将Excel文件复制到 data/product/ 目录")
        return

    # 解析文档
    parser = DocumentParser()
    data = parser.parse_document(str(product_file))

    # 导出为JSON和CSV
    exporter = DataExporter()
    results = exporter.export_extracted_data(
        data,
        str(settings.OUTPUT_EXTRACTED_DIR),
        formats=['json', 'csv']  # 导出为JSON和CSV
    )

    print("\n导出结果:")
    for format_type, file_path in results.items():
        print(f"  {format_type.upper()}: {file_path}")


def example_3_auto_generate():
    """示例3: 自动化生成 - 使用文件管理器自动查找文件"""
    print("\n" + "=" * 70)
    print("示例3: 自动化生成 - 无需手动指定文件路径")
    print("=" * 70)

    manager = FileManager()

    # 自动查找文件
    product_file = manager.get_latest_file('product')
    competitor_file = manager.get_latest_file('competitor')

    if not product_file:
        print("⚠️  暂无产品文档,请将文件放入 data/product/ 目录")
        return

    # 生成分析报告
    generator = SalesGenerator()

    print("\n正在生成产品分析报告...")
    output = generator.generate_product_analysis_report(
        product_file=str(product_file),
        competitor_file=str(competitor_file) if competitor_file else None
    )

    print(f"\n✅ 分析报告已生成!")
    print(f"📊 分析报告: {output}")
    print(f"📂 提取数据: {settings.OUTPUT_EXTRACTED_DIR}")


def example_4_directory_structure():
    """示例4: 查看目录结构"""
    print("\n" + "=" * 70)
    print("示例4: 目录结构")
    print("=" * 70)

    print("\n📁 输入目录 (data/):")
    print(f"  产品文档: {settings.DATA_PRODUCT_DIR}")
    print(f"  竞品文档: {settings.DATA_COMPETITOR_DIR}")
    print(f"  客户信息: {settings.DATA_CUSTOMER_DIR}")
    print(f"  产品目录: {settings.DATA_CATALOG_DIR}")

    print("\n📁 输出目录 (output/):")
    print(f"  提取数据: {settings.OUTPUT_EXTRACTED_DIR}")
    print(f"  分析报告: {settings.OUTPUT_ANALYSIS_DIR}")
    print(f"  销售话术: {settings.OUTPUT_SCRIPTS_DIR}")
    print(f"  演示大纲: {settings.OUTPUT_PRESENTATIONS_DIR}")
    print(f"  客户推荐: {settings.OUTPUT_RECOMMENDATIONS_DIR}")
    print(f"  销售邮件: {settings.OUTPUT_EMAILS_DIR}")


def example_5_scan_and_organize():
    """示例5: 扫描和整理文件"""
    print("\n" + "=" * 70)
    print("示例5: 扫描和整理文件")
    print("=" * 70)

    manager = FileManager()

    # 扫描所有文件
    print("\n扫描data目录...")
    classified = manager.scan_directory()

    print("\n扫描结果:")
    for file_type, files in classified.items():
        if files:
            print(f"\n{file_type} ({len(files)}个文件):")
            for f in files:
                print(f"  - {f.name}")

    # 测试自动整理 (不实际移动文件)
    print("\n\n测试自动整理 (dry run)...")
    summary = manager.auto_organize_files(dry_run=True)

    if summary['moved']:
        print("\n需要移动的文件:")
        for item in summary['moved']:
            print(f"  {item}")

    if summary['unclassified']:
        print("\n未分类的文件:")
        for item in summary['unclassified']:
            print(f"  {item}")


def main():
    """运行所有示例"""
    print("\n")
    print("=" * 70)
    print("  SellSysInsurance - 功能示例演示")
    print("=" * 70)

    examples = [
        ("文件管理器", example_1_file_manager),
        ("数据导出", example_2_data_export),
        ("自动化生成", example_3_auto_generate),
        ("目录结构", example_4_directory_structure),
        ("文件扫描整理", example_5_scan_and_organize),
    ]

    print("\n可用示例:")
    for idx, (name, _) in enumerate(examples, 1):
        print(f"  {idx}. {name}")
    print(f"  0. 运行所有示例")

    try:
        choice = input("\n请选择示例 (0-5): ").strip()

        if choice == '0':
            for name, func in examples:
                func()
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            _, func = examples[int(choice) - 1]
            func()
        else:
            print("无效选择")
            return

    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)
    print("示例演示完成!")
    print("=" * 70)
    print("\n更多使用方法,请查看: USAGE_EXAMPLES.md")


if __name__ == "__main__":
    main()
