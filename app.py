import streamlit as st
import requests
import calendar
import random
import re
from datetime import datetime, date
from praytimes import PrayTimes
import news_data


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="The Reflection Portal",
    page_icon="🕌",
    layout="centered"
)


# ============================================================
# INITIALIZE SESSION STATES
# ============================================================

if "tasbih_count" not in st.session_state:
    st.session_state.tasbih_count = 0

if "tasbih_phrase" not in st.session_state:
    st.session_state.tasbih_phrase = "SubhanAllah"

if "cal_month_offset" not in st.session_state:
    st.session_state.cal_month_offset = 0

if "water_ml" not in st.session_state:
    st.session_state.water_ml = 0

if "current_hadith_idx" not in st.session_state:
    st.session_state.current_hadith_idx = datetime.now().day


# ============================================================
# HELPER FUNCTION
# ============================================================

def clean_news_text(text):
    """
    Remove accidental Markdown code formatting/backticks
    so news text uses the same standard font.
    """
    if text is None:
        return ""

    text = str(text)

    # Remove Markdown backticks
    text = text.replace("`", "")

    # Remove excessive Markdown emphasis markers
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)

    return text.strip()


# ============================================================
# MODERNIZED THEME STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL APPLICATION
       ======================================================== */

    .stApp {
        background-color: #FDFBF7 !important;
        color: #2C2520 !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }

    html,
    body,
    [class*="css"] {
        font-family: Arial, Helvetica, sans-serif !important;
    }


    /* ========================================================
       GILDED FRAME CARD
       ======================================================== */

    .islamic-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        border-top: 5px solid #D4AF37;
        box-shadow: 0 4px 20px rgba(212, 175, 55, 0.08);
        margin-bottom: 25px;
    }

    .hadith-text {
        font-size: 1.2rem;
        font-style: italic;
        color: #4A3E3D;
        line-height: 1.6;
        text-align: center;
        margin-bottom: 12px;
        padding: 0 20px;
    }

    .hadith-source {
        font-size: 0.85rem;
        color: #8C7A6B;
        text-align: center;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
    }


    /* ========================================================
       PRAYER GRID
       ======================================================== */

    .prayer-grid {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 25px;
    }

    .prayer-box {
        background: #FFFFFF;
        border: 1px solid #EADCC9;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        flex: 1;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.01);
    }

    .prayer-name {
        font-size: 0.85rem;
        color: #8C7A6B;
        font-weight: 500;
        text-transform: uppercase;
    }

    .prayer-time {
        font-size: 1.25rem;
        color: #A3843B;
        font-weight: 700;
        margin-top: 4px;
    }


    /* ========================================================
       UTILITY CARDS
       ======================================================== */

    .utility-card {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #EADCC9;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.01);
    }


    /* ========================================================
       CALENDAR
       ======================================================== */

    .calendar-header {
        text-align: center;
        font-size: 1.25rem;
        font-weight: 600;
        color: #A3843B;
        margin-top: 5px;
        line-height: 1.4;
    }

    .day-box {
        background-color: #FFFFFF;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #EADCC9;
        margin: 2px;
    }

    .day-box-active {
        background-color: #F7F3EB;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #D4AF37;
        margin: 2px;
        font-weight: bold;
    }


    /* ========================================================
       NEWS CARDS
       ======================================================== */

    .news-card {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 4px solid #D4AF37;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.01);

        /* Standard font */
        font-family: Arial, Helvetica, sans-serif !important;
        color: #2C2520 !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .news-card * {
        font-family: Arial, Helvetica, sans-serif !important;
    }

    .news-card code,
    .news-card pre {
        font-family: Arial, Helvetica, sans-serif !important;
        background: transparent !important;
        color: #2C2520 !important;
        padding: 0 !important;
        border: none !important;
        border-radius: 0 !important;
        font-size: inherit !important;
        font-weight: inherit !important;
    }

    .news-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #A3843B !important;
        margin-bottom: 5px;
        font-family: Arial, Helvetica, sans-serif !important;
    }

    .news-date {
        font-size: 0.85rem;
        color: #8C7A6B !important;
        margin-bottom: 8px;
        font-family: Arial, Helvetica, sans-serif !important;
    }

    .news-description {
        font-size: 0.95rem;
        color: #2C2520 !important;
        line-height: 1.6;
        font-family: Arial, Helvetica, sans-serif !important;
    }


    /* ========================================================
       KNOWLEDGE CARDS
       ======================================================== */

    .knowledge-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #EADCC9;
        margin-bottom: 15px;
        font-family: Arial, Helvetica, sans-serif !important;
    }

    .knowledge-card * {
        font-family: Arial, Helvetica, sans-serif !important;
    }

    .knowledge-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #2C2520 !important;
        border-bottom: 2px solid #F7F3EB;
        padding-bottom: 6px;
        margin-bottom: 8px;
    }


    /* ========================================================
       GENERAL TEXT
       ======================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    p,
    span,
    label,
    div {
        font-family: Arial, Helvetica, sans-serif;
    }

    h1,
    h2,
    h3,
    p,
    span,
    label {
        color: #2C2520 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #A3843B !important;
        border: 1px solid #EADCC9 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-family: Arial, Helvetica, sans-serif !important;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #F7F3EB !important;
        border-color: #D4AF37 !important;
        color: #2C2520 !important;
    }


    /* ========================================================
       STREAMLIT UI
       ======================================================== */

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BRANDING HEADER
# ============================================================

