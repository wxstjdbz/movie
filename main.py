```text
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 열 이름의 앞뒤 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜를 실제 날짜로 변환
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

    # 날짜가 제대로 변환된 데이터만 사용
    df = df.dropna(subset=["날짜"])

    return df


# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오지 못했습니다.")
    st.exception(e)
    st.stop()


# ==================================================
# 제목
# ==================================================

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "1년치 일별 박스오피스 10위권 데이터를 이용해 "
    "영화의 시간에 따른 변화를 살펴봅니다."
)


# ==================================================
# 그래프 1. 영화별 일관객 변화
# ==================================================

st.divider()

st.header("그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 선택하면 그 영화의 날짜별 일관객 변화를 볼 수 있습니다."
)


# 영화 목록
movie_list = (
    df["영화명"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

movie_list.sort()


# 영화 선택
selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# 선택한 영화 데이터
movie_df = df[
    df["영화명"].astype(str) == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# 그래프 생성
fig = px.line(
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


# 마우스를 올렸을 때 날짜와 관객 수 표시
fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "일관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)


fig.update_layout(
    hovermode="x",
    xaxis_title="날짜",
    yaxis_title="일관객 수"
)


# 그래프 표시
st.plotly_chart(
    fig,
    use_container_width=True
)


# 설명 문구
st.markdown("### 이 그래프로 알 수 있는 것")

st.write(
    "선택한 영화의 날짜별 일관객 변화와 관객이 증가하거나 감소하는 시점을 알 수 있습니다."
)


# ==================================================
# 그래프 2
# ==================================================

st.divider()

st.header("그래프 2")

st.info("앞으로 추가할 그래프를 위한 공간입니다.")

st.markdown("### 이 그래프로 알 수 있는 것")

st.write("")


# ==================================================
# 그래프 3
# ==================================================

st.divider()

st.header("그래프 3")

st.info("앞으로 추가할 그래프를 위한 공간입니다.")

st.markdown("### 이 그래프로 알 수 있는 것")

st.write("")
```
