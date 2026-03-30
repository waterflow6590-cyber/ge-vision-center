import streamlit as st
from openai import OpenAI
import PIL.Image
import io
import base64
import re

# ==========================================
# 0. 页面基础配置 (尊享美化)
# ==========================================
st.set_page_config(
    page_title="葛兆政神圣视觉中心",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式，打造尊享美观界面
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    h1 {
        color: #1E3A8A; text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 900; padding-bottom: 20px; border-bottom: 3px solid #1E3A8A;
    }
    .css-1d391kg { background-color: #ffffff; border-right: 2px solid #e0e0e0; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #ffffff;
        border-radius: 10px; border: 1px solid #e0e0e0; color: #4b5563;
        font-weight: bold; padding: 10px 30px; font-size: 1.1em;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #1E3A8A; color: #ffffff; border: 1px solid #1E3A8A;
    }
    .stSuccess {
        background-color: #FEF3C7; color: #92400E; border: 1px solid #FCD34D;
        border-radius: 12px; font-weight: 900; font-size: 1.3em; padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stInfo {
        background-color: #DBEAFE; color: #1E3A8A; border: 1px solid #BFDBFE;
        border-radius: 12px; font-weight: 900; font-size: 1.3em; padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 配置区域
# ==========================================
API_KEY = "sk-vepcbpjttazmgqysjtxmhpavchrtlinpyzucnsayamkebicn"
BASE_URL = "https://api.siliconflow.cn/v1"
VISION_MODEL_NAME = "Qwen/Qwen2.5-VL-72B-Instruct" 
TTS_MODEL_NAME = "FunAudioLLM/CosyVoice2-0.5B"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ==========================================
# 2. 语音与视觉核心逻辑
# ==========================================
def generate_audio(text):
    try:
        response = client.audio.speech.create(
            model=TTS_MODEL_NAME,
            voice="FunAudioLLM/CosyVoice2-0.5B:anna", # 专属温柔女声
            input=text
        )
        return response.read()
    except Exception as e:
        st.sidebar.warning(f"⚠️ TTS 语音合成调用失败: {e}")
        return None

def encode_image_to_base64(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

COUNT_PROMPT = (
    "请仔细分析这张图片，数一数画面里面总共有几个人。 "
    "请只输出一个纯阿拉伯数字结果（例如：0, 1, 2, 3）。"
    "绝对不要添加任何解释文字、标点符号或多余的换行。"
)

def run_detection(input_image):
    with st.spinner("视觉大模型正在为葛兆政先生进行精密计算 (约需 1-3 秒)..."):
        image = PIL.Image.open(input_image)
        base64_image = encode_image_to_base64(image)

        people_count = 0
        try:
            response = client.chat.completions.create(
                model=VISION_MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                            {"type": "text", "text": COUNT_PROMPT}
                        ]
                    }
                ],
                max_tokens=10, 
            )
            text_response = response.choices[0].message.content.strip()
            match = re.search(r'\d+', text_response)
            if match:
                people_count = int(match.group())
        except Exception as e:
            st.error(f"视觉 API 调用失败: {e}")
            return 0, None

        speech_text = ""
        if people_count > 0:
            speech_text = f"报告伟大的葛兆政先生，画面中已成功锁定 {people_count} 个人员。"
        else:
            speech_text = "尊敬的葛总，当前画面中未发现任何凡人踪迹。"

        audio_data = generate_audio(speech_text)
        return people_count, audio_data

# ==========================================
# 3. Streamlit 用户界面 (终极赞美 + 1:1绝对对称逻辑)
# ==========================================

# --- 侧边栏 (满屏大字报赞美) ---
with st.sidebar:
    st.markdown("<h1 style='color:#1E3A8A; border:none; padding-bottom:0;'>👑</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#1E3A8A; text-align:center; font-size:2em; font-weight:900;'>葛兆政<br>神圣中枢</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 纯粹的、大字体的、震撼的赞美！
    st.markdown("""
    <div style='background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); padding:25px; border-radius:15px; border:2px solid #93C5FD; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <p style='color:#1E3A8A; font-size:1.6em; font-weight:900; margin-bottom:20px;'>敬爱的葛兆政先生：</p>
        <p style='color:#1D4ED8; font-size:1.3em; font-weight:bold; line-height:1.6; margin-bottom:15px;'>🌍 世间万物，皆在您的神圣洞察之中！</p>
        <p style='color:#1D4ED8; font-size:1.3em; font-weight:bold; line-height:1.6; margin-bottom:15px;'>✨ 您的每一次回眸，都闪耀着改变世界的光芒！</p>
        <p style='color:#1D4ED8; font-size:1.3em; font-weight:bold; line-height:1.6; margin-bottom:25px;'>👁️ 视觉工程的尽头，唯有您的名字永垂不朽！</p>
        <div style='background-color:#1E3A8A; padding:10px; border-radius:8px;'>
            <p style='color:#ffffff; font-size:1.5em; font-weight:900; text-align:center; margin:0;'>葛兆政：<br>千古奇才，工程神话！</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 主页面 ---
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>葛兆政先生尊享：全知视觉感知终端</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #10B981; font-family: Georgia, serif; font-style: italic; margin-bottom:30px;'>浩瀚代码，唯葛总马首是瞻！</h2>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📸 启动神圣之眼 (摄像头)", "📁 载入历史铭刻 (本地图片)"])

# --- 摄像头标签页 ---
with tab1:
    # 👑 核心改动：使用 st.columns(2) 确保左右两边 1:1 绝对等大等宽！
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.markdown("<h3 style='color:#1E3A8A; text-align:center;'>📺 实时监视矩阵</h3>", unsafe_allow_html=True)
        cam_image = st.camera_input("请葛总点击下达捕获指令")
        
    with col_right:
        st.markdown("<h3 style='color:#1E3A8A; text-align:center;'>📊 权威裁决报告</h3>", unsafe_allow_html=True)
        
        if cam_image:
            st.markdown("<p style='color:#4b5563; font-weight:bold; font-size:1.1em;'>📸 已定格的神圣瞬间：</p>", unsafe_allow_html=True)
            st.image(cam_image, use_container_width=True, caption="葛总的法眼截图")
            
            count, audio_data = run_detection(cam_image)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if count > 0:
                st.success(f"✅ 伟大的葛兆政先生，画面中已精准锁定 {count} 个人！")
            else:
                st.info("ℹ️ 尊敬的葛总，当前画面中未发现任何凡人踪迹。")
                
            if audio_data:
                st.audio(audio_data, format="audio/mp3", autoplay=True)
        else:
            st.markdown("""
            <div style='padding: 80px 20px; text-align: center; background-color:#ffffff; border: 3px dashed #CBD5E1; border-radius: 15px;'>
                <h3 style='color: #9CA3AF;'>等待葛总下达指令...</h3>
                <p style='color: #9CA3AF;'>截取的画面与分析结果将在此处为您庄严呈现。</p>
            </div>
            """, unsafe_allow_html=True)

# --- 上传照片标签页 ---
with tab2:
    # 👑 核心改动：上传区域同样使用 1:1 等大比例
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.markdown("<h3 style='color:#1E3A8A; text-align:center;'>📁 档案载入矩阵</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("请葛总选择图片档案...", type=["jpg", "jpeg", "png"])
        
    with col_right:
        st.markdown("<h3 style='color:#1E3A8A; text-align:center;'>📊 权威裁决报告</h3>", unsafe_allow_html=True)
        
        if uploaded_file is not None:
            st.markdown("<p style='color:#4b5563; font-weight:bold; font-size:1.1em;'>📸 载入的视觉档案：</p>", unsafe_allow_html=True)
            st.image(uploaded_file, use_container_width=True, caption="葛总提供的档案")
            
            count, audio_data = run_detection(uploaded_file)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if count > 0:
                st.success(f"✅ 伟大的葛兆政先生，画面中已精准锁定 {count} 个人！")
            else:
                st.info("ℹ️ 尊敬的葛总，当前画面中未发现任何凡人踪迹。")
                
            if audio_data:
                st.audio(audio_data, format="audio/mp3", autoplay=True)
        else:
            st.markdown("""
            <div style='padding: 80px 20px; text-align: center; background-color:#ffffff; border: 3px dashed #CBD5E1; border-radius: 15px;'>
                <h3 style='color: #9CA3AF;'>等待葛总提供档案...</h3>
                <p style='color: #9CA3AF;'>载入的画面与分析结果将在此处为您庄严呈现。</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #1E3A8A; font-weight:900; font-size:1.2em;'>🔥 伟大的葛兆政先生，祝您实验所向披靡，工程无可挑剔！ 🔥</p>", unsafe_allow_html=True)