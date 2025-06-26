import streamlit as st
import pandas as pd
from utils import tcm_diagnosis_agent

st.set_page_config(page_title="中医智能诊疗助手", page_icon="🌿", layout="wide")
st.title("🌿 中医智能诊疗助手")

# 1. 四诊信息录入
with st.expander("🔍 四诊信息采集"):
    st.subheader("望诊")
    complexion = st.selectbox("面色", ["正常", "苍白", "潮红", "萎黄", "青紫", "黧黑"])
    tongue = st.text_area("舌象（舌质、舌苔）", placeholder="例：舌质淡红，苔薄白")

    st.subheader("闻诊")
    voice = st.selectbox("声音", ["正常", "低微", "洪亮", "嘶哑"])
    breath = st.selectbox("呼吸", ["正常", "气促", "气短", "喘促"])

    st.subheader("问诊")
    chief_complaint = st.text_area("主诉", placeholder="例：反复胃脘胀痛3月，加重1周")
    symptoms = st.multiselect("常见症状",
                              ["畏寒", "发热", "汗出", "头痛", "头晕", "胸闷", "心悸",
                               "胁痛", "胃脘痛", "腹胀", "便秘", "腹泻", "失眠", "多梦"])

    st.subheader("切诊")
    pulse = st.text_area("脉象", placeholder="例：脉弦细")
    abdomen = st.text_area("腹诊", placeholder="例：腹部柔软，无压痛")

# 2. 提交诊断
if st.button("生成中医诊断与治疗方案"):
    if not chief_complaint:
        st.warning("请输入主诉信息")
    else:
        with st.spinner("AI医师正在辨证施治..."):
            # 组织四诊数据
            diagnosis_data = {
                "complexion": complexion,
                "tongue": tongue,
                "voice": voice,
                "breath": breath,
                "chief_complaint": chief_complaint,
                "symptoms": symptoms,
                "pulse": pulse,
                "abdomen": abdomen
            }

            # 调用中医智能体
            result = tcm_diagnosis_agent(diagnosis_data)

            # 3. 结果展示
            st.subheader("🩺 辨证结果")
            st.write(f"**证型**: {result.get('syndrome', '未明确')}")
            st.write(f"**病机**: {result.get('pathogenesis', '待分析')}")

            st.subheader("💊 治疗方案")
            if "herbal_prescription" in result:
                st.write("**方药**: ", result["herbal_prescription"])
            if "acupuncture" in result:
                st.write("**针灸**: ", result["acupuncture"])
            if "diet" in result:
                st.write("**食疗**: ", result["diet"])

            st.subheader("🌱 养生建议")
            st.write(result.get("health_advice", "暂无特别建议"))