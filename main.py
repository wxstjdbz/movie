import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 페이지 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# 데이터 주소
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# ============================================================
# 데이터 불러오기
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str).str.strip(),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자 변환
    df["일관객"] = pd.to_numeric(
        df["일관객"],
        errors="coerce"
    )

    # 영화명 정리
    df["영화명"] = df["영화명"].astype(str).str.strip()

    # 날짜가 없는 행 제거
    df = df.dropna(subset=["날짜"])

    return df


# ============================================================
# 데이터 준비
# ============================================================

try:
    df = load_data()

except Exception as e:
    st.error("앗! 데이터를 불러오지 못했어요. 🍿")
    st.exception(e)
    st.stop()


# ============================================================
# 귀여운 설명 박스
# ============================================================

def insight_box(text):
    st.markdown(
        f"""
        <div style="
            background-color: #fff8e7;
            padding: 16px 20px;
            border-radius: 15px;
            border: 1px solid #f3dfaa;
            margin-top: 10px;
            margin-bottom: 20px;
        ">
            <div style="font-size: 16px; font-weight: 700;">
                🍿 이 그래프로 알 수 있는 것
            </div>
            <div style="margin-top: 8px; font-size: 15px;">
                {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 제목
# ============================================================

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.markdown(
    """
    ### 🍿 영화의 시간이 만든 재미있는 변화들

    1년 동안의 박스오피스 데이터를 그래프로 살펴보면서  
    **어떤 영화가 언제 사랑받았는지**, **관객이 언제 많았는지** 찾아봅니다. 🔎
    """
)


# ============================================================
# 그래프 1
# ============================================================

st.divider()

st.header("🎞️ 그래프 1. 영화별 일관객 변화")

st.write(
    "궁금한 영화를 골라서 날짜별 관객 변화를 살펴보세요."
)


movie_list = sorted(
    df["영화명"]
    .dropna()
    .unique()
    .tolist()
)


selected_movie = st.selectbox(
    "🎬 영화를 선택하세요!",
    movie_list
)


movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"🎬 {selected_movie}의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)


fig1.update_traces(
    hovertemplate=(
        "📅 %{x|%Y-%m-%d}"
        "<br>"
        "👥 %{y:,.0f}명"
        "<extra></extra>"
    )
)


fig1.update_layout(
    hovermode="x",
    xaxis_title="날짜",
    yaxis_title="일관객 수"
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


# ------------------------------------------------------------
# 그래프 1 실제 분석
# ------------------------------------------------------------

if not movie_df.empty:

    max_row = movie_df.loc[
        movie_df["일관객"].idxmax()
    ]

    min_row = movie_df.loc[
        movie_df["일관객"].idxmin()
    ]

    max_date = max_row["날짜"].strftime("%Y년 %m월 %d일")
    min_date = min_row["날짜"].strftime("%Y년 %m월 %d일")

    max_audience = max_row["일관객"]
    min_audience = min_row["일관객"]

    insight1 = (
        f"🍿 <b>{selected_movie}</b>은 이 기간 중 "
        f"<b>{max_date}</b>에 가장 많은 관객인 "
        f"<b>{max_audience:,.0f}명</b>을 기록했어요. "
        f"가장 적었던 날은 {min_date}로 {min_audience:,.0f}명이었어요."
    )

else:
    insight1 = "선택한 영화의 데이터를 찾을 수 없어요. 😢"


insight_box(insight1)


# ============================================================
# 그래프 2
# ============================================================

st.divider()

st.header("🏆 그래프 2. 기간 전체 일관객 TOP 5")

st.write(
    "이 기간 동안 누적해서 가장 많은 관객을 모은 영화 5편을 비교합니다."
)


top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
    .tolist()
)


top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)


fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="🏆 기간 전체 일관객 TOP 5",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)


fig2.update_traces(
    hovertemplate=(
        "🎬 %{fullData.name}"
        "<br>"
        "📅 %{x|%Y-%m-%d}"
        "<br>"
        "👥 %{y:,.0f}명"
        "<extra></extra>"
    )
)


fig2.update_layout(
    hovermode="x",
    legend_title="영화",
    legend=dict(
        itemclick="toggle",
        itemdoubleclick="toggleothers"
    )
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# ------------------------------------------------------------
# TOP 5 분석
# ------------------------------------------------------------

top5_summary = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)


top_movie = top5_summary.index[0]
top_movie_audience = top5_summary.iloc[0]

fifth_movie = top5_summary.index[-1]
fifth_movie_audience = top5_summary.iloc[-1]


insight2 = (
    f"🏆 이 기간의 TOP 5 가운데 <b>{top_movie}</b>이 "
    f"<b>{top_movie_audience:,.0f}명</b>으로 가장 많은 일관객 합계를 기록했어요. "
    f"5위인 <b>{fifth_movie}</b>도 {fifth_movie_audience:,.0f}명을 기록했답니다."
)

insight_box(insight2)


# ============================================================
# 그래프 3
# ============================================================

st.divider()

st.header("🌊 그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "매일 박스오피스 10위권 영화의 관객을 모두 더해 전체적인 관객 흐름을 살펴봅니다."
)


daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)


top3_days = daily_total.nlargest(
    3,
    "일관객"
)


fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="🌊 날짜별 박스오피스 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)


fig3.update_traces(
    hovertemplate=(
        "📅 %{x|%Y-%m-%d}"
        "<br>"
        "👥 %{y:,.0f}명"
        "<extra></extra>"
    )
)


for _, row in top3_days.iterrows():

    date_text = row["날짜"].strftime("%m월 %d일")

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=f"⭐ {date_text}",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40
    )


fig3.update_layout(
    hovermode="x",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)


# ------------------------------------------------------------
# TOP 3 분석
# ------------------------------------------------------------

top_day = top3_days.iloc[0]

top_day_date = top_day["날짜"].strftime("%Y년 %m월 %d일")
top_day_audience = top_day["일관객"]


insight3 = (
    f"🌟 10위권 전체 관객이 가장 많았던 날은 "
    f"<b>{top_day_date}</b>로, 무려 <b>{top_day_audience:,.0f}명</b>이었어요! "
    f"TOP 3 중에서도 이날의 관객 규모가 가장 컸습니다."
)

insight_box(insight3)


# ============================================================
# 그래프 4
# ============================================================

st.divider()

st.header("📊 그래프 4. 영화별 기간 전체 일관객 TOP 10")

st.write(
    "영화별 일관객 합계를 비교하고, 각 영화가 10위권에 등장한 날수도 함께 살펴봅니다."
)


movie_stats = (
    df.dropna(subset=["영화명"])
    .groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        일수=("날짜", "nunique")
    )
    .reset_index()
)


top10_df = (
    movie_stats
    .nlargest(10, "일관객합계")
    .sort_values("일관객합계", ascending=True)
)


fig4 = px.bar(
    top10_df,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="📊 영화별 기간 전체 일관객 TOP 10",
    labels={
        "일관객합계": "기간 전체 일관객",
        "영화명": "영화"
    }
)


fig4.update_traces(
    customdata=top10_df[["일수"]].to_numpy(),
    hovertemplate=(
        "🎬 %{y}"
        "<br>"
        "👥 기간 전체 일관객: %{x:,.0f}명"
        "<br>"
        "📅 10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)


fig4.update_layout(
    xaxis_title="기간 전체 일관객",
    yaxis_title="영화"
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


# ------------------------------------------------------------
# TOP 10 분석
# ------------------------------------------------------------

top10_best = top10_df.iloc[-1]

best_movie = top10_best["영화명"]
best_audience = top10_best["일관객합계"]
best_days = int(top10_best["일수"])


insight4 = (
    f"🥇 TOP 10 가운데 <b>{best_movie}</b>이 "
    f"<b>{best_audience:,.0f}명</b>으로 가장 많은 관객을 기록했어요. "
    f"이 영화는 관측 기간 동안 <b>{best_days}일</b>이나 10위권에 등장했답니다."
)

insight_box(insight4)


# ============================================================
# 그래프 5
# ============================================================

st.divider()

st.header("🗓️ 그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "어느 달의 어느 요일에 영화관 관객이 많았는지 색으로 살펴봅니다."
)


# 월 추출
heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month


# 요일 추출
weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일"] = heatmap_df["날짜"].dt.dayofweek.map(
    lambda x: weekday_names[x]
)


# 월 × 요일별 합계
heatmap_data = (
    heatmap_df
    .groupby(
        ["월", "요일"],
        as_index=False
    )["일관객"]
    .sum()
)


# 표로 변환
heatmap_table = heatmap_data.pivot(
    index="월",
    columns="요일",
    values="일관객"
)


# 순서 고정
heatmap_table = heatmap_table.reindex(
    columns=weekday_names
)

heatmap_table = heatmap_table.reindex(
    index=range(1, 13)
)


# 히트맵
fig5 = px.imshow(
    heatmap_table,
    x=weekday_names,
    y=[f"{month}월" for month in range(1, 13)],
    text_auto=".2s",
    aspect="auto",
    title="🗓️ 월 × 요일별 박스오피스 10위권 일관객 합계",
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    }
)


fig5.update_traces(
    hovertemplate=(
        "%{y} %{x}"
        "<br>"
        "👥 일관객 합계: %{z:,.0f}명"
        "<extra></extra>"
    )
)


fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월"
)


st.plotly_chart(
    fig5,
    use_container_width=True
)


# ------------------------------------------------------------
# 히트맵 실제 분석
# ------------------------------------------------------------

# 가장 큰 월 × 요일 조합
max_cell = heatmap_table.stack().idxmax()

max_month = max_cell[0]
max_weekday = max_cell[1]
max_cell_value = heatmap_table.loc[
    max_month,
    max_weekday
]


# 가장 작은 월 × 요일 조합
min_cell = heatmap_table.stack().idxmin()

min_month = min_cell[0]
min_weekday = min_cell[1]
min_cell_value = heatmap_table.loc[
    min_month,
    min_weekday
]


insight5 = (
    f"🔥 가장 관객이 많았던 조합은 "
    f"<b>{max_month}월 {max_weekday}</b>로 "
    f"<b>{max_cell_value:,.0f}명</b>이었어요. "
    f"반대로 가장 적었던 조합은 "
    f"<b>{min_month}월 {min_weekday}</b>로 "
    f"{min_cell_value:,.0f}명이었어요."
)

insight_box(insight5)
