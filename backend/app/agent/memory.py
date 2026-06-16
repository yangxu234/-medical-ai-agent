"""对话记忆管理"""
from typing import Dict, List, Optional
from collections import defaultdict


class ConversationMemory:
    """对话记忆管理器
    
    使用简单的内存存储管理对话历史
    生产环境建议使用Redis或数据库存储
    """
    
    def __init__(self, max_turns: int = 10):
        """
        Args:
            max_turns: 保留的最大对话轮数
        """
        self.max_turns = max_turns
        self.memories: Dict[str, List[dict]] = defaultdict(list)
    
    def get_history(self, conversation_id: str) -> str:
        """获取格式化的对话历史"""
        messages = self.memories.get(conversation_id, [])
        
        if not messages:
            return "暂无对话历史"
        
        history = []
        for msg in messages:
            role = "用户" if msg["role"] == "user" else "助手"
            history.append(f"{role}: {msg['content']}")
        
        return "\n".join(history)
    
    def get_history_list(self, conversation_id: str) -> List[dict]:
        """获取对话历史列表"""
        return self.memories.get(conversation_id, [])
    
    def save_turn(self, conversation_id: str, user_msg: str, ai_msg: str):
        """保存一轮对话"""
        messages = self.memories[conversation_id]
        
        # 添加用户消息
        messages.append({"role": "user", "content": user_msg})
        
        # 添加AI回复
        messages.append({"role": "assistant", "content": ai_msg})
        
        # 限制历史长度
        if len(messages) > self.max_turns * 2:
            self.memories[conversation_id] = messages[-(self.max_turns * 2):]
    
    def clear(self, conversation_id: str):
        """清空对话历史"""
        if conversation_id in self.memories:
            del self.memories[conversation_id]
    
    def extract_symptoms(self, conversation_id: str) -> List[str]:
        """从对话历史中提取症状关键词"""
        messages = self.memories.get(conversation_id, [])
        
        symptoms = []
        symptom_keywords = [
            "头痛", "头晕", "恶心", "呕吐", "发烧", "发热", "咳嗽",
            "胸闷", "心悸", "腹痛", "腹泻", "便秘", "失眠", "乏力",
            "疼痛", "肿胀", "瘙痒", "皮疹"
        ]
        
        for msg in messages:
            if msg["role"] == "user":
                for keyword in symptom_keywords:
                    if keyword in msg["content"] and keyword not in symptoms:
                        symptoms.append(keyword)
        
        return symptoms
