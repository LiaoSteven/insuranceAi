"""
配置管理模块
加载和管理应用配置
"""

import os
from pathlib import Path
from typing import Optional


class Settings:
    """应用配置类"""

    def __init__(self):
        """初始化配置"""
        # 项目根目录
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent

        # API配置
        self.ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
        self.CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022')

        # 加密配置（如果需要文件加密功能）
        self.ENCRYPTION_PASSWORD = os.getenv('ENCRYPTION_PASSWORD')

        # 数据目录配置 - 输入文件分类
        self.DATA_DIR = self.BASE_DIR / 'data'
        self.DATA_PRODUCT_DIR = self.DATA_DIR / 'product'        # 产品文档
        self.DATA_COMPETITOR_DIR = self.DATA_DIR / 'competitor'  # 竞品文档
        self.DATA_CUSTOMER_DIR = self.DATA_DIR / 'customer'      # 客户信息
        self.DATA_CATALOG_DIR = self.DATA_DIR / 'catalog'        # 产品目录
        self.ENCRYPTED_DIR = self.DATA_DIR / 'encrypted'
        self.TEMPLATES_DIR = self.DATA_DIR / 'templates'

        # 输出目录配置 - 按类型分类存档
        self.OUTPUT_DIR = self.BASE_DIR / 'output'
        self.OUTPUT_EXTRACTED_DIR = self.OUTPUT_DIR / 'extracted_data'     # 提取的原始数据(JSON)
        self.OUTPUT_ANALYSIS_DIR = self.OUTPUT_DIR / 'analysis_reports'    # AI分析报告
        self.OUTPUT_SCRIPTS_DIR = self.OUTPUT_DIR / 'sales_scripts'        # 销售话术
        self.OUTPUT_PRESENTATIONS_DIR = self.OUTPUT_DIR / 'presentations'  # 演示大纲
        self.OUTPUT_RECOMMENDATIONS_DIR = self.OUTPUT_DIR / 'recommendations'  # 客户推荐
        self.OUTPUT_EMAILS_DIR = self.OUTPUT_DIR / 'emails'                # 销售邮件

        # 兼容旧代码
        self.SALES_SCRIPTS_DIR = self.OUTPUT_SCRIPTS_DIR

        # 确保目录存在
        self._ensure_directories()

    def _ensure_directories(self):
        """确保必要的目录存在"""
        directories = [
            # 输入数据目录
            self.DATA_DIR,
            self.DATA_PRODUCT_DIR,
            self.DATA_COMPETITOR_DIR,
            self.DATA_CUSTOMER_DIR,
            self.DATA_CATALOG_DIR,
            self.ENCRYPTED_DIR,
            self.TEMPLATES_DIR,
            # 输出数据目录
            self.OUTPUT_DIR,
            self.OUTPUT_EXTRACTED_DIR,
            self.OUTPUT_ANALYSIS_DIR,
            self.OUTPUT_SCRIPTS_DIR,
            self.OUTPUT_PRESENTATIONS_DIR,
            self.OUTPUT_RECOMMENDATIONS_DIR,
            self.OUTPUT_EMAILS_DIR
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def validate(self) -> tuple[bool, Optional[str]]:
        """
        验证配置

        Returns:
            (是否有效, 错误消息)
        """
        if not self.ANTHROPIC_API_KEY:
            return False, "未设置ANTHROPIC_API_KEY环境变量"

        return True, None

    def get_absolute_path(self, relative_path: str) -> Path:
        """
        获取绝对路径

        Args:
            relative_path: 相对路径

        Returns:
            绝对路径
        """
        return self.BASE_DIR / relative_path

    def __repr__(self):
        """字符串表示"""
        return f"""Settings(
    BASE_DIR={self.BASE_DIR},
    CLAUDE_MODEL={self.CLAUDE_MODEL},
    API_KEY={'已设置' if self.ANTHROPIC_API_KEY else '未设置'}
)"""


def load_env_file(env_file: str = '.env'):
    """
    从.env文件加载环境变量

    Args:
        env_file: .env文件路径
    """
    env_path = Path(env_file)

    if not env_path.exists():
        print(f"⚠️  未找到{env_file}文件")
        return

    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # 跳过注释和空行
            if not line or line.startswith('#'):
                continue

            # 解析键值对
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")

                # 设置环境变量
                os.environ[key] = value

    print(f"✅ 已加载{env_file}配置")


# 启动时自动加载.env文件
try:
    # 使用项目根目录的.env文件
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
    load_env_file(str(env_path))
except Exception as e:
    print(f"⚠️  加载.env文件失败: {e}")


# 全局配置实例（在加载.env文件之后创建）
settings = Settings()
