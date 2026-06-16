"""提供商配置"""

PROVIDER_CONFIG = {
    "deepseek": {
        "name": "DeepSeek",
        "description": "深度求索，性价比高",
        "base_url": "https://api.deepseek.com/v1",
        "models": [
            {"id": "deepseek-chat", "name": "DeepSeek-V3", "description": "通用对话，最新版本"},
            {"id": "deepseek-reasoner", "name": "DeepSeek-R1", "description": "深度推理模型"},
        ],
        "requires_base_url": False,
    },
    "openai": {
        "name": "OpenAI",
        "description": "GPT系列模型",
        "base_url": "https://api.openai.com/v1",
        "models": [
            {"id": "gpt-4", "name": "GPT-4", "description": "最强模型"},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "description": "更快更便宜"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "经济实惠"},
        ],
        "requires_base_url": False,
    },
    "claude": {
        "name": "Claude (Anthropic)",
        "description": "Anthropic出品，擅长长文本",
        "base_url": "https://api.anthropic.com",
        "models": [
            {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "description": "最强"},
            {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "description": "均衡"},
            {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "description": "最快"},
        ],
        "requires_base_url": False,
    },
    "qwen": {
        "name": "通义千问",
        "description": "阿里云出品，国内首选",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "models": [
            {"id": "qwen-turbo", "name": "通义千问-Turbo", "description": "快速响应"},
            {"id": "qwen-plus", "name": "通义千问-Plus", "description": "增强版"},
            {"id": "qwen-max", "name": "通义千问-Max", "description": "最强能力"},
        ],
        "requires_base_url": False,
    },
    "custom": {
        "name": "自定义模型",
        "description": "Ollama、vLLM等本地部署模型",
        "base_url": None,
        "models": [
            {"id": "custom", "name": "自定义模型", "description": "用户自定义"},
        ],
        "requires_base_url": True,
    }
}