st.markdown(
    """
    <h1 style="
        text-align: center;
        color: #A3843B !important;
        font-weight: 300;
    ">
        🕌 THE REFLECTION PORTAL
    </h1>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LIVE HIJRI DATE AND PRAYER TIME FETCHING
# ============================================================

hijri_display_str = "8 Rabi' al-Thani 1448 AH"

lat, lon = 3.0333, 101.4500

timings = {}


try:
    url = "https://aladhan.com"

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=3
    ).json()

    if response["code"] == 200:
        timings = response["data"]["timings"]

        h_data = response["data"]["date"]["hijri"]

        hijri_display_str = (
            f"{h_data['day']} "
            f"{h_data['month']['en']} "
            f"{h_data['year']} AH"
        )

except Exception:
    pass


# ============================================================
# HEADER INFORMATION
# ============================================================

st.markdown(
    f"""
    <p style="
        text-align: center;
        color: #8C7A6B !important;
        font-size: 1.1rem;
        margin-top: -10px;
    ">
        🌙 {hijri_display_str} | Klang, Selangor
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        text-align: center;
        color: #D4AF37;
        margin-bottom: 25px;
    ">
        ✦ ═══ 🕌 ═══ ✦
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# NAVIGATION TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "✨ Prayer & Utilities",
        "📅 Islamic Calendar",
        "📿 Interactive Tasbih",
        "📈 Global Finance News",
        "📖 Shariah Knowledge"
    ]
)


# ============================================================
# TAB 1: PRAYER & UTILITIES
# ============================================================

