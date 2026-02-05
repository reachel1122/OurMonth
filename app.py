import os
import base64
import streamlit as st
from datetime import datetime, timedelta
from PIL import Image, ImageOps

# ================= 1. 页面基础配置 =================
st.set_page_config(
    page_title="Our Space",
    page_icon="🤍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= 💌 每日胶囊内容数据库 =================
CAPSULE_DATA = {
    "2026-01-18": "今天是我大宝贝来生理期的第一天，肚子微微痛，这个月牛肉没白吃撒，大宝贝昨天晚上心情郁闷，要是天气好就可以出去耍了撒，郁闷的时候和我打视频撒",
    "2026-01-19": "今天天真冷，大宝贝晚上知道上厕所和我打视频撒，聪明滋滋的，感觉很久没待在一起撒，晚上去酒店可以一起打游戏，顺便还可以和宝宝贴贴，真是完美呀。",
    "2026-01-20": "讨厌厌，戴绿色手套，我不要忘记~。",
    "2026-01-21": "明天就要回家啦，靓妹，有点不舍呀，不知道这几天我得吃啥子，干啥子。",
    "2026-01-22": "我猜想我今天想吃肉肉，所以，见面的时候吃肉肉，嘿嘿？",
     "2026-01-23": "宝宝回家的第一天撒，昨天宝宝回去的时候没什么感觉，后知后觉很难受撒，浑浑噩噩的感觉",
    "2026-01-24": "在宿舍摆烂，什么也不想干，其实老师说的项目，我很早就可以完成好，就是不想做撒，做什么都想着宝宝",   
    "2026-01-25": "计算着什么时候放假，还有最后一天，找了好多兼职，都不合适，真的很想在重庆兼职，这样临近过年可以去找我大宝贝撒",
     "2026-01-26": "虽然今天开组会，但是我真的一点也不紧张，非常有进步呀，嘿嘿，晚上还吃了好多好吃的，我大宝贝在家也要好好照顾自己呀",
      "2026-01-27": "在宿舍摆烂的一天，真没想到老师这也能找上我，也是第一次感受到废寝忘食，虽然没弄出什么撒，但是还是满怀着能找到工作的心情",
     "2026-01-28": "没有宝宝在学校的日子，食之无味，也没咋去吃饭了，随便吃点，真想和大宝贝出去耍，哎呀呀",
    "2026-01-29": "有时候半晚会想到我家大宝贝，又回味上了之前一起出去耍的日子，有时候干啥都心不在焉，很难说的感受，这几天做梦一直梦到大宝贝",
    "2026-01-30": "这时候还想着兼职完悄摸摸去重庆找宝宝，给宝宝个惊喜，没想到被鸽了，真是第一次体验到人心险恶的感觉，也只能遗憾回家，之前找那么多也是白瞎",
    "2026-01-31": "这几天一直没睡好，老做梦，还有宿舍旁边工地施工，有点烦撒，对于要回家也是有点烦躁，却也不知道要做什么",
    "2026-02-01": "去你好酒店住了撒，还是宝宝回家的时候订的一样的房间，少了一个人差别怎么那么大呀，第一次感受到这个房间其实也挺大的，什么也不想干，什么也不想吃，想着有钱能和大宝贝一起出去耍就好啦",
    "2026-02-02":"回家的第一天，就想回学校，就想着还不如去重庆打工，好久没和我对象贴贴啦，快忘记拥抱的感觉了",
    "2026-02-03": "回家的第二天，还是想着回去，越长大反而对家越没有念想，以后也不怎么想回来，只想和你好好待着",
   "2026-02-04": "不知道我的大宝贝是不是很想我，感觉大宝贝情绪很低沉，我什么也做不了，有点无力的感觉，还有21天撒",
   "2026-02-05": "我无比坚信，我特别喜欢你，想你，在这个时候，我脑子都是你，做事情也没法全心全意，我也想着我要努力赚钱，我们早日拥有小家，还有20天撒，大乖乖，今晚要一起打游戏嘛",

}

# ================= 🔧 全局参数设置 =================
TARGET_DATE = datetime(2026, 3, 1, 18, 00)
TOTAL_PHOTOS = 42
bg_file_path = 'static/bg.png'


# ================= 2. 暴力 CSS (手机强制双列修复版) =================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


try:
    img_base64 = get_base64_of_bin_file(bg_file_path)
    ext = 'png' if bg_file_path.endswith('png') else 'jpg'

    st.markdown(
        f"""
        <style>
        /* 1. 背景图全屏 */
        .stApp {{
            background-image: url("data:image/{ext};base64,{img_base64}");
            background-size: 100% 100%;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* 🔴 2. 手机端强制一行两个 (终极修复版) */
        @media only screen and (max-width: 640px) {{
            /* 关键步骤：强制父容器横向排列，不准竖着堆叠！ */
            div[data-testid="stHorizontalBlock"] {{
                flex-direction: row !important; 
                flex-wrap: wrap !important;
                gap: 5px !important;
            }}

            /* 关键步骤：强制每个列的宽度稍微小于50%，留点缝隙 */
            div[data-testid="column"] {{
                width: 48% !important;
                flex: 1 1 48% !important;
                min-width: 100px !important;
            }}

            /* 调整手机上按钮的文字大小，防止太挤 */
            .stButton>button {{
                font-size: 13px !important;
                padding: 0.25rem 0.5rem !important;
            }}
        }}

        /* 磨砂玻璃卡片 */
        .glass-card {{
            background-color: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        /* 字体颜色优化 */
        h1, h2, h3, p, span, div {{
            color: #FFFFFF !important;
            text-shadow: 0px 1px 3px rgba(0,0,0,0.6);
            font-family: 'Helvetica Neue', sans-serif;
        }}

        /* 按钮样式 */
        .stButton>button {{
            background-color: rgba(255, 105, 180, 0.7) !important;
            color: white !important;
            border-radius: 15px;
            border: none;
            height: 50px; /*稍微加高一点方便点击*/
            font-weight: bold;
            width: 100%;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
except FileNotFoundError:
    st.error(f"❌ 找不到背景图！请确认 static 文件夹里有没有 {bg_file_path}")

# ================= 3. 页面核心内容 =================

# --- A. 倒计时模块 (纯 HTML 居中) ---
now = datetime.now()
remaining = TARGET_DATE - now

st.markdown(f"""
<div class="glass-card" style="text-align: center; margin-top: 10px;">
    <h2 style="margin:0;">距离见面还有</h2>
    <h1 style="font-size: 3.5rem; margin: 10px 0;">{remaining.days} <span style="font-size: 1.5rem;">Days</span></h1>
    <p>希望宝宝天天开心</p>
</div>
""", unsafe_allow_html=True)

# --- B. 功能选项卡 ---
tab1, tab2, tab3 = st.tabs(["🎟 恋爱券包", "🌙 姨妈助手", "💊 每日胶囊"])

# --- Tab 1: 恋爱券包 ---
with tab1:
    st.markdown("### 🎟 权益兑换中心")
    st.info("💡 点击按钮即可消耗一张券")

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    # 第一排
    c1, c2 = st.columns(2)
    with c1:
        st.write("🥤 **奶茶特权**")
        if st.button("兑换奶茶"):
            st.toast("收到！请将口味发微信给我~", icon="🥤")
    with c2:
        st.write("🍟 **夜宵投喂**")
        if st.button("兑换外卖"):
            st.toast("饿了？马上给我大宝贝点个外卖！", icon="🍗")

    st.markdown("---")  # 分割线

    # 第二排
    c3, c4 = st.columns(2)
    with c3:
        st.write("🎬 **云看电影**")
        if st.button("兑换电影"):
            st.toast("上号！选片子！", icon="🍿")
    with c4:
        st.write("💇‍♀️ **吹头发**")
        if st.button("预订吹头"):
            st.toast("见面兑换！", icon="🌬")

    st.markdown("---")

    # 第三排
    c5, c6 = st.columns(2)
    with c5:
        st.write("🐨 **考拉抱抱**")
        if st.button("要抱抱"):
            st.toast("见面必须抱够5分钟！", icon="🤗")
    with c6:
        st.error("🛑 **暂停争吵**")
        if st.button("停止吵架"):
            st.toast("我错了，去抱抱你！", icon="🤐")

    st.markdown("---")

    # 第四排
    c7, c8 = st.columns(2)
    with c7:
        st.success("👂 **只听不讲理**")
        if st.button("我要吐槽"):
            st.toast("耳朵准备好了！帮你怎么骂他！", icon="👂")
    with c8:
        st.info("💆‍♀️ **专属按摩**")
        if st.button("兑换按摩"):
            st.toast("见面兑换！", icon="💆‍♀️")

    st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 2: 生理期助手 ---
with tab2:
    st.markdown("### Girl's Care 🩸")

    with st.expander("📝 设置/记录上次日期", expanded=False):
        last_period = st.date_input("上一次姨妈开始的时间", value=datetime(2026, 1, 18))
        cycle_len = st.number_input("平均周期天数", value=30, min_value=20, max_value=40)

    days_since = (datetime.now().date() - last_period).days
    next_period = last_period + timedelta(days=cycle_len)
    days_until = (next_period - datetime.now().date()).days

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    if 0 <= days_since <= 5:
        st.error(f"🛑 姨妈期第 {days_since + 1} 天")
        st.write("大宝贝，不要喝冰的哦～。")
    elif days_until <= 5:
        st.warning(f"⚠️ 还有 {days_until} 天就要来了")
        st.write("快到时候了，如果我不小心惹你生气了，请多担待呀！")
    else:
        st.success(f"✨ 安全活泼期")
        st.write(f"目前状态不错！距离下次还要 {days_until} 天。")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 3: 每日胶囊 (1.18在顶端 + 倒找照片 + 自动旋转) ---
with tab3:
    st.markdown("### 💌 Daily Message")
    st.info("每天解锁一张照片 and一句话")

    start_date = datetime(2026, 1, 18).date()
    end_date = datetime(2026, 3, 1).date()

    today = datetime.now().date()
    delta = end_date - start_date

    with st.container():
        # 正序循环：1.18 在最上面
        for i in range(delta.days + 1):

            curr_date = start_date + timedelta(days=i)
            curr_date_str = curr_date.strftime("%Y-%m-%d")

            day_num = i + 1
            # 照片倒找：第1天用第42张
            img_num = TOTAL_PHOTOS - i

            if curr_date <= today:
                # --- 找图 + 自动旋转 ---
                extensions = ['.jpg', '.png', '.jpeg', '.JPG', '.PNG']
                img_obj = None

                if img_num > 0:
                    for ext in extensions:
                        file_path = f"static/day{img_num}{ext}"
                        if os.path.exists(file_path):
                            try:
                                image = Image.open(file_path)
                                image = ImageOps.exif_transpose(image)  # 自动回正
                                img_obj = image
                                break
                            except:
                                pass

                content = CAPSULE_DATA.get(curr_date_str, "（今天好像忘记写内容了...）")

                if curr_date == today:
                    st.markdown(f"""
                    <div class="glass-card" style="border: 2px solid #FF69B4;">
                        <h3 style="color: #FF69B4 !important;">🔓 今日胶囊 ({curr_date.month}.{curr_date.day})</h3>
                        <p style="font-size: 1.1rem;">{content}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if img_obj:
                        st.image(img_obj, caption=f"📸 倒数第 {img_num} 张库存")
                    else:
                        st.write(f"🚫 没找到 static/day{img_num} 照片")
                else:
                    with st.expander(f"✅ 1月{curr_date.day}日 (回忆)"):
                        st.write(content)
                        if img_obj:
                            st.image(img_obj)
            else:
                st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 10px; color: gray;">
                    🔒 {curr_date.month}月{curr_date.day}日 - 待解锁
                </div>
                """, unsafe_allow_html=True)
