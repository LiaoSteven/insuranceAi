"""
加密文件处理模块
提供文件加密和解密功能，确保敏感数据的本地安全存储
"""

import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64


class FileEncryption:
    """文件加密解密类"""

    def __init__(self, password: str = None):
        """
        初始化加密器

        Args:
            password: 加密密码，如果不提供则从环境变量读取
        """
        if password is None:
            password = os.getenv('ENCRYPTION_PASSWORD', 'default_password_change_me')

        self.password = password.encode()
        self.salt = b'insurance_sales_system_salt_2024'  # 实际使用时应该随机生成并保存

    def _generate_key(self) -> bytes:
        """
        基于密码生成加密密钥

        Returns:
            加密密钥
        """
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key

    def encrypt_file(self, input_path: str, output_path: str = None) -> str:
        """
        加密文件

        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径，如果不指定则在原文件名后加.encrypted

        Returns:
            加密后的文件路径
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        if output_path is None:
            output_path = input_path + '.encrypted'

        # 读取原始文件
        with open(input_path, 'rb') as f:
            data = f.read()

        # 加密
        key = self._generate_key()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)

        # 写入加密文件
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

        print(f"✅ 文件已加密: {output_path}")
        return output_path

    def decrypt_file(self, input_path: str, output_path: str = None) -> str:
        """
        解密文件

        Args:
            input_path: 加密文件路径
            output_path: 输出文件路径，如果不指定则在原文件名去掉.encrypted

        Returns:
            解密后的文件路径
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        if output_path is None:
            if input_path.endswith('.encrypted'):
                output_path = input_path[:-10]  # 去掉.encrypted
            else:
                output_path = input_path + '.decrypted'

        # 读取加密文件
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()

        # 解密
        key = self._generate_key()
        fernet = Fernet(key)
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
        except Exception as e:
            raise ValueError(f"解密失败，请检查密码是否正确: {str(e)}")

        # 写入解密文件
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        print(f"✅ 文件已解密: {output_path}")
        return output_path

    def decrypt_to_memory(self, input_path: str) -> bytes:
        """
        解密文件到内存（不写入磁盘）

        Args:
            input_path: 加密文件路径

        Returns:
            解密后的数据（字节）
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        # 读取加密文件
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()

        # 解密
        key = self._generate_key()
        fernet = Fernet(key)
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
        except Exception as e:
            raise ValueError(f"解密失败，请检查密码是否正确: {str(e)}")

        return decrypted_data


def encrypt_directory(directory_path: str, password: str = None, file_extensions: list = None):
    """
    批量加密目录中的文件

    Args:
        directory_path: 目录路径
        password: 加密密码
        file_extensions: 要加密的文件扩展名列表，如['.xlsx', '.docx', '.pptx']
    """
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"目录不存在: {directory_path}")

    if file_extensions is None:
        file_extensions = ['.xlsx', '.docx', '.pptx', '.pdf', '.txt']

    encryptor = FileEncryption(password)
    encrypted_count = 0

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            if file_ext in file_extensions and not file.endswith('.encrypted'):
                try:
                    encryptor.encrypt_file(file_path)
                    encrypted_count += 1
                except Exception as e:
                    print(f"❌ 加密失败 {file_path}: {str(e)}")

    print(f"\n✅ 批量加密完成，共加密 {encrypted_count} 个文件")
