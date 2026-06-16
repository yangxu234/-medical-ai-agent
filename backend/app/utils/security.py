from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import hashlib
from app.config import settings

# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """哈希密码"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT Token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """解码JWT Token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("无效的Token")


class APIKeyManager:
    """API Key安全管理器"""
    
    def __init__(self):
        # 使用配置的加密密钥
        key = settings.ENCRYPTION_KEY.encode()
        # 确保密钥长度为32字节
        key = hashlib.sha256(key).digest()
        # Fernet需要base64编码的32字节密钥
        import base64
        key = base64.urlsafe_b64encode(key)
        self.cipher = Fernet(key)
    
    def encrypt_key(self, api_key: str) -> str:
        """加密API Key"""
        return self.cipher.encrypt(api_key.encode()).decode()
    
    def decrypt_key(self, encrypted_key: str) -> str:
        """解密API Key"""
        return self.cipher.decrypt(encrypted_key.encode()).decode()
    
    def mask_key(self, api_key: str) -> str:
        """遮蔽API Key用于前端显示"""
        if not api_key or len(api_key) <= 8:
            return "****"
        return api_key[:4] + "****" + api_key[-4:]
