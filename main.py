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

    # 열 이름 앞뒤 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜를 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str).str.strip(),
        format="%Y%m%d",
        errors="coerce"
    )

    # 일관객을 숫자로 변환
    df["일관객"] = pd.to_numeric(
        df["일관객"],
        errors="coerce"
    )

    # 날짜가 정상적으로 변환된 행만 사용
    df = df.dropna(subset=["날짜"])

    return df


# ============================================================
# 데이터 준비
# ============================================================

try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오지 못했습니다.")
    st.exception(e)
    st.stop()


# ============================================================
# 제목
# ============================================================

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "1년치 일별 박스오피스 10위권 데이터를 이용해 "
    "영화의 시간에 따른 변화를 살펴봅니다."
)


# ============================================================
# 그래프 1
# 영화별 일관객 변화
# ============================================================

st.divider()

st.header("그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 선택하면 그 영화의 날짜별 일관객 변화를 볼 수 있습니다."
)


movie_list = (
    df["영화명"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

movie_list.sort()


selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


movie_df = df[
    df["영화명"].astype(str) == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)


fig1.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "일관객: %{y:,.0f}명"
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


st.markdown("### 이 그래프로 알 수 있는 것")

st.write(
    "선택한 영화의 날짜별 일관객 변화와 관객이 증가하거나 감소하는 시점을 알 수 있습니다."
)


# ============================================================
# 그래프 2
# 기간 전체 일관객 합계 TOP 5
# ============================================================

st.divider()

st.header("그래프 2. 기간 전체 일관객 TOP 5")

st.write(
    "이 기간 동안 일관객의 합계가 가장 큰 5편의 날짜별 일관객 변화를 비교합니다."
)


top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)["영화명"]
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
    markers=False,
    title="기간 전체 일관객 합계 TOP 5 영화의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)


fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>"
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "일관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)


fig2.update_layout(
    hovermode="x",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
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


st.markdown("**기간 전체 일관객 합계 TOP 5**")

for i, movie in enumerate(top5_movies, start=1):

    total_audience = top5_df.loc[
        top5_df["영화명"] == movie,
        "일관객"
    ].sum()

    st.write(
        f"{i}. {movie} — {total_audience:,.0f}명"
    )


st.markdown("### 이 그래프로 알 수 있는 것")

st.write(
    "기간 전체 일관객 합계가 가장 큰 5편이 날짜에 따라 어떤 관객 변화를 보였는지 비교할 수 있습니다."
)


# ============================================================
# 그래프 3
# 날짜별 10위권 일관객 합계
# ============================================================

st.divider()

st.header("그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "매일 박스오피스 10위권 영화의 일관객을 모두 더해 "
    "그날 영화관을 찾은 관객 규모의 변화를 살펴봅니다."
)


daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)


top3_days = (
    daily_total
    .sort_values("일관객", ascending=False)
    .head(3)
    .sort_values("날짜")
)


fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)


fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "10위권 일관객 합계: %{y:,.0f}명"
        "<extra></extra>"
    )
)


