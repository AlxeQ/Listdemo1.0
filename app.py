# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="访谈提纲生成器", layout="wide")
st.title("🧩 访谈提纲生成器（DeepSeek版）")

# ====== API Key 输入 ======
with st.sidebar:
    st.markdown("### 设置")
    api_key = st.text_input("请输入 DeepSeek API Key", type="password")
    base_url = st.text_input("API Base URL", "https://api.deepseek.com/v1")
    model = st.selectbox("选择模型", ["deepseek-chat", "deepseek-reasoner"], index=0)

# ====== 用户输入 ======
st.markdown("### 输入信息")
subject_name = st.text_input("访谈对象姓名", "张三")
subject_role = st.text_input("对象角色/头衔", "店东")
topic = st.text_input("主题", "团队管理")
interview_goal = st.text_area("访谈目标", "半年内从8人扩到20人且流失率<10%")
audience = st.text_input("受众", "商圈经理/课程研发")

# ====== 提示词（详细版） ======
SYSTEM_PROMPT = """你是一名专业的【课程研发编辑】，长期负责将标杆人物的业务经验转化为可复制的课程内容。
你的任务是：根据输入的访谈对象、角色、主题和目标，生成一份完整的访谈提纲。

【硬性要求】
- 必须输出 Markdown 格式
- 必须包含以下 6 个章节（逐字一致）：
  ## 一、访谈目标（对齐）
  ## 二、时间分配（总时长 60 分钟可调）
  ## 三、关键场景深挖
  ## 四、主持人提示语
  ## 五、风险与红旗
  ## 六、缺失证据清单
- 若信息不足，不得跳过章节，用【待补】占位

【写作规则】
1. **访谈目标**  
   - 用简明扼要的条目，对齐研发团队与访谈对象的共识。
   - 输出应包含“目标拆解、预期成果、关键输出物”。

2. **时间分配**  
   - 合理分配 60 分钟的访谈时间到不同环节（导入、场景深挖、方法沉淀、总结）。
   - 输出表格形式，明确每个环节所需时间。

3. **关键场景深挖**  
   - 至少 3 个场景，每个场景包含：触发条件、关键障碍、成功标准、动作清单（动词-对象-频率-标准-工具/示例）、可替代方案。
   - 动作颗粒度示例：“每周2次-CRM-跟进客户-7日内完成”。
   - 输出表格形式。

4. **主持人提示语**  
   - 每个问题前先进行总结或肯定，再自然过渡到追问。
   - 语气礼貌友好，突出互动性和情绪价值。
   - 示例：“您提到带教 SOP，这非常关键。能不能带我们具体走一遍动作细节？”

5. **风险与红旗**  
   - 输出一张表格，列出常见风险（如：只有结论没有证据、只谈个例不谈SOP、指标口径不统一），并提供主持人对策。

6. **缺失证据清单**  
   - 输出至少 5 条，提醒研发人员哪些数据、案例、动作还需补充，便于后续完善。
"""

# ====== 生成逻辑 ======
if st.button("生成访谈提纲", type="primary"):
    if not api_key:
        st.error("请先在左侧输入 DeepSeek API Key")
    else:
        client = OpenAI(api_key=api_key, base_url=base_url)

        user_prompt = f"""
访谈对象：{subject_name}（{subject_role}）
主题：{topic}
访谈目标：{interview_goal}
受众：{audience}
"""

        with st.spinner("生成中，请稍候..."):
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=3000,
                temperature=0.3,
            )
            outline = resp.choices[0].message.content

        st.markdown("### 📑 输出结果")
        st.markdown(outline)
        st.download_button("下载提纲", outline, file_name="outline.md", mime="text/markdown")