with tab1:

    hadiths = [
        {
            "text": "The best among you are those who have the best manners and character.",
            "source": "Sahih al-Bukhari"
        },
        {
            "text": "Cleanliness is half of faith.",
            "source": "Sahih Muslim"
        },
        {
            "text": "A Muslim is the one from whose tongue and hands the Muslims are safe.",
            "source": "Sahih al-Bukhari"
        },
        {
            "text": "Make things easy for people and do not make them difficult.",
            "source": "Sahih al-Bukhari"
        }
    ]

    selected_hadith = hadiths[
        st.session_state.current_hadith_idx % len(hadiths)
    ]

    st.markdown(
        f"""
        <div class="islamic-card">

            <div class="hadith-text">
                “{selected_hadith['text']}”
            </div>

            <div class="hadith-source">
                — {selected_hadith['source']}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    h_col1, h_col2, h_col3 = st.columns(3)

    with h_col2:

        if st.button(
            "🔄 Shuffle Hadith",
            use_container_width=True
        ):
            st.session_state.current_hadith_idx = random.randint(0, 100)
            st.rerun()


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    st.subheader("🕒 Daily Prayer Windows")


    if not timings:

        PT = PrayTimes("Egypt")

        times = PT.getTimes(
            datetime.now().date(),
            (lat, lon),
            8
        )

        timings = {
            "Fajr": times["fajr"],
            "Dhuhr": times["dhuhr"],
            "Asr": times["asr"],
            "Maghrib": times["maghrib"],
            "Isha": times["isha"]
        }


    st.markdown(
        f"""
        <div class="prayer-grid">

            <div class="prayer-box">
                <div class="prayer-name">Fajr</div>
                <div class="prayer-time">
                    {timings["Fajr"]}
                </div>
            </div>

            <div class="prayer-box">
                <div class="prayer-name">Dhuhr</div>
                <div class="prayer-time">
                    {timings["Dhuhr"]}
                </div>
            </div>

            <div class="prayer-box">
                <div class="prayer-name">Asr</div>
                <div class="prayer-time">
                    {timings["Asr"]}
                </div>
            </div>

            <div class="prayer-box">
                <div class="prayer-name">Maghrib</div>
                <div class="prayer-time">
                    {timings["Maghrib"]}
                </div>
            </div>

            <div class="prayer-box">
                <div class="prayer-name">Isha</div>
                <div class="prayer-time">
                    {timings["Isha"]}
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # QIBLA
    # --------------------------------------------------------

    ut_col1, ut_col2 = st.columns(2)

    with ut_col1:

        st.markdown(
            """
            <div class="utility-card">

                <div style="font-size:1.8rem;">
                    🧭
                </div>

                <div style="
                    font-weight:600;
                    color:#A3843B;
                    font-size:1.1rem;
                    margin-top:2px;
                ">
                    Qibla Orientation
                </div>

                <h2 style="
                    margin:5px 0 0 0;
                    font-size:1.8rem;
                    font-weight:300;
                ">
                    292° NW
                </h2>

                <p style="
                    margin:2px 0 0 0;
                    font-size:0.75rem;
                    color:#8C7A6B;
                ">
                    Calculated for Klang coordinates
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # HYDRATION TRACKER
    # --------------------------------------------------------

    with ut_col2:

        water_goal = 2000

        progress_percentage = min(
            st.session_state.water_ml / water_goal,
            1.0
        )

        st.markdown(
            f"""
            <div class="utility-card">

                <div style="font-size:1.8rem;">
                    💧
                </div>

                <div style="
                    font-weight:600;
                    color:#A3843B;
                    font-size:1.1rem;
                    margin-top:2px;
                ">
                    Hydration Tracker
                </div>

                <h2 style="
                    margin:5px 0 5px 0;
                    font-size:1.8rem;
                    font-weight:300;
                ">
                    {st.session_state.water_ml} / {water_goal} ml
                </h2>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.progress(progress_percentage)


        w_b1, w_b2 = st.columns(2)


        with w_b1:

            if st.button(
                "➕ Add 250ml",
                use_container_width=True
            ):
                st.session_state.water_ml += 250
                st.rerun()


        with w_b2:

            if st.button(
                "Clear 🔄",
                use_container_width=True
            ):
                st.session_state.water_ml = 0
                st.rerun()


# ============================================================
# TAB 2: ISLAMIC CALENDAR
# ============================================================

with tab2:

    st.subheader("📆 Dual Hijri-Gregorian Calendar")


    today_dt = datetime.now()

    target_year = today_dt.year

    target_month = (
        today_dt.month +
        st.session_state.cal_month_offset
    )


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

        if st.button(
            "◀ Prev Month",
            use_container_width=True
        ):

            st.session_state.cal_month_offset -= 1
            st.rerun()


    with nav_col2:

        st.markdown(
            f"""
            <div class="calendar-header">

                {calendar.month_name[target_month]}
                {target_year}

                <br>

                <span style="
                    font-size:0.9rem;
                    color:#8C7A6B;
                    font-weight:400;
                ">
                    🌙 {hijri_months_map[target_month]}
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )


    with nav_col3:

        if st.button(
            "Next Month ▶",
            use_container_width=True
        ):

            st.session_state.cal_month_offset += 1
            st.rerun()


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # WEEKDAY HEADERS
    # --------------------------------------------------------

    wd_cols = st.columns(7)

    weekdays = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
    ]


    for idx, day_name in enumerate(weekdays):

        wd_cols[idx].markdown(
            f"""
            <div style="
                text-align:center;
                font-weight:600;
                color:#A3843B;
            ">
                {day_name}
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # CALENDAR
    # --------------------------------------------------------

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

                        <div style="
                            font-size:1.05rem;
                            font-weight:600;
                        ">
                            {day}
                        </div>

                        <div style="
                            font-size:0.75rem;
                            color:#8C7A6B;
                            margin-top:4px;
                        ">
                            🌙 {approx_hijri_day}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# TAB 3: INTERACTIVE TASBIH
# ============================================================

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
        f"""
        <div class="utility-card">

            <div style="
                font-size:4rem;
                font-weight:300;
                color:#A3843B;
            ">
                {st.session_state.tasbih_count}
            </div>

            <div style="
                font-size:1.2rem;
                color:#8C7A6B;
            ">
                {st.session_state.tasbih_phrase}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "<br>",
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


# ============================================================
# TAB 4: GLOBAL FINANCE NEWS
# ============================================================

with tab4:

    st.subheader(
        "📊 Global Islamic Banking & Market Updates"
    )


    for item in news_data.ITEMS:

        title = clean_news_text(
            item.get("title", "")
        )

        news_date = clean_news_text(
            item.get("date", "")
        )

        description = clean_news_text(
            item.get("desc", "")
        )


        st.markdown(
            f"""
            <div class="news-card">

                <div class="news-title">
                    {title}
                </div>

                <div class="news-date">
                    📅 {news_date}
                </div>

                <div class="news-description">
                    {description}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# TAB 5: SHARIAH KNOWLEDGE HUB
# ============================================================

with tab5:

    st.subheader(
        "💡 Islamic Finance Foundations & Concepts"
    )


    for concept in news_data.KNOWLEDGE:

        term = clean_news_text(
            concept.get("term", "")
        )

        explanation = clean_news_text(
            concept.get("concept", "")
        )


        st.markdown(
            f"""
            <div class="knowledge-card">

                <div class="knowledge-title">
                    📌 {term}
                </div>

                <div style="
                    color:#2C2520;
                    line-height:1.6;
                ">
                    {explanation}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )
