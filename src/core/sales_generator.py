"""
销售脚本生成器
整合文档解析和AI分析，生成完整的销售材料
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 添加src到路径以支持导入
sys.path.insert(0, str(Path(__file__).parent.parent))

from .document_parser import DocumentParser, DataExporter, parse_multiple_documents
from .ai_analyzer import AIAnalyzer
from config.settings import settings


class SalesGenerator:
    """销售脚本生成器"""

    def __init__(self, api_key: str = None, save_extracted_data: bool = True):
        """
        初始化销售脚本生成器

        Args:
            api_key: Anthropic API密钥
            save_extracted_data: 是否保存提取的原始数据(JSON格式)
        """
        self.parser = DocumentParser()
        self.analyzer = AIAnalyzer(api_key)
        self.exporter = DataExporter()
        self.save_extracted_data = save_extracted_data

        # 使用新的分类目录结构
        self.output_extracted_dir = settings.OUTPUT_EXTRACTED_DIR
        self.output_analysis_dir = settings.OUTPUT_ANALYSIS_DIR
        self.output_scripts_dir = settings.OUTPUT_SCRIPTS_DIR
        self.output_presentations_dir = settings.OUTPUT_PRESENTATIONS_DIR
        self.output_recommendations_dir = settings.OUTPUT_RECOMMENDATIONS_DIR
        self.output_emails_dir = settings.OUTPUT_EMAILS_DIR

        # 兼容旧代码
        self.output_dir = str(self.output_scripts_dir)

    def _parse_and_save_document(self, file_path: str, doc_type: str = "document") -> tuple:
        """
        解析文档并保存提取的数据

        Args:
            file_path: 文档路径
            doc_type: 文档类型描述(用于日志)

        Returns:
            (提取的数据字典, 格式化的文本字符串)
        """
        print(f"\n📄 解析{doc_type}...")
        data = self.parser.parse_document(file_path)
        formatted_text = self.parser.format_extracted_data(data)

        # 保存提取的原始数据(JSON格式)
        if self.save_extracted_data:
            self.exporter.export_extracted_data(
                data,
                str(self.output_extracted_dir),
                formats=['json', 'csv']
            )

        return data, formatted_text

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

        # 解析产品文档并保存原始数据
        _, product_text = self._parse_and_save_document(product_file, "产品文档")

        # 解析竞品文档（如果提供）
        competitor_text = None
        if competitor_file:
            _, competitor_text = self._parse_and_save_document(competitor_file, "竞品文档")

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

        # 保存报告到分析报告目录
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"product_analysis_{timestamp}.txt"

        output_path = self.output_analysis_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ 报告已保存: {output_path}")
        return str(output_path)

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

        # 解析产品文档并保存原始数据
        _, product_text = self._parse_and_save_document(product_file, "产品文档")

        # 解析客户画像（如果提供）
        customer_text = None
        if customer_profile_file:
            _, customer_text = self._parse_and_save_document(customer_profile_file, "客户画像")

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

        # 保存脚本到销售话术目录
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"sales_script_{tone}_{timestamp}.txt"

        output_path = self.output_scripts_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ 脚本已保存: {output_path}")
        return str(output_path)

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

        # 解析文档并保存原始数据
        _, product_text = self._parse_and_save_document(product_file, "产品文档")
        _, customer_text = self._parse_and_save_document(customer_file, "客户信息")

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

        # 保存大纲到演示大纲目录
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"presentation_{presentation_type}_{timestamp}.txt"

        output_path = self.output_presentations_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ 大纲已保存: {output_path}")
        return str(output_path)

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

        # 解析文档并保存原始数据
        _, customer_text = self._parse_and_save_document(customer_file, "客户信息")
        _, catalog_text = self._parse_and_save_document(product_catalog_file, "产品目录")

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

        # 保存推荐方案到推荐目录
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"recommendation_{timestamp}.txt"

        output_path = self.output_recommendations_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ 推荐方案已保存: {output_path}")
        return str(output_path)

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

        # 解析产品文档并保存原始数据
        _, product_text = self._parse_and_save_document(product_file, "产品文档")

        # 解析收件人信息（如果提供）
        recipient_text = None
        if recipient_file:
            _, recipient_text = self._parse_and_save_document(recipient_file, "收件人信息")

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

        # 保存邮件到邮件目录
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"email_{purpose}_{timestamp}.txt"

        output_path = self.output_emails_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ 邮件已保存: {output_path}")
        return str(output_path)

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
