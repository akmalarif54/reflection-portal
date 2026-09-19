import streamlit as st
import requests
import calendar
import random
from datetime import datetime, date
from praytimes import PrayTimes
import news_data

# Set centered wide layout page width
st.set_page_config(page_title="The Reflection Portal", page_icon="🕌", layout="centered")

# --- INITIALIZE SESSION STATES ---
if 'tasbih_count' not in st.session_state:
    st.session_state.tasbih_count = 0
if 'tasbih_phrase' not in st.session_state:
    st.session_state.tasbih_phrase = "SubhanAllah"
if 'cal_month_offset' not in st.session_state:
    st.session_state.cal_month_offset = 0
if 'water_ml' not in st.session_state:
    st.session_state.water_ml = 0
if 'current_hadith_idx' not in st.session_state:
    st.session_state.current_hadith_idx = datetime.now().day

# --- GORGEOUS MODERNISED THEME STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7 !important; color: #2C2520 !important; font-family: 'Inter', sans-serif; }
    *::selection { background: #F7F3EB !important; color: #A3843B !important; }
    *::-moz-selection { background: #F7F3EB !important; color: #A3843B !important; }
    /* Gilded Frame Card Container */
    .islamic-card { background-color: #FFFFFF; padding: 30px; border-radius: 20px; border-top: 5px solid #D4AF37; box-shadow: 0 4px 20px rgba(212, 175, 55, 0.08); margin-bottom: 25px; }
    .hadith-text { font-size: 1.2rem; font-style: italic; color: #4A3E3D; line-height: 1.6; text-align: center; margin-bottom: 12px; padding: 0 20px; }
    .hadith-source { font-size: 0.85rem; color: #8C7A6B; text-align: center; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; }

    /* Modern Prayer Metric Grid Boxes */
    .prayer-grid { display: flex; justify-content: space-between; gap: 10px; margin-bottom: 25px; }
    .prayer-box { background: #FFFFFF; border: 1px solid #EADCC9; border-radius: 12px; padding: 15px; text-align: center; flex: 1; box-shadow: 0 2px 12px rgba(0,0,0,0.01); }
    .prayer-name { font-size: 0.85rem; color: #8C7A6B; font-weight: 500; text-transform: uppercase; }
    .prayer-time { font-size: 1.25rem; color: #A3843B; font-weight: 700; margin-top: 4px; }

    /* Utility Quick Tracker Cards */
    .utility-card { background-color: #FFFFFF; padding: 22px; border-radius: 16px; border: 1px solid #EADCC9; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.01); }

    /* Calendar Header & Day Blocks */
    .calendar-header { text-align: center; font-size: 1.25rem; font-weight: 600; color: #A3843B; margin-top: 5px; line-height: 1.4; }
    .day-box { background-color: #FFFFFF; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #EADCC9; margin: 2px; }
    .day-box-active { background-color: #F7F3EB; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #D4AF37; margin: 2px; font-weight: bold; }

    /* News & Knowledge Cards */
    .news-card { background-color: #FFFFFF; padding: 22px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid #D4AF37; box-shadow: 0 2px 10px rgba(0,0,0,0.01); }
    .news-title { font-size: 1.1rem; font-weight: 600; color: #A3843B; margin-bottom: 5px; }
    .knowledge-card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #EADCC9; margin-bottom: 15px; }
    .knowledge-title { font-size: 1.05rem; font-weight: 600; color: #2C2520; border-bottom: 2px solid #F7F3EB; padding-bottom: 6px; margin-bottom: 8px; }

    h1, h2, h3, p, span, label { color: #2C2520 !important; }

    /* Global Transparent and Visible Buttons */
    div.stButton > button {
        background-color: #FFFFFF !important; color: #A3843B !important;
        border: 1px solid #EADCC9 !important; border-radius: 8px !important;
        font-weight: 500 !important; transition: all 0.2s ease;
    }

    div.stButton > button:hover { background-color: #F7F3EB !important; border-color: #D4AF37 !important; color: #2C2520 !important; }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Branding Headers
st.markdown("<h1 style='text-align: center; color: #A3843B !important; font-weight: 300;'>🕌 THE REFLECTION PORTAL</h1>", unsafe_allow_html=True)

# Live dynamic Hijri date and times fetching
hijri_display_str = "8 Rabi' al-Thani 1448 AH"
lat, lon = 3.0333, 101.4500
timings = {}

try:
    url = f"https://aladhan.com"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3).json()
    if response["code"] == 200:
        timings = response["data"]["timings"]
        h_data = response["data"]["date"]["hijri"]
        hijri_display_str = f"{h_data['day']} {h_data['month']['en']} {h_data['year']} AH"
except:
    pass

st.markdown(f"<p style='text-align: center; color: #8C7A6B !important; font-size: 1.1rem; margin-top: -10px;'>🌙 {hijri_display_str} | Klang, Selangor</p>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #D4AF37; margin-bottom: 25px;'>✦ ═══ 🕌 ═══ ✦</div>", unsafe_allow_html=True)

# Navigation Structural Workspace Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✨ Prayer & Utilities",
    "📅 Islamic Calendar",
    "📿 Interactive Tasbih",
    "📈 Global Finance News",
    "📖 Shariah Knowledge"
])

# ================= TAB 1: PRAYER & UTILITIES =================
with tab1:
    hadiths = [
        {"text": "“The best among you are those who have the best manners and character.”", "source": "Sahih al-Bukhari"},
        {"text": "“Cleanliness is half of faith.”", "source": "Sahih Muslim"},
        {"text": "“A Muslim is the one from whose tongue and hands the Muslims are safe.”", "source": "Sahih al-Bukhari"},
        {"text": "“Make things easy for people and do not make them difficult.”", "source": "Sahih al-Bukhari"}
    ]

    selected_hadith = hadiths[st.session_state.current_hadith_idx % len(hadiths)]
    st.markdown(f"<div class='islamic-card'><div class='hadith-text'>“{selected_hadith['text']}”</div><div class='hadith-source'>— {selected_hadith['source']}</div></div>", unsafe_allow_html=True)

    h_col1, h_col2, h_col3 = st.columns(3)
    with h_col2:
        if st.button("🔄 Shuffle Hadith", use_container_width=True):
            st.session_state.current_hadith_idx = random.randint(0, 100)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🕒 Daily Prayer Windows")
    if not timings:
        PT = PrayTimes('Egypt')
        times = PT.getTimes(datetime.now().date(), (lat, lon), 8)
        timings = {"Fajr": times["fajr"], "Dhuhr": times["dhuhr"], "Asr": times["asr"], "Maghrib": times["maghrib"], "Isha": times["isha"]}

    st.markdown(f"""
        <div class='prayer-grid'>
            <div class='prayer-box'><div class='prayer-name'>Fajr</div><div class='prayer-time'>{timings['Fajr']}</div></div>
            <div class='prayer-box'><div class='prayer-name'>Dhuhr</div><div class='prayer-time'>{timings['Dhuhr']}</div></div>
            <div class='prayer-box'><div class='prayer-name'>Asr</div><div class='prayer-time'>{timings['Asr']}</div></div>
            <div class='prayer-box'><div class='prayer-name'>Maghrib</div><div class='prayer-time'>{timings['Maghrib']}</div></div>
            <div class='prayer-box'><div class='prayer-name'>Isha</div><div class='prayer-time'>{timings['Isha']}</div></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ut_col1, ut_col2 = st.columns(2)

    with ut_col1:
        st.markdown(f"""
            <div class='utility-card'>
                <div style='font-size:1.8rem;'>🧭</div>
                <div style='font-weight:600; color:#A3843B; font-size:1.1rem; margin-top:2px;'>Qibla Orientation</div>
                <h2 style='margin:5px 0 0 0; font-size:1.8rem; font-weight:300;'>292° NW</h2>
                <p style='margin:2px 0 0 0; font-size:0.75rem; color:#8C7A6B;'>Calculated for Klang coordinates</p>
            </div>
        """, unsafe_allow_html=True)

    with ut_col2:
        water_goal = 2000
        progress_percentage = min(st.session_state.water_ml / water_goal, 1.0)

        st.markdown(f"""
            <div class='utility-card' style='padding-bottom:12px;'>
                <div style='font-size:1.8rem;'>💧</div>
                <div style='font-weight:600; color:#A3843B; font-size:1.1rem; margin-top:2px;'>Hydration Tracker</div>
                <h2 style='margin:5px 0 5px 0; font-size:1.8rem; font-weight:300;'>{st.session_state.water_ml} / {water_goal} ml</h2>
            </div>
        """, unsafe_allow_html=True)

        st.progress(progress_percentage)

        w_b1, w_b2 = st.columns(2)

        with w_b1:
            if st.button("➕ Add 250ml", use_container_width=True):
                st.session_state.water_ml += 250
                st.rerun()

        with w_b2:
            if st.button("Clear 🔄", use_container_width=True):
                st.session_state.water_ml = 0
                st.rerun()


# ================= TAB 2: ISLAMIC CALENDAR =================
with tab2:
    st.subheader("📆 Dual Hijri-Gregorian Calendar")

    today_dt = datetime.now()
    target_year = today_dt.year
    target_month = today_dt.month + st.session_state.cal_month_offset

    while target_month > 12:
        target_month -= 12
        target_year += 1

    while target_month < 1:
        target_month += 12
        target_year -= 1

    hijri_months_map = {
        1: "Rajab / Sha'ban",
        2: "Sha'ban / Ramadan",
        3: "Ramadan / Shawwal",
        4: "Shawwal / Dhu al-Qi'dah",
        5: "Dhu al-Qi'dah / Dhu al-Hijjah",
        6: "Dhu al-Hijjah / Muharram",
        7: "Muharram / Safar",
        8: "Safar / Rabi' al-Awwal",
        9: "Rabi' al-Awwal / Rabi' al-Thani",
        10: "Rabi' al-Thani / Jumada al-Ula",
        11: "Jumada al-Ula / Jumada al-Akhirah",
        12: "Jumada al-Akhirah / Rajab"
    }

    nav_col1, nav_col2, nav_col3 = st.columns(3)

    with nav_col1:
        if st.button("◀ Prev Month", use_container_width=True):
            st.session_state.cal_month_offset -= 1
            st.rerun()

    with nav_col2:
        st.markdown(
            f"<div class='calendar-header' style='text-align: center;'>{calendar.month_name[target_month]} {target_year}<br><span style='font-size:0.9rem; color:#8C7A6B;font-weight:400;'>🌙 {hijri_months_map[target_month]}</span></div>",
            unsafe_allow_html=True
        )

    with nav_col3:
        if st.button("Next Month ▶", use_container_width=True):
            st.session_state.cal_month_offset += 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    wd_cols = st.columns(7)

    for idx, day in enumerate(
        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    ):
        wd_cols[idx].markdown(
            f"{day}",
            unsafe_allow_html=True
        )

    cal_matrix = calendar.monthcalendar(
        target_year,
        target_month
    )

    for week in cal_matrix:
        c_cols = st.columns(7)

        for i, day in enumerate(week):

            if day == 0:
                c_cols[i].write("")

            else:

                is_today = (
                    day == today_dt.day
                    and target_month == today_dt.month
                    and target_year == today_dt.year
                )

                box_style = (
                    "day-box-active"
                    if is_today
                    else "day-box"
                )

                approx_hijri_day = (
                    (day + 11) % 30
                    if (day + 11) % 30 != 0
                    else 30
                )

                c_cols[i].markdown(
                    f"""
                    <div class="{box_style}">
                        <div>{day}</div>
                        <div style="font-size:0.75rem;color:#A3843B;">
                            {approx_hijri_day}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ================= TAB 3: INTERACTIVE TASBIH =================

with tab3:

    st.subheader("📿 Digital Tasbih Counter")

    phrase = st.selectbox(
        "Choose Phrase",
        [
            "SubhanAllah",
            "Alhamdulillah",
            "Allahu Akbar",
            "Astaghfirullah"
        ]
    )

    if phrase != st.session_state.tasbih_phrase:
        st.session_state.tasbih_phrase = phrase
        st.session_state.tasbih_count = 0

    st.markdown(
        f"{st.session_state.tasbih_count}{st.session_state.tasbih_phrase}",
        unsafe_allow_html=True
    )

    b1, b2 = st.columns(2)

    with b1:
        if st.button(
            "📿 TAP TO COUNT",
            use_container_width=True
        ):
            st.session_state.tasbih_count += 1
            st.rerun()

    with b2:
        if st.button(
            "🔄 Reset",
            use_container_width=True
        ):
            st.session_state.tasbih_count = 0
            st.rerun()


# ================= TAB 4: GLOBAL FINANCE NEWS =================

with tab4:

    st.subheader(
        "📊 Global Islamic Banking & Market Updates"
    )

    for item in news_data.ITEMS:

        st.markdown(
            f"""
            {item['title']}
            📅 {item['date']}
            {item['desc']}
            """,
            unsafe_allow_html=True
        )


# ================= TAB 5: SHARIAH KNOWLEDGE HUB =================

with tab5:

    st.subheader(
        "💡 Islamic Finance Foundations & Concepts"
    )

    for Concept in news_data.KNOWLEDGE:

        st.markdown(
            f"""
            📌 {Concept['term']}
            {Concept['concept']}
            """,
            unsafe_allow_html=True
        )
