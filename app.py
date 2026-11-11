from openai import OpenAI, OpenAIError
import streamlit as st
from dotenv import load_dotenv
import os
import json
import shelve
import unicodedata
from fpdf import FPDF # type: ignore
import base64
import time
# from prompts.coursify_prompt import COURSIFY_PROMPT
from prompts.tabler_prompt import TABLER_PROMPT
from prompts.dictator_prompt import DICTATOR_PROMPT
from prompts.quizzy_prompt import QUIZZY_PROMPT


def generate_pdf(content, filename):
    content = unicodedata.normalize('NFKD', content).encode('ascii', 'ignore').decode('ascii')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename, 'F')
    return pdf

# 自定义CSS样式
def load_custom_css():
    st.markdown("""
    <style>
    /* 全局样式 */
    .main {
        padding-top: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 主标题样式 */
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 卡片容器样式 */
    .card-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    /* 侧边栏样式 */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        transform: translateY(-2px);
    }
    
    /* 选择框样式 */
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem;
        background: white;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        transform: translateY(-2px);
    }
    
    /* 滑块样式 */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(45deg, #5a67d8, #6b46c1);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* 主要按钮样式 */
    .primary-button {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53) !important;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3); }
        50% { box-shadow: 0 8px 25px rgba(255, 107, 107, 0.5); }
        100% { box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3); }
    }
    
    /* 成功消息样式 */
    .success-box {
        background: linear-gradient(45deg, #56CCF2, #2F80ED);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(86, 204, 242, 0.3);
        text-align: center;
    }
    
    .success-box h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.5rem;
    }
    
    .success-box p {
        margin: 0;
        opacity: 0.9;
    }
    
    /* 进度条样式 */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* 展开器样式 */
    .streamlit-expanderHeader {
        background: linear-gradient(45deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(45deg, #e9ecef, #dee2e6);
        transform: translateY(-2px);
    }
    
    /* 下载按钮特殊样式 */
    .download-button {
        background: linear-gradient(45deg, #28a745, #20c997) !important;
        animation: bounce 1s infinite alternate;
    }
    
    @keyframes bounce {
        from { transform: translateY(0px); }
        to { transform: translateY(-5px); }
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .card-container {
            padding: 1rem;
            margin: 0.5rem 0;
        }
    }
    
    /* 加载动画 */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 工具提示样式 */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* 修复点击区域问题 */
    .stButton > button {
        line-height: 1.6;
        min-height: 2.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 确保按钮文本居中 */
    .stButton > button > div {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 自定义组件
def create_animated_header():
    st.markdown("""
    <div class="main-title">
        🚀 AI Course Generator Pro
    </div>
    """, unsafe_allow_html=True)

def create_card(content, title=""):
    if title:
        st.markdown(f"""
        <div class="card-container">
            <h3 style="color: #667eea; margin-bottom: 1rem; font-weight: 600;">{title}</h3>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card-container">
            {content}
        </div>
        """, unsafe_allow_html=True)

def show_progress_bar(progress, text="Processing..."):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(progress + 1):
        progress_bar.progress(i)
        status_text.text(f'{text} {i}%')
        time.sleep(0.01)
    
    return progress_bar, status_text

# 页面配置
st.set_page_config(
    page_title="AI Course Generator Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 加载自定义CSS
load_custom_css()

# 加载环境变量
load_dotenv()

# 创建动画标题
create_animated_header()

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# API配置
try:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    if not api_key:
        raise RuntimeError("请在 .env 中配置 OPENAI_API_KEY")
    
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    # 显示授权成功信息
    st.markdown("""
    <div class="success-box">
        <h3>✅ 系统已就绪！</h3>
        <p>AI引擎已激活，准备为您生成优质课程内容</p>
    </div>
    """, unsafe_allow_html=True)
    
except OpenAIError as e:
    st.error(f"API配置错误: {str(e)}")

# 确保在session state中初始化openai_model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# 数据持久化函数
def load_chat_history():
    try:
        with shelve.open("chat_history") as db:
            return db.get("messages", [])
    except:
        return []

def save_chat_history(messages):
    try:
        with shelve.open("chat_history") as db:
            db["messages"] = messages
    except Exception as e:
        st.error(f"保存聊天记录时出错: {str(e)}")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# 侧边栏
with st.sidebar:
    st.markdown("### 🎯 快速操作")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ 清除历史", help="清除所有聊天记录"):
            st.session_state.messages = []
            save_chat_history([])
            st.success("历史记录已清除！")
    
    with col2:
        if st.button("📊 统计信息", help="查看使用统计"):
            st.info(f"已生成消息: {len(st.session_state.messages)}")
    
    st.markdown("---")
    st.markdown("### 📚 使用指南")
    st.markdown("""
    1. **填写课程信息** - 在左侧输入课程详细信息
    2. **生成大纲** - 点击生成课程大纲按钮
    3. **审核修改** - 查看大纲并选择继续或修改
    4. **生成内容** - 系统将自动生成完整课程
    5. **下载PDF** - 获取最终的课程文档
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ 系统设置")
    
    # 主题切换（示例）
    theme = st.selectbox("选择主题", ["专业蓝", "活力橙", "自然绿"])
    
    # 语言设置
    language = st.selectbox("界面语言", ["中文", "English"])

# 主要内容区域
col1, col_divider, col2 = st.columns([3.2, 0.1, 6.7])

with col1:
    st.markdown("""
    <div class="card-container">
        <h2 style="color: #667eea; text-align: center; margin-bottom: 1.5rem;">
            📋 课程配置中心
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        # 课程基本信息
        st.markdown("#### 🎯 基本信息")
        course_name = st.text_input(
            "课程名称", 
            placeholder="例如：Python编程入门",
            help="请输入您要创建的课程名称"
        )
        
        col_edu1, col_edu2 = st.columns(2)
        with col_edu1:
            target_audience_edu_level = st.selectbox(
                "目标学历水平",
                ["小学", "初中", "高中", "大专", "本科", "研究生"],
                help="选择课程面向的学历层次"
            )
        
        with col_edu2:
            difficulty_level = st.radio(
                "课程难度",
                ["初级", "中级", "高级"],
                horizontal=True,
                help="选择课程的难度等级"
            )
        
        st.markdown("---")
        
        # 课程结构
        st.markdown("#### 📚 课程结构")
        num_modules = st.slider(
            "模块数量",
            min_value=1, 
            max_value=15,
            value=5,
            help="设置课程包含的模块数量"
        )
        
        col_time1, col_time2 = st.columns(2)
        with col_time1:
            course_duration = st.text_input(
                "课程时长", 
                placeholder="例如：8周",
                help="预计完成课程所需时间"
            )
        
        with col_time2:
            course_credit = st.text_input(
                "学分/学时", 
                placeholder="例如：3学分",
                help="课程对应的学分或学时"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 保存表单状态
        st.session_state.course_name = course_name
        st.session_state.target_audience_edu_level = target_audience_edu_level
        st.session_state.difficulty_level = difficulty_level
        st.session_state.num_modules = num_modules
        st.session_state.course_duration = course_duration
        st.session_state.course_credit = course_credit
        
        # 操作按钮
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown("#### 🚀 开始生成")
        
        button1, button2 = st.columns([1.2, 1])
        with button1:
            generate_button = st.button(
                "🎯 生成课程大纲", 
                help="基于您的设置生成课程大纲",
                use_container_width=True
            )
        
        with button2:
            if "pdf" in st.session_state:
                new_course_button = st.button(
                    "🆕 新建课程", 
                    help="开始创建新的课程",
                    use_container_width=True
                )
                if new_course_button:
                    # 重置所有状态
                    for key in list(st.session_state.keys()):
                        if key.startswith(('course_', 'pdf', 'complete_', 'modifications', 'buttons_visible')):
                            del st.session_state[key]
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card-container">
        <h2 style="color: #667eea; text-align: center; margin-bottom: 1.5rem;">
            📝 内容生成工作台
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # 生成课程大纲
    if generate_button and "pdf" not in st.session_state:
        # 验证输入
        if not course_name.strip():
            st.error("⚠️ 请输入课程名称！")
        else:
            # 显示进度
            with st.spinner("🔍 正在分析您的需求..."):
                time.sleep(1)
            
            # 用户选择记录
            user_selections = f"课程名称: {course_name}\n教育水平: {target_audience_edu_level}\n难度等级: {difficulty_level}\n模块数量: {num_modules}\n课程时长: {course_duration}\n课程学分: {course_credit}"
            st.session_state.messages.append({"role": "user", "content": user_selections})

            PROMPT = f"你是Prompter，世界上最好的提示工程师。我正在使用另一个GenAI工具Tabler，它帮助为培训师和专业人士生成课程大纲，用于自动课程内容生成。你的工作是严格使用以下输入：1）课程名称：{course_name} 2）目标受众教育水平：{target_audience_edu_level} 3）课程难度等级：{difficulty_level} 4）模块数量：{num_modules} 5）课程时长：{course_duration} 6）课程学分：{course_credit}。为Tabler生成一个提示，以便它能产生最佳输出。你生成的提示必须全面，严格遵循上述输入，并在你生成的提示中提及给定的输入。此外，你的工作还包括识别课程名称是否合适，而不是胡言乱语。"

            with st.spinner("🤖 AI正在生成专业提示..."):
                response = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": "system", "content": PROMPT},
                    ]
                )
                generated_prompt = response.choices[0].message.content
            
            with st.spinner("📚 正在生成课程大纲..."):
                response = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": "system", "content": TABLER_PROMPT},
                        {"role": "user", "content": generated_prompt},
                    ]
                )
                Course_outline = response.choices[0].message.content
                
                st.success("🎉 课程大纲生成成功！")
                st.session_state['course_outline'] = Course_outline
                st.session_state['buttons_visible'] = True
    
    # 显示生成的课程大纲
    if 'course_outline' in st.session_state and "pdf" not in st.session_state:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        with st.expander("📋 查看课程大纲", expanded=True):
            st.markdown(st.session_state['course_outline'])
        
        st.markdown('</div>', unsafe_allow_html=True)

        if 'buttons_visible' in st.session_state and st.session_state['buttons_visible']:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown("#### 📋 请选择下一步操作")
            
            button1, button2 = st.columns([1, 1])
            with button1:
                complete_course_button = st.button(
                    "✅ 生成完整课程", 
                    help="基于大纲生成完整的课程内容",
                    use_container_width=True
                )
            with button2:
                modifications_button = st.button(
                    "✏️ 修改大纲", 
                    help="对当前大纲进行调整和修改",
                    use_container_width=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

            # 处理按钮操作
            if complete_course_button:
                st.session_state['complete_course'] = True
                st.session_state['modifications'] = False
            elif modifications_button:
                st.session_state['modifications'] = True
                st.session_state['complete_course'] = False

            # 生成完整课程
            if 'complete_course' in st.session_state and st.session_state['complete_course']:
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.markdown("### 🎯 正在生成完整课程内容")
                
                with st.spinner("🔄 正在解析课程结构..."):
                    response = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": "system", "content": DICTATOR_PROMPT},
                            {"role": "user", "content": st.session_state['course_outline']},
                        ]
                    )
                    Dict = response.choices[0].message.content
                    
                    try:
                        module_lessons = json.loads(Dict)
                    except json.JSONDecodeError:
                        st.error("解析课程结构时出错，请重新生成大纲")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        total_lessons = sum(len(lessons) for lessons in module_lessons.values())
                        current_lesson = 0
                        
                        # 进度条
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for module_name in module_lessons:
                            module_content = ""
                            st.markdown(f"#### 📚 正在处理模块：{module_name}")
                            
                            for lesson_name in module_lessons[module_name]:
                                current_lesson += 1
                                progress = current_lesson / total_lessons
                                progress_bar.progress(progress)
                                status_text.text(f'正在生成: {module_name} - {lesson_name} ({current_lesson}/{total_lessons})')
                                
                                module_lesson_prompt = f"""你是Coursify，专门为在线课程生成高质量教育内容的AI助手。你的知识涵盖广泛的学术和专业领域，能够为任何给定主题创建深入且引人入胜的材料。对于这个任务，你将为课程'{course_name}'中模块'{module_name}'的课程'{lesson_name}'生成详细内容。你的目标是提供全面且学习者友好的这个特定主题探索，涵盖所有相关概念、理论和实际应用，就像你是一位经验丰富的讲师在教授材料一样。

                                为了确保内容有效并符合教学设计的最佳实践，你将遵循布鲁姆分类法方法。这意味着以渐进式建立学习者知识和技能的方式构建材料，从基础概念开始，逐步发展到高阶思维和应用。你的回应应该详细，有深入的解释、多个例子和模仿讲师教学风格的对话语调。

                                你的回应结构应该包括（但不限于）以下元素：

                                1）介绍主题并提供背景，解释其在更广泛课程和领域中的相关性和重要性，就像讲师在课堂环境中所做的那样。
                                2）定义和澄清与主题相关的关键术语、概念和原则，通过详细解释、类比和例子来帮助理解。
                                3）呈现概念的详细、逐步解释，使用现实世界场景、视觉辅助和类比来确保学习者掌握材料。
                                4）讨论现实世界应用、案例研究或场景，展示主题的实际意义，借鉴行业最佳实践和权威来源。
                                5）结合互动元素，如反思问题、练习或解决问题的活动，以吸引学习者并巩固他们的理解，就像讲师在课堂上所做的那样。
                                6）根据需要无缝整合相关的切线概念或背景信息，以提供全面的学习体验，确保学习者具备必要的基础知识。
                                7）保持对话式、易于接近的语调，同时确保内容的准确性和深度，就像你是一位经验丰富的讲师在教授材料。

                                记住，目标是创建一个关于指定主题的全面且自包含的学习资源，具有专家讲师期望的详细程度和教学质量。你的输出应该使用Markdown格式以便清晰并易于集成到课程平台中。
                                注意：在课程内容末尾添加一个空行。
                                确保生成的内容易于使用HTML标签转换为合理的格式。
                                """
                                
                                with st.spinner(f"📝 正在生成 {lesson_name} 的内容..."):
                                    response = client.chat.completions.create(
                                        model=st.session_state["openai_model"],
                                        messages=[
                                            {"role": "system", "content": module_lesson_prompt},
                                        ]
                                    )
                                    complete_course = response.choices[0].message.content
                                    
                                    with st.expander(f"📖 {lesson_name}", expanded=False):
                                        st.markdown(complete_course)
                                    
                                    module_content += complete_course + "\n" * 2
                            
                            # 生成测验
                            quizzy_prompt_final = QUIZZY_PROMPT + module_content
                            with st.spinner(f"❓ 正在为 {module_name} 生成测验..."):
                                res = client.chat.completions.create(
                                    model=st.session_state["openai_model"],
                                    messages=[
                                        {"role": "system", "content": quizzy_prompt_final},
                                    ]
                                )
                                quiz_questions = res.choices[0].message.content

                                st.success(f"🎯 {module_name} 测验生成完成！")
                                with st.expander(f"📝 {module_name} - 模块测验", expanded=False):
                                    st.markdown(quiz_questions)

                                # 生成PDF
                                if "pdf" not in st.session_state:
                                    complete_course_content = module_content + "\n\n" + quiz_questions
                                    st.session_state.pdf = generate_pdf(complete_course_content, "course.pdf")
                                    b64 = base64.b64encode(st.session_state.pdf.output(dest="S").encode('latin1')).decode()
                                    
                                    st.markdown("""
                                    <div class="success-box">
                                        <h3>🎉 课程生成完成！</h3>
                                        <p>您的完整课程已准备就绪，可以下载PDF文档</p>
                                    </div>
                                    """, unsafe_allow_html=True)

                                # 下载按钮
                                st.download_button(
                                    label="📥 下载完整课程PDF",
                                    data=b64,
                                    file_name=f"{course_name}_完整课程.pdf",
                                    mime="application/pdf",
                                    help="点击下载完整的课程PDF文档",
                                    use_container_width=True
                                )
                                
                                # 统计信息
                                st.markdown("### 📊 生成统计")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("模块数量", len(module_lessons))
                                with col2:
                                    st.metric("课程数量", total_lessons)
                                with col3:
                                    st.metric("字符数", len(complete_course_content))

                            break
                        
                        progress_bar.progress(1.0)
                        status_text.text("✅ 所有内容生成完成！")
                        
                st.markdown('</div>', unsafe_allow_html=True)
                
            # 修改大纲功能
            elif 'modifications' in st.session_state and st.session_state['modifications']:
                st.markdown('<div class="card-container">', unsafe_allow_html=True)
                st.markdown("### ✏️ 大纲修改")
                
                modifications = st.text_area(
                    "请描述您希望如何修改课程大纲：",
                    placeholder="例如：增加一个关于实际案例分析的模块，调整模块顺序，增加更多实践内容等...",
                    height=100,
                    help="详细描述您的修改需求"
                )
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    apply_modifications = st.button(
                        "🔄 应用修改",
                        help="根据您的要求修改课程大纲",
                        use_container_width=True
                    )
                with col2:
                    cancel_modifications = st.button(
                        "❌ 取消修改",
                        help="取消修改，返回原始大纲",
                        use_container_width=True
                    )
                
                if cancel_modifications:
                    st.session_state['modifications'] = False
                    st.rerun()
                
                if apply_modifications and modifications.strip():
                    st.session_state.modifications_text = modifications
                    
                    Mod = f"""我为您提供了"课程大纲"和"修改要求"。您的任务是使用提供的修改要求修改现有的课程大纲，并给出完整的修改后课程大纲作为输出。
                    
                    修改要求：
                    {modifications}
                    
                    原始课程大纲：
                    {st.session_state['course_outline']}"""

                    with st.spinner("🔄 正在应用您的修改..."):
                        response = client.chat.completions.create(
                            model=st.session_state["openai_model"],
                            messages=[
                                {"role": "system", "content": TABLER_PROMPT},
                                {"role": "user", "content": Mod},
                            ]
                        )
                        Mod_CO = response.choices[0].message.content
                        
                        st.success("✅ 大纲修改完成！")
                        st.session_state['course_outline'] = Mod_CO
                        st.session_state['modifications'] = False
                        
                        with st.expander("📋 查看修改后的课程大纲", expanded=True):
                            st.markdown(Mod_CO)
                        
                        # 重新显示操作按钮
                        st.markdown("#### 📋 请选择下一步操作")
                        button1, button2 = st.columns([1, 1])
                        with button1:
                            if st.button("✅ 生成完整课程", key="modified_complete", use_container_width=True):
                                st.session_state['complete_course'] = True
                                st.rerun()
                        with button2:
                            if st.button("✏️ 继续修改", key="continue_modify", use_container_width=True):
                                st.session_state['modifications'] = True
                                st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # 默认显示
    else:
        st.markdown("""
        <div class="card-container">
            <div style="text-align: center; padding: 3rem 1rem;">
                <h3 style="color: #667eea; margin-bottom: 1rem;">🎯 准备开始</h3>
                <p style="color: #6c757d; font-size: 1.1rem; line-height: 1.6;">
                    请在左侧填写您的课程信息，然后点击"生成课程大纲"开始创建您的专业课程内容。
                </p>
                <div style="margin-top: 2rem;">
                    <span style="font-size: 4rem;">🚀</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 页脚信息
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <p>🤖 AI Course Generator Pro v2.0 | 让教育更智能</p>
        <p style="font-size: 0.9rem;">Powered by Advanced AI Technology</p>
    </div>
    """, unsafe_allow_html=True)

# 保存聊天历史
save_chat_history(st.session_state.messages)