"""
文件管理模块
自动扫描和分类管理data目录中的文档
支持自动识别文件类型并分类到对应目录
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 添加src到路径以支持导入
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings


class FileManager:
    """文件管理器 - 自动扫描和分类文档"""

    # 支持的文件扩展名
    SUPPORTED_EXTENSIONS = {'.xlsx', '.xls', '.docx', '.doc', '.pptx', '.ppt', '.pdf'}

    # 文件类型关键词映射
    TYPE_KEYWORDS = {
        'product': ['产品', 'product', '方案', 'plan', '险种'],
        'competitor': ['竞品', 'competitor', '竞争', 'competition', '对手'],
        'customer': ['客户', 'customer', '用户', 'user', '画像', 'profile'],
        'catalog': ['目录', 'catalog', '列表', 'list', '清单']
    }

    def __init__(self):
        """初始化文件管理器"""
        self.data_dir = settings.DATA_DIR
        self.product_dir = settings.DATA_PRODUCT_DIR
        self.competitor_dir = settings.DATA_COMPETITOR_DIR
        self.customer_dir = settings.DATA_CUSTOMER_DIR
        self.catalog_dir = settings.DATA_CATALOG_DIR

    def scan_directory(self, directory: Path = None) -> Dict[str, List[Path]]:
        """
        扫描目录,按类型分类文件

        Args:
            directory: 要扫描的目录,默认为data根目录

        Returns:
            文件类型到文件路径列表的映射
        """
        if directory is None:
            directory = self.data_dir

        results = {
            'product': [],
            'competitor': [],
            'customer': [],
            'catalog': [],
            'unclassified': []
        }

        # 扫描目录
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in self.SUPPORTED_EXTENSIONS:
                file_type = self._classify_file(file_path)
                results[file_type].append(file_path)

        return results

    def _classify_file(self, file_path: Path) -> str:
        """
        根据文件名和路径分类文件

        Args:
            file_path: 文件路径

        Returns:
            文件类型 (product/competitor/customer/catalog/unclassified)
        """
        # 检查文件是否在分类目录中
        try:
            relative_path = file_path.relative_to(self.data_dir)
            first_dir = relative_path.parts[0] if len(relative_path.parts) > 1 else None

            if first_dir in ['product', 'competitor', 'customer', 'catalog']:
                return first_dir
        except ValueError:
            pass

        # 根据文件名关键词分类
        filename_lower = file_path.stem.lower()

        for file_type, keywords in self.TYPE_KEYWORDS.items():
            if any(keyword in filename_lower for keyword in keywords):
                return file_type

        return 'unclassified'

    def get_latest_file(self, file_type: str) -> Optional[Path]:
        """
        获取指定类型的最新文件

        Args:
            file_type: 文件类型 (product/competitor/customer/catalog)

        Returns:
            最新文件路径,如果不存在返回None
        """
        type_dir_map = {
            'product': self.product_dir,
            'competitor': self.competitor_dir,
            'customer': self.customer_dir,
            'catalog': self.catalog_dir
        }

        target_dir = type_dir_map.get(file_type)
        if not target_dir:
            raise ValueError(f"不支持的文件类型: {file_type}")

        # 查找所有支持的文件
        files = []
        for ext in self.SUPPORTED_EXTENSIONS:
            files.extend(target_dir.glob(f'*{ext}'))

        if not files:
            return None

        # 按修改时间排序,返回最新的
        latest_file = max(files, key=lambda p: p.stat().st_mtime)
        return latest_file

    def list_files_by_type(self, file_type: str) -> List[Tuple[str, Path]]:
        """
        列出指定类型的所有文件

        Args:
            file_type: 文件类型 (product/competitor/customer/catalog)

        Returns:
            (文件名, 文件路径)的列表,按修改时间排序
        """
        type_dir_map = {
            'product': self.product_dir,
            'competitor': self.competitor_dir,
            'customer': self.customer_dir,
            'catalog': self.catalog_dir
        }

        target_dir = type_dir_map.get(file_type)
        if not target_dir:
            raise ValueError(f"不支持的文件类型: {file_type}")

        files = []
        for ext in self.SUPPORTED_EXTENSIONS:
            files.extend(target_dir.glob(f'*{ext}'))

        # 按修改时间降序排序
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        return [(f.name, f) for f in files]

    def auto_organize_files(self, dry_run: bool = True) -> Dict[str, List[str]]:
        """
        自动整理data目录下的文件到对应分类目录

        Args:
            dry_run: 是否为测试模式(不实际移动文件)

        Returns:
            移动操作的摘要
        """
        # 扫描所有文件
        classified = self.scan_directory()

        type_dir_map = {
            'product': self.product_dir,
            'competitor': self.competitor_dir,
            'customer': self.customer_dir,
            'catalog': self.catalog_dir
        }

        summary = {
            'moved': [],
            'already_organized': [],
            'unclassified': []
        }

        # 处理已分类的文件
        for file_type in ['product', 'competitor', 'customer', 'catalog']:
            target_dir = type_dir_map[file_type]

            for file_path in classified[file_type]:
                # 检查文件是否已在正确目录中
                if file_path.parent == target_dir:
                    summary['already_organized'].append(str(file_path))
                else:
                    # 需要移动
                    new_path = target_dir / file_path.name

                    # 处理文件名冲突
                    counter = 1
                    while new_path.exists():
                        stem = file_path.stem
                        suffix = file_path.suffix
                        new_path = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1

                    if not dry_run:
                        file_path.rename(new_path)

                    summary['moved'].append(f"{file_path} -> {new_path}")

        # 记录未分类文件
        summary['unclassified'] = [str(f) for f in classified['unclassified']]

        return summary

    def print_file_summary(self):
        """打印文件摘要"""
        print("\n" + "=" * 70)
        print("📁 文件管理器 - 文件摘要")
        print("=" * 70)

        categories = [
            ('产品文档', 'product'),
            ('竞品文档', 'competitor'),
            ('客户信息', 'customer'),
            ('产品目录', 'catalog')
        ]

        for name, file_type in categories:
            files = self.list_files_by_type(file_type)
            print(f"\n{name} ({len(files)}个文件):")
            print("-" * 70)

            if files:
                for idx, (filename, filepath) in enumerate(files, 1):
                    size_kb = filepath.stat().st_size / 1024
                    print(f"  {idx}. {filename} ({size_kb:.1f}KB)")
            else:
                print("  (无文件)")

        print("\n" + "=" * 70)

    def get_file_by_name_pattern(self, file_type: str, pattern: str) -> Optional[Path]:
        """
        根据名称模式查找文件

        Args:
            file_type: 文件类型
            pattern: 文件名模式(部分匹配)

        Returns:
            匹配的文件路径,如果找到多个返回最新的
        """
        files = self.list_files_by_type(file_type)
        pattern_lower = pattern.lower()

        matched = [f for name, f in files if pattern_lower in name.lower()]

        if not matched:
            return None

        # 返回最新的匹配文件
        return matched[0]


def quick_find_file(file_type: str, pattern: str = None) -> Optional[Path]:
    """
    快速查找文件

    Args:
        file_type: 文件类型 (product/competitor/customer/catalog)
        pattern: 文件名模式(可选),如果不提供则返回最新文件

    Returns:
        文件路径或None
    """
    manager = FileManager()

    if pattern:
        return manager.get_file_by_name_pattern(file_type, pattern)
    else:
        return manager.get_latest_file(file_type)
