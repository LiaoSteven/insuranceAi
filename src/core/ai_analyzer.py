"""
Claude AI分析模块
使用Claude API对提取的文档内容进行智能分析
支持产品比较、优势分析、客户定制等功能
"""

import os
from typing import Dict, List, Optional
import anthropic


class AIAnalyzer:
    """Claude AI分析器"""

    def __init__(self, api_key: str = None):
        """
        初始化AI分析器

        Args:
            api_key: Anthropic API密钥，如果不提供则从环境变量读取
        """
        if api_key is None:
            api_key = os.getenv('ANTHROPIC_API_KEY')

        if not api_key:
            raise ValueError("请提供ANTHROPIC_API_KEY环境变量或传入api_key参数")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = os.getenv('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022')

    def analyze_product_comparison(self, product_data: str, competitor_data: str = None) -> str:
        """
        产品比较分析

        Args:
            product_data: 本公司产品信息
            competitor_data: 竞品信息（可选）

        Returns:
            分析结果
        """
        prompt = f"""你是一位专业的保险产品分析师。请分析以下产品信息：

【本公司产品信息】
{product_data}
"""

        if competitor_data:
            prompt += f"""
【竞品信息】
{competitor_data}

请从以下角度进行对比分析：
1. 产品特点对比
2. 价格竞争力分析
3. 保障范围差异
4. 目标客户群体
5. 我们的竞争优势
6. 需要改进的地方
"""
        else:
            prompt += """
请从以下角度分析产品：
1. 产品核心特点
2. 适合的客户群体
3. 定价策略
4. 保障范围
5. 产品优势
6. 潜在风险点
"""

        print("🤖 正在进行产品分析...")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.content[0].text
        print("✅ 产品分析完成")
        return result

    def generate_sales_pitch(
        self,
        product_data: str,
        customer_profile: str = None,
        tone: str = "professional"
    ) -> str:
        """
        生成销售话术

        Args:
            product_data: 产品信息
            customer_profile: 客户画像（可选）
            tone: 语气风格 (professional/friendly/consultative)

        Returns:
            销售话术
        """
        tone_descriptions = {
            "professional": "专业、正式，使用行业术语",
            "friendly": "亲切、友好，用通俗易懂的语言",
            "consultative": "咨询式，着重解决客户问题"
        }

        tone_desc = tone_descriptions.get(tone, tone_descriptions["professional"])

        prompt = f"""你是一位经验丰富的保险销售顾问。请根据以下信息生成一份销售话术：

【产品信息】
{product_data}
"""

        if customer_profile:
            prompt += f"""
【客户画像】
{customer_profile}
"""

        prompt += f"""
【要求】
1. 语气风格：{tone_desc}
2. 包含开场白、产品介绍、优势说明、常见异议处理、促成成交
3. 结构清晰，易于实际使用
4. 突出产品对客户的价值
5. 提供3-5个常见问题的回答话术
"""

        print("🤖 正在生成销售话术...")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.content[0].text
        print("✅ 销售话术生成完成")
        return result

    def create_customer_presentation(
        self,
        product_data: str,
        customer_info: str,
        presentation_type: str = "standard"
    ) -> str:
        """
        生成客户定制演示内容

        Args:
            product_data: 产品信息
            customer_info: 客户信息
            presentation_type: 演示类型 (standard/detailed/executive)

        Returns:
            演示内容大纲
        """
        type_descriptions = {
            "standard": "标准演示，15-20分钟，适合初次接触",
            "detailed": "详细演示，30-45分钟，适合深度沟通",
            "executive": "高管演示，10分钟以内，突出ROI和战略价值"
        }

        type_desc = type_descriptions.get(presentation_type, type_descriptions["standard"])

        prompt = f"""你是一位专业的保险销售培训师。请为以下场景设计演示内容大纲：

【产品信息】
{product_data}

【客户信息】
{customer_info}

【演示类型】
{type_desc}

【输出要求】
1. 清晰的演示结构（开场、主体、结尾）
2. 每个环节的关键要点
3. 需要准备的材料
4. 预计时间分配
5. 互动环节设计
6. 可能的客户问题及应对
7. PPT大纲建议（标题+要点）
"""

        print("🤖 正在生成演示内容...")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.content[0].text
        print("✅ 演示内容生成完成")
        return result

    def analyze_customer_needs(self, customer_data: str, product_catalog: str) -> str:
        """
        分析客户需求并推荐产品

        Args:
            customer_data: 客户数据
            product_catalog: 产品目录

        Returns:
            需求分析和推荐结果
        """
        prompt = f"""你是一位专业的保险需求分析师。请根据以下信息进行需求分析：

【客户信息】
{customer_data}

【可选产品】
{product_catalog}

【分析要求】
1. 客户需求分析（风险点、保障需求、预算考虑）
2. 产品推荐（最多3个）
3. 推荐理由
4. 保额建议
5. 缴费方案建议
6. 风险提示
7. 后续跟进建议
"""

        print("🤖 正在分析客户需求...")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.content[0].text
        print("✅ 客户需求分析完成")
        return result

    def generate_email_template(
        self,
        purpose: str,
        product_data: str,
        recipient_info: str = None
    ) -> str:
        """
        生成邮件模板

        Args:
            purpose: 邮件目的 (introduction/follow_up/proposal/thank_you)
            product_data: 产品信息
            recipient_info: 收件人信息

        Returns:
            邮件内容
        """
        purpose_descriptions = {
            "introduction": "首次接触，介绍产品",
            "follow_up": "跟进客户，推进销售",
            "proposal": "正式方案，详细说明",
            "thank_you": "感谢购买，售后服务"
        }

        purpose_desc = purpose_descriptions.get(purpose, "通用邮件")

        prompt = f"""请生成一封专业的保险销售邮件：

【邮件目的】
{purpose_desc}

【产品信息】
{product_data}
"""

        if recipient_info:
            prompt += f"""
【收件人信息】
{recipient_info}
"""

        prompt += """
【要求】
1. 主题行（简洁有吸引力）
2. 称呼（专业得体）
3. 正文（结构清晰，重点突出）
4. 行动号召（CTA明确）
5. 落款（专业规范）
6. 邮件长度适中（不超过300字）
"""

        print("🤖 正在生成邮件模板...")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.content[0].text
        print("✅ 邮件模板生成完成")
        return result

    def custom_analysis(self, prompt: str, context_data: str = None) -> str:
        """
        自定义分析

        Args:
            prompt: 自定义提示词
            context_data: 上下文数据

        Returns:
            分析结果
        """
        full_prompt = prompt

        if context_data:
            full_prompt = f"""【上下文信息】
{context_data}

【分析要求】
{prompt}
"""

        print("🤖 正在执行自定义分析...")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )

        result = response.content[0].text
        print("✅ 自定义分析完成")
        return result