for _, row in top3_days.iterrows():

    date_text = row["날짜"].strftime("%Y-%m-%d")
    audience = row["일관객"]

    fig3.add_annotation(
        x=row["날짜"],
        y=audience,
        text=f"★ {date_text}<br>{audience:,.0f}명",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-55
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


st.markdown("**10위권 일관객 합계가 가장 컸던 날 TOP 3**")

for i, (_, row) in enumerate(
    top3_days.sort_values("일관객", ascending=False).iterrows(),
    start=1
):

    date_text = row["날짜"].strftime("%Y-%m-%d")
    audience = row["일관객"]

    st.write(
        f"{i}. {date_text} — {audience:,.0f}명"
    )


st.markdown("### 이 그래프로 알 수 있는 것")

st.write(
    "날짜별 박스오피스 10위권의 전체 관객 규모와 관객이 특히 많았던 날을 한눈에 알 수 있습니다."
)


# ============================================================
# 그래프 4
# 영화별 기간 전체 일관객 TOP 10
# ============================================================

st.divider()

st.header("그래프 4. 영화별 기간 전체 일관객 TOP 10")

st.write(
    "영화별로 이 기간의 일관객을 모두 더해 가장 많은 영화 10편을 비교합니다."
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
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .copy()
)


# 그래프에서 관객이 많은 영화가 위에 오도록
top10_df = top10_df.sort_values(
    "일관객합계",
    ascending=True
)


fig4 = px.bar(
    top10_df,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="영화별 기간 전체 일관객 TOP 10",
    labels={
        "일관객합계": "기간 전체 일관객",
        "영화명": "영화"
    }
)


fig4.update_traces(
    customdata=top10_df[["일수"]].to_numpy(),
    hovertemplate=(
        "영화: %{y}"
        "<br>"
        "기간 전체 일관객: %{x:,.0f}명"
        "<br>"
        "10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)


fig4.update_layout(
    xaxis_title="기간 전체 일관객",
    yaxis_title="영화",
    yaxis={
        "categoryorder": "total ascending"
    }
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


st.markdown("### 이 그래프로 알 수 있는 것")

st.write(
    "이 기간 동안 일관객이 가장 많았던 영화 10편과 각 영화가 10위권에 든 날수를 비교할 수 있습니다."
)


# ============================================================
# 그래프 5
# 월 × 요일별 일관객 합계 히트맵
# ============================================================

st.divider()

st.header("그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "날짜에서 월과 요일을 뽑아 월요일부터 일요일까지의 "
    "요일별 관객 규모를 월별로 비교합니다."
)


# ------------------------------------------------------------
# 월과 요일 추출
# ------------------------------------------------------------

heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month

weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일"] = heatmap_df["날짜"].dt.dayofweek.map(
    dict(enumerate(weekday_order))
)


# ------------------------------------------------------------
# 월 × 요일별 일관객 합계
# ------------------------------------------------------------

heatmap_data = (
    heatmap_df
    .groupby(["월", "요일"], as_index=False)["일관객"]
    .sum()
)


# ------------------------------------------------------------
# 모든 월 × 요일 조합을 만들고 없는 값은 0으로 처리
# ------------------------------------------------------------

all_months = list(range(1, 13))

all_combinations = pd.MultiIndex.from_product(
    [all_months, weekday_order],
    names=["월", "요일"]
).to_frame(index=False)


heatmap_data = all_combinations.merge(
    heatmap_data,
    on=["월", "요일"],
    how="left"
)

heatmap_data["일관객"] = heatmap_data["일관객"].fillna(0)


# ------------------------------------------------------------
# 히트맵
# ------------------------------------------------------------

fig5 = px.density_heatmap(
    heatmap_data,
    x="요일",
    y="월",
    z="일관객",
    category_orders={
        "요일": weekday_order,
        "월": all_months
    },
    text_auto=".2s",
    title="월 × 요일별 박스오피스 10위권 일관객 합계",
    labels={
        "요일": "요일",
        "월": "월",
        "일관객": "일관객 합계"
    }
)


# ------------------------------------------------------------
# 마우스를 올렸을 때 표시
# ------------------------------------------------------------

fig5.update_traces(
    hovertemplate=(
        "%{y}월 %{x}"
        "<br>"
        "10위권 일관객 합계: %{z:,.0f}명"
        "<extra></extra>"
    )
)


# ------------------------------------------------------------
# 월 / 요일 순서 및 그래프 설정
# ------------------------------------------------------------

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    coloraxis_colorbar_title="일관객"
)


st.plotly_chart(
    fig5,
    use_container_width=True
)


# ------------------------------------------------------------
# 설명
# ------------------------------------------------------------

st.markdown("### 이 그래프로 알 수 있는 것")

st.write(
    "어느 달의 어떤 요일에 박스오피스 10위권 전체의 일관객이 많았는지 한눈에 비교할 수 있습니다."
)


# ============================================================
# 그래프 6
# 앞으로 추가할 공간
# ============================================================

st.divider()

st.header("그래프 6")

st.info(
    "앞으로 추가할 그래프를 위한 공간입니다."
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.write("")
