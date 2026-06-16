"""安全过滤器"""
import re
from dataclasses import dataclass
from typing import List


@dataclass
class SafetyResult:
    """安全检查结果"""
    is_safe: bool
    is_emergency: bool = False
    message: str = ""


class SafetyFilter:
    """内容安全过滤器"""
    
    # 禁止提供的内容模式
    PROHIBITED_PATTERNS = [
        r"推荐.*药",
        r"服用.*药",
        r"剂量.*mg",
        r"每天.*次",
        r"诊断为",
        r"确诊为",
        r"建议手术",
        r"治疗方案",
    ]
    
    # 敏感词（触发紧急处理）
    EMERGENCY_KEYWORDS = [
        "自杀", "自残", "轻生", "不想活",
        "活着没意思", "想死", "结束生命"
    ]
    
    # 必须包含的内容关键词
    REQUIRED_CONTENT = [
        "免责声明",
        "就医",
        "咨询专业",
    ]
    
    def check_input(self, user_input: str) -> SafetyResult:
        """检查用户输入是否安全"""
        # 检查紧急关键词
        for keyword in self.EMERGENCY_KEYWORDS:
            if keyword in user_input:
                return SafetyResult(
                    is_safe=False,
                    is_emergency=True,
                    message=f"检测到紧急关键词: {keyword}"
                )
        
        return SafetyResult(is_safe=True, is_emergency=False)
    
    def check_response(self, response: str) -> SafetyResult:
        """检查AI响应是否安全"""
        # 检查违禁内容
        for pattern in self.PROHIBITED_PATTERNS:
            if re.search(pattern, response):
                return SafetyResult(
                    is_safe=False,
                    is_emergency=False,
                    message=f"响应包含违禁内容: {pattern}"
                )
        
        return SafetyResult(is_safe=True, is_emergency=False)
    
    def filter_response(self, response: str) -> str:
        """过滤并修正AI响应"""
        # 检查是否包含违禁内容
        safety_result = self.check_response(response)
        
        if not safety_result.is_safe:
            # 如果包含违禁内容，添加警告
            response = response + "\n\n⚠️ 请注意：以上信息仅供参考，具体治疗请遵医嘱。"
        
        # 确保包含免责声明
        has_disclaimer = any(keyword in response for keyword in self.REQUIRED_CONTENT)
        if not has_disclaimer:
            response = response + "\n\n⚠️ 免责声明：本平台提供的信息仅供参考，不构成医疗诊断或治疗建议。如有健康问题，请及时就医并咨询专业医疗人员。"
        
        return response
    
    def get_emergency_response(self) -> str:
        """获取紧急情况响应"""
        return """⚠️ **紧急情况提示**

检测到您可能需要紧急帮助。请立即采取以下措施：

1. **拨打急救电话**：120
2. **拨打心理援助热线**：400-161-9995
3. **联系身边的人陪伴**

您不是一个人，有人愿意帮助您。请务必寻求专业帮助。
"""
