"""
SellSysInsurance - Main Entry Point
Insurance sales system management application

本应用支持从本地文档（PPT/Excel/Word/PDF）提取信息，
使用Claude AI进行智能分析，生成销售脚本和材料。
文档内容仅在本地解析，不会上传到网络。
"""

import sys
import argparse
from pathlib import Path

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.sales_generator import SalesGenerator
from config.settings import settings


def print_banner():
    """打印欢迎横幅"""
    print("=" * 70)
    print("  SellSysInsurance - 保险销售智能助手")
    print("=" * 70)
    print("  支持本地文档解析 | Claude AI智能分析 | 销售脚本生成")
    print("  数据安全：文档仅本地处理，不上传网络")
    print("=" * 70)
    print()


def check_config():
    """检查配置"""
    is_valid, error_msg = settings.validate()
    if not is_valid:
        print(f"❌ 配置错误: {error_msg}")
        print("\n请按以下步骤配置：")
        print("1. 复制 .env.example 为 .env")
        print("2. 在 .env 文件中设置 ANTHROPIC_API_KEY")
        print("3. 重新运行程序")
        sys.exit(1)


def cmd_analysis(args):
    """产品分析命令"""
    print("\n📊 产品分析模式")
    print("-" * 70)

    generator = SalesGenerator()
    output = generator.generate_product_analysis_report(
        product_file=args.product,
        competitor_file=args.competitor,
        output_filename=args.output
    )

    print(f"\n✅ 分析完成！")
    print(f"📁 输出文件: {output}")


def cmd_script(args):
    """销售话术命令"""
    print("\n💬 销售话术生成模式")
    print("-" * 70)

    generator = SalesGenerator()
    output = generator.generate_sales_script(
        product_file=args.product,
        customer_profile_file=args.customer,
        tone=args.tone,
        output_filename=args.output
    )

    print(f"\n✅ 话术生成完成！")
    print(f"📁 输出文件: {output}")


def cmd_presentation(args):
    """演示大纲命令"""
    print("\n📽️  演示大纲生成模式")
    print("-" * 70)

    generator = SalesGenerator()
    output = generator.generate_presentation_outline(
        product_file=args.product,
        customer_file=args.customer,
        presentation_type=args.type,
        output_filename=args.output
    )

    print(f"\n✅ 大纲生成完成！")
    print(f"📁 输出文件: {output}")


def cmd_recommendation(args):
    """客户推荐命令"""
    print("\n🎯 客户推荐方案生成模式")
    print("-" * 70)

    generator = SalesGenerator()
    output = generator.generate_customer_recommendation(
        customer_file=args.customer,
        product_catalog_file=args.catalog,
        output_filename=args.output
    )

    print(f"\n✅ 推荐方案生成完成！")
    print(f"📁 输出文件: {output}")


def cmd_email(args):
    """邮件生成命令"""
    print("\n📧 销售邮件生成模式")
    print("-" * 70)

    generator = SalesGenerator()
    output = generator.generate_email(
        purpose=args.purpose,
        product_file=args.product,
        recipient_file=args.recipient,
        output_filename=args.output
    )

    print(f"\n✅ 邮件生成完成！")
    print(f"📁 输出文件: {output}")


def main():
    """主函数"""
    print_banner()

    parser = argparse.ArgumentParser(
        description='SellSysInsurance - 保险销售智能助手',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 产品分析
  python src/main.py analysis --product data/product.xlsx --competitor data/competitor.xlsx

  # 生成销售话术
  python src/main.py script --product data/product.xlsx --tone professional

  # 生成演示大纲
  python src/main.py presentation --product data/product.xlsx --customer data/customer.xlsx

  # 客户推荐
  python src/main.py recommendation --customer data/customer.xlsx --catalog data/catalog.xlsx

  # 生成邮件
  python src/main.py email --purpose introduction --product data/product.xlsx

支持的文件格式: .xlsx, .docx, .pptx, .pdf
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 产品分析命令
    parser_analysis = subparsers.add_parser('analysis', help='产品分析报告')
    parser_analysis.add_argument('--product', required=True, help='产品文档路径')
    parser_analysis.add_argument('--competitor', help='竞品文档路径（可选）')
    parser_analysis.add_argument('--output', help='输出文件名（可选）')
    parser_analysis.set_defaults(func=cmd_analysis)

    # 销售话术命令
    parser_script = subparsers.add_parser('script', help='生成销售话术')
    parser_script.add_argument('--product', required=True, help='产品文档路径')
    parser_script.add_argument('--customer', help='客户画像文档路径（可选）')
    parser_script.add_argument('--tone', default='professional',
                               choices=['professional', 'friendly', 'consultative'],
                               help='语气风格（默认: professional）')
    parser_script.add_argument('--output', help='输出文件名（可选）')
    parser_script.set_defaults(func=cmd_script)

    # 演示大纲命令
    parser_pres = subparsers.add_parser('presentation', help='生成演示大纲')
    parser_pres.add_argument('--product', required=True, help='产品文档路径')
    parser_pres.add_argument('--customer', required=True, help='客户信息文档路径')
    parser_pres.add_argument('--type', default='standard',
                             choices=['standard', 'detailed', 'executive'],
                             help='演示类型（默认: standard）')
    parser_pres.add_argument('--output', help='输出文件名（可选）')
    parser_pres.set_defaults(func=cmd_presentation)

    # 客户推荐命令
    parser_rec = subparsers.add_parser('recommendation', help='生成客户推荐方案')
    parser_rec.add_argument('--customer', required=True, help='客户信息文档路径')
    parser_rec.add_argument('--catalog', required=True, help='产品目录文档路径')
    parser_rec.add_argument('--output', help='输出文件名（可选）')
    parser_rec.set_defaults(func=cmd_recommendation)

    # 邮件生成命令
    parser_email = subparsers.add_parser('email', help='生成销售邮件')
    parser_email.add_argument('--purpose', required=True,
                              choices=['introduction', 'follow_up', 'proposal', 'thank_you'],
                              help='邮件目的')
    parser_email.add_argument('--product', required=True, help='产品文档路径')
    parser_email.add_argument('--recipient', help='收件人信息文档路径（可选）')
    parser_email.add_argument('--output', help='输出文件名（可选）')
    parser_email.set_defaults(func=cmd_email)

    args = parser.parse_args()

    # 如果没有提供命令，显示帮助
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 检查配置
    check_config()

    # 执行对应的命令
    try:
        args.func(args)
    except Exception as e:
        print(f"\n❌ 执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
