"""医疗健康咨询Agent主类"""
from typing import Dict, Any, AsyncGenerator
from app.agent.llm_factory import LLMFactory
from app.agent.safety_filter import SafetyFilter
from app.agent.knowledge_base import MedicalKnowledgeBase
from app.agent.memory import ConversationMemory
from app.agent.prompt_templates import SYSTEM_PROMPT, EMERGENCY_RESPONSE


class MedicalAgent:
    """医疗健康咨询Agent"""
    
    def __init__(self):
        self.llm_factory = LLMFactory()
        self.safety_filter = SafetyFilter()
        self.knowledge_base = MedicalKnowledgeBase()
        self.memory = ConversationMemory()
    
    def _build_prompt(self, user_input: str, conversation_id: str) -> tuple:
        """构建Prompt，返回 (prompt_text, knowledge_context)"""
        knowledge_context = self.knowledge_base.search(user_input)
        chat_history = self.memory.get_history(conversation_id)
        prompt = SYSTEM_PROMPT.format(
            knowledge_context=knowledge_context,
            chat_history=chat_history
        )
        return prompt, knowledge_context

    async def process(self, user_input: str, conversation_id: str, user_id: int, db=None) -> Dict[str, Any]:
        """处理用户输入，返回建议"""
        # 1. 安全检查
        safety_result = self.safety_filter.check_input(user_input)
        if safety_result.is_emergency:
            return {"advice": EMERGENCY_RESPONSE, "metadata": {"type": "emergency"}}
        
        # 2. 获取LLM
        try:
            llm = self.llm_factory.create_llm(user_id, db)
        except ValueError as e:
            return {"advice": f"⚠️ 模型配置错误：{str(e)}\n\n请在设置页面配置您的API Key。", "metadata": {"type": "error", "error": str(e)}}
        
        # 3. 构建Prompt
        prompt, knowledge_context = self._build_prompt(user_input, conversation_id)
        
        # 4. 调用LLM
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            messages = [SystemMessage(content=prompt), HumanMessage(content=user_input)]
            response = llm.invoke(messages)
            advice = response.content
            tokens_used = 0
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                tokens_used = response.usage_metadata.get('total_tokens', 0)
        except Exception as e:
            return {"advice": f"⚠️ AI模型调用失败：{str(e)}\n\n请检查您的API Key配置是否正确。", "metadata": {"type": "error", "error": str(e)}}
        
        # 5. 安全过滤 + 保存
        safe_advice = self.safety_filter.filter_response(advice)
        self.memory.save_turn(conversation_id, user_input, safe_advice)
        
        return {
            "advice": safe_advice,
            "metadata": {"model": getattr(llm, 'model_name', 'unknown'), "tokens_used": tokens_used}
        }
    
    async def process_stream(self, user_input: str, conversation_id: str, user_id: int, db=None) -> AsyncGenerator[str, None]:
        """流式处理用户输入，逐token输出"""
        import json

        # 1. 安全检查
        safety_result = self.safety_filter.check_input(user_input)
        if safety_result.is_emergency:
            yield f"data: {json.dumps({'type': 'content', 'text': EMERGENCY_RESPONSE})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return
        
        # 2. 获取LLM
        try:
            llm = self.llm_factory.create_llm(user_id, db)
        except ValueError as e:
            msg = f"⚠️ 模型配置错误：{str(e)}\n\n请在设置页面配置您的API Key。"
            yield f"data: {json.dumps({'type': 'content', 'text': msg})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return
        
        # 3. 构建Prompt
        prompt, _ = self._build_prompt(user_input, conversation_id)
        
        # 4. 流式调用LLM
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            messages = [SystemMessage(content=prompt), HumanMessage(content=user_input)]
            
            full_response = ""
            for chunk in llm.stream(messages):
                token = chunk.content
                if token:
                    full_response += token
                    yield f"data: {json.dumps({'type': 'content', 'text': token})}\n\n"
            
            # 5. 安全过滤完整回复
            safe_advice = self.safety_filter.filter_response(full_response)
            # 如果过滤后内容有变化，发送修正
            if safe_advice != full_response:
                yield f"data: {json.dumps({'type': 'correct', 'text': safe_advice})}\n\n"
            
            # 6. 保存对话历史
            self.memory.save_turn(conversation_id, user_input, safe_advice)
            
        except Exception as e:
            err_msg = f"⚠️ AI模型调用失败：{str(e)}\n\n请检查您的API Key配置是否正确。"
            yield f"data: {json.dumps({'type': 'content', 'text': err_msg})}\n\n"
        
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
