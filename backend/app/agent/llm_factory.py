"""LLM动态工厂"""
import time
from typing import Optional
from app.config import settings
from app.agent.providers import PROVIDER_CONFIG
from app.utils.security import APIKeyManager


class LLMFactory:
    """动态LLM创建工厂
    
    根据用户配置创建不同的LLM实例
    支持DeepSeek、OpenAI、Claude、通义千问等
    """
    
    def __init__(self):
        self.key_manager = APIKeyManager()
        self.providers = PROVIDER_CONFIG
    
    def create_llm(self, user_id: int, db=None):
        """根据用户配置创建LLM实例"""
        # 如果没有传入db，使用默认配置
        if db is None:
            return self._create_default_llm()
        
        # 获取用户配置
        from app.models.model_config import UserModelConfig
        config = UserModelConfig.get_by_user(db, user_id)
        
        if not config or not config.api_key_encrypted:
            # 使用默认配置（DeepSeek）
            return self._create_default_llm()
        
        # 解密API Key
        api_key = self.key_manager.decrypt_key(config.api_key_encrypted)
        
        # 获取提供商配置
        provider_config = self.providers.get(config.provider)
        if not provider_config:
            raise ValueError(f"不支持的提供商: {config.provider}")
        
        # 创建LLM实例
        return self._create_llm_instance(
            provider=config.provider,
            model_name=config.model_name,
            api_key=api_key,
            base_url=config.base_url or provider_config.get("base_url"),
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
    
    def _create_llm_instance(self, provider: str, model_name: str,
                              api_key: str, base_url: str,
                              temperature: float, max_tokens: int,
                              timeout: int = 30):
        """创建LLM实例"""
        
        if provider == "claude":
            # Claude使用专门的类
            try:
                from langchain_anthropic import ChatAnthropic
                return ChatAnthropic(
                    model=model_name,
                    anthropic_api_key=api_key,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=timeout,
                )
            except ImportError:
                raise ImportError("请安装 langchain-anthropic: pip install langchain-anthropic")
        else:
            # DeepSeek、OpenAI、Qwen、自定义都使用OpenAI兼容格式
            try:
                from langchain_openai import ChatOpenAI
                kwargs = {
                    "model": model_name,
                    "api_key": api_key,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "request_timeout": timeout,
                }
                if base_url:
                    kwargs["base_url"] = base_url
                
                return ChatOpenAI(**kwargs)
            except ImportError:
                raise ImportError("请安装 langchain-openai: pip install langchain-openai")
    
    def _create_default_llm(self):
        """创建默认LLM（DeepSeek）"""
        api_key = settings.DEEPSEEK_API_KEY
        if not api_key:
            raise ValueError("未配置DEEPSEEK_API_KEY，请在.env文件中配置或在设置页面配置模型")
        
        return self._create_llm_instance(
            provider="deepseek",
            model_name=settings.DEFAULT_MODEL,
            api_key=api_key,
            base_url=settings.DEFAULT_BASE_URL,
            temperature=0.7,
            max_tokens=2000,
        )
    
    def test_connection(self, provider: str, model_name: str,
                        api_key: str, base_url: str = None) -> dict:
        """测试模型连接（仅验证API可达性和Key有效性）"""
        import httpx

        provider_config = self.providers.get(provider, {})
        url = (base_url or provider_config.get("base_url", "")).rstrip("/") + "/models"

        headers = {}
        if provider == "claude":
            headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
        else:
            headers = {"Authorization": f"Bearer {api_key}"}

        try:
            start_time = time.time()
            with httpx.Client(timeout=10) as client:
                resp = client.get(url, headers=headers)
            latency = (time.time() - start_time) * 1000

            if resp.status_code in (200, 201):
                return {"success": True, "message": "连接成功", "latency_ms": round(latency, 2)}
            elif resp.status_code == 401:
                return {"success": False, "message": "API Key 无效", "latency_ms": round(latency, 2)}
            else:
                return {"success": False, "message": f"API 返回 {resp.status_code}: {resp.text[:200]}", "latency_ms": round(latency, 2)}

        except httpx.ConnectTimeout:
            return {"success": False, "message": "连接超时，请检查网络或API地址", "latency_ms": None}
        except httpx.ConnectError as e:
            return {"success": False, "message": f"无法连接到服务器: {e}", "latency_ms": None}
        except Exception as e:
            return {"success": False, "message": f"连接失败: {str(e)}", "latency_ms": None}
