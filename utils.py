import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
# utils.py
import os
from dotenv import load_dotenv


def tcm_diagnosis_agent(diagnosis_data):
    # load_dotenv()  # 确保.env文件被加载

    model = ChatOpenAI(
        base_url="https://api.deepseek.com/",  # 移除XML标签，保持纯URL
        api_key="sk-20353aca745c417694cf1b3c0af9db17",  # 直接传入密钥
        model="deepseek-reasoner",
        temperature=0.3,
        max_tokens=2048
    )
    # ...后续代码不变...
# 中医辨证施治提示词
TCM_PROMPT = """你是一位资深中医师，请根据以下四诊信息完成辨证施治：
{diagnosis_data}

请严格按照以下JSON格式输出：
{{
    "syndrome": "证型名称（如：肝郁脾虚证）",
    "pathogenesis": "病机分析（50字以内）",
    "herbal_prescription": "推荐方药（如：逍遥散加减）",
    "acupuncture": "针灸方案（可选）",
    "diet": "食疗建议（可选）",
    "health_advice": "养生调护建议（100字以内）"
}}

要求：
1. 证型需符合《中医诊断学》标准
2. 方药需注明剂量范围
3. 输出必须为合法JSON格式
4. 禁止使用西药相关内容
"""


def tcm_diagnosis_agent(diagnosis_data):
    load_dotenv()
    model = ChatOpenAI(
        base_url='https://api.deepseek.com/',
        model="deepseek-reasoner",
        temperature=0.3,  # 降低随机性保证医疗严谨性
        max_tokens=2048
    )

    prompt = PromptTemplate(
        input_variables=["diagnosis_data"],
        template=TCM_PROMPT
    )

    try:
        response = model.invoke(prompt.format(diagnosis_data=json.dumps(diagnosis_data, ensure_ascii=False)))
        return json.loads(response.content)
    except Exception as e:
        print(f"中医智能体错误: {e}")
        return {
            "syndrome": "辨证失败",
            "pathogenesis": "系统暂时无法分析",
            "health_advice": "建议咨询线下中医师"
        }