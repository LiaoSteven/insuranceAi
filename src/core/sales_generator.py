"""
销售脚本生成器
整合文档解析和AI分析，生成完整的销售材料
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from .document_parser import DocumentParser, parse_multiple_documents
from .ai_analyzer import AIAnalyzer


class SalesGenerator:
    """销售脚本生成器"""

    def __init__(self, api_key: str = None):
        """
        初始化销售脚本生成器

        Args:
            api_key: Anthropic API密钥
        """
        self.parser = DocumentParser()
        self.analyzer = AIAnalyzer(api_key)
        self.output_dir = "output/sales_scripts"

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_product_analysis_report(
        self,
        product_file: str,
        competitor_file: str = None,
        output_filename: str = None
    ) -> str:
        """
        生成产品分析报告

        Args:
            product_file: 产品文档路径
            competitor_file: 竞品文档路径（可选）
            output_filename: 输出文件名

        Returns:
            输出文件路径
        """
        print("=" * 60)
        print("📊 开始生成产品分析报告")
        print("=" * 60)

        # 解析产品文档
        print("\n📄 解析产品文档...")
        product_data = self.parser.parse_document(product_file)
        product_text = self.parser.format_extracted_data(product_data)

        # 解析竞品文档（如果提供）
        competitor_text = None
        if competitor_file:
            print("\n📄 解析竞品文档...")
            competitor_data = self.parser.parse_document(competitor_file)
            competitor_text = self.parser.format_extracted_data(competitor_data)

        # AI分析
        print("\n🤖 开始AI分析...")
        analysis = self.analyzer.analyze_product_comparison(
            product_text,
            competitor_text
        )

        # 生成报告
        report = self._format_report(
            title="产品分析报告",
            sections=[
                ("产品文档内容", product_text),
                ("竞品文档内容", competitor_text if competitor_text else "未提供"),
                ("AI分析结果", analysis)
            ]
        )

        # 保存报告
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"product_analysis_{timestamp}.txt"

        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ 报告已保存: {output_path}")
        return output_path

    def generate_sales_script(
        self,
        product_file: str,
        customer_profile_file: str = None,
        tone: str = "professional",
        output_filename: str = None
    ) -> str:
        """
        生成销售话术脚本

        Args:
            product_file: 产品文档路径
            customer_profile_file: 客户画像文档路径（可选）
            tone: 语气风格
            output_filename: 输出文件名

        Returns:
            输出文件路径
        """
        print("=" * 60)
        print("💬 开始生成销售话术脚本")
        print("=" * 60)

        # 解析产品文档
        print("\n📄 解析产品文档...")
        product_data = self.parser.parse_document(product_file)
        product_text = self.parser.format_extracted_data(product_data)

        # 解析客户画像（如果提供）
        customer_text = None
        if customer_profile_file:
            print("\n📄 解析客户画像...")
            customer_data = self.parser.parse_document(customer_profile_file)
            customer_text = self.parser.format_extracted_data(customer_data)

        # 生成销售话术
        print(f"\n🤖 生成销售话术（风格: {tone}）...")
        script = self.analyzer.generate_sales_pitch(
            product_text,
            customer_text,
            tone
        )

        # 生成报告
        sections = [
            ("产品信息", product_text),
        ]
        if customer_text:
            sections.append(("客户画像", customer_text))
        sections.append(("销售话术", script))

        report = self._format_report(
            title=f"销售话术脚本 - {tone.upper()}风格",
            sections=sections
        )

        # 保存脚本
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"sales_script_{tone}_{timestamp}.txt"

        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ 脚本已保存: {output_path}")
        return output_path

    def generate_presentation_outline(
        self,
        product_file: str,
        customer_file: str,
        presentation_type: str = "standard",
        output_filename: str = None
    ) -> str:
        """
        生成客户演示大纲

        Args:
            product_file: 产品文档路径
            customer_file: 客户信息文档路径
            presentation_type: 演示类型
            output_filename: 输出文件名

        Returns:
            输出文件路径
        """
        print("=" * 60)
        print("📽️  开始生成演示大纲")
        print("=" * 60)

        # 解析文档
        print("\n📄 解析产品文档...")
        product_data = self.parser.parse_document(product_file)
        product_text = self.parser.format_extracted_data(product_data)

        print("\n📄 解析客户信息...")
        customer_data = self.parser.parse_document(customer_file)
        customer_text = self.parser.format_extracted_data(customer_data)

        # 生成演示内容
        print(f"\n🤖 生成演示大纲（类型: {presentation_type}）...")
        outline = self.analyzer.create_customer_presentation(
            product_text,
            customer_text,
            presentation_type
        )

        # 生成报告
        report = self._format_report(
            title=f"客户演示大纲 - {presentation_type.upper()}",
            sections=[
                ("产品信息", product_text),
                ("客户信息", customer_text),
                ("演示大纲", outline)
            ]
        )

        # 保存大纲
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"presentation_{presentation_type}_{timestamp}.txt"

        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ 大纲已保存: {output_path}")
        return output_path

    def generate_customer_recommendation(
        self,
        customer_file: str,
        product_catalog_file: str,
        output_filename: str = None
    ) -> str:
        """
        生成客户推荐方案

        Args:
            customer_file: 客户信息文档路径
            product_catalog_file: 产品目录文档路径
            output_filename: 输出文件名

        Returns:
            输出文件路径
        """
        print("=" * 60)
        print("🎯 开始生成客户推荐方案")
        print("=" * 60)

        # 解析文档
        print("\n📄 解析客户信息...")
        customer_data = self.parser.parse_document(customer_file)
        customer_text = self.parser.format_extracted_data(customer_data)

        print("\n📄 解析产品目录...")
        catalog_data = self.parser.parse_document(product_catalog_file)
        catalog_text = self.parser.format_extracted_data(catalog_data)

        # 分析并推荐
        print("\n🤖 分析客户需求并推荐产品...")
        recommendation = self.analyzer.analyze_customer_needs(
            customer_text,
            catalog_text
        )

        # 生成报告
        report = self._format_report(
            title="客户需求分析与产品推荐",
            sections=[
                ("客户信息", customer_text),
                ("产品目录", catalog_text),
                ("推荐方案", recommendation)
            ]
        )

        # 保存推荐方案
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"recommendation_{timestamp}.txt"

        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ 推荐方案已保存: {output_path}")
        return output_path

    def generate_email(
        self,
        purpose: str,
        product_file: str,
        recipient_file: str = None,
        output_filename: str = None
    ) -> str:
        """
        生成销售邮件

        Args:
            purpose: 邮件目的
            product_file: 产品文档路径
            recipient_file: 收件人信息文档路径（可选）
            output_filename: 输出文件名

        Returns:
            输出文件路径
        """
        print("=" * 60)
        print("📧 开始生成销售邮件")
        print("=" * 60)

        # 解析产品文档
        print("\n📄 解析产品文档...")
        product_data = self.parser.parse_document(product_file)
        product_text = self.parser.format_extracted_data(product_data)

        # 解析收件人信息（如果提供）
        recipient_text = None
        if recipient_file:
            print("\n📄 解析收件人信息...")
            recipient_data = self.parser.parse_document(recipient_file)
            recipient_text = self.parser.format_extracted_data(recipient_data)

        # 生成邮件
        print(f"\n🤖 生成邮件（目的: {purpose}）...")
        email = self.analyzer.generate_email_template(
            purpose,
            product_text,
            recipient_text
        )

        # 生成报告
        sections = [("产品信息", product_text)]
        if recipient_text:
            sections.append(("收件人信息", recipient_text))
        sections.append(("邮件内容", email))

        report = self._format_report(
            title=f"销售邮件 - {purpose.upper()}",
            sections=sections
        )

        # 保存邮件
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"email_{purpose}_{timestamp}.txt"

        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ 邮件已保存: {output_path}")
        return output_path

    def _format_report(self, title: str, sections: List[tuple]) -> str:
        """
        格式化报告

        Args:
            title: 报告标题
            sections: 报告章节列表 [(标题, 内容), ...]

        Returns:
            格式化的报告文本
        """
        lines = [
            "=" * 80,
            f"  {title}",
            "=" * 80,
            f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"生成工具: SellSysInsurance",
            "\n" + "=" * 80 + "\n"
        ]

        for section_title, section_content in sections:
            if section_content and section_content != "未提供":
                lines.extend([
                    f"\n{'#' * 3} {section_title}",
                    "-" * 80,
                    section_content,
                    "\n" + "-" * 80 + "\n"
                ])

        lines.append("\n" + "=" * 80)
        lines.append("报告结束")
        lines.append("=" * 80)

        return "\n".join(lines)


def quick_generate(
    mode: str,
    product_file: str,
    secondary_file: str = None,
    **kwargs
) -> str:
    """
    快速生成功能

    Args:
        mode: 生成模式 (analysis/script/presentation/recommendation/email)
        product_file: 主要文档路径
        secondary_file: 次要文档路径
        **kwargs: 其他参数

    Returns:
        输出文件路径
    """
    generator = SalesGenerator()

    modes = {
        'analysis': generator.generate_product_analysis_report,
        'script': generator.generate_sales_script,
        'presentation': generator.generate_presentation_outline,
        'recommendation': generator.generate_customer_recommendation,
        'email': generator.generate_email,
    }

    if mode not in modes:
        raise ValueError(f"不支持的模式: {mode}. 支持的模式: {list(modes.keys())}")

    func = modes[mode]

    # 根据不同模式调用不同的函数
    if mode == 'analysis':
        return func(product_file, secondary_file, **kwargs)
    elif mode == 'script':
        return func(product_file, secondary_file, **kwargs)
    elif mode == 'presentation':
        return func(product_file, secondary_file, **kwargs)
    elif mode == 'recommendation':
        return func(secondary_file, product_file, **kwargs)
    elif mode == 'email':
        return func(kwargs.get('purpose', 'introduction'), product_file, secondary_file, **kwargs)
