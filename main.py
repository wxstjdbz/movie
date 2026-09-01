```python
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 페이지 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)


# ============================================================
# 데이터 주소
# ============================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/"
    "data/kobis_daily.csv"
)


# ============================================================
# 데이터 불러오기
# ============================================================

@st.cache_data
def load_data():
    # CSV 불러오기
    data = pd.read_csv(DATA_URL)

    # 열 이름 앞뒤의 불필요한 공백 제거
    data.columns = data.columns.str.strip()

    # 날짜를 실제 날짜 데이터로 변환
    data["날짜"] = pd.to_datetime(
        data["날짜"].astype(str).str.strip(),
        format="%Y%m%d",
        errors="coerce",
    )

    # 숫자로 사용해야 하는 열을 숫자로 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수",
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce",
            )

    # 날짜가 변환되지 않은 행 제거
    data = data.dropna(subset=["날짜"])

    return data


# ============================================================
# 데이터 준비
# ============================================================

try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
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
# 데이터 확인
# ============================================================

with st.expander("데이터 확인하기"):
    st.write(f"전체 데이터 행 수: {len(df):,}")
    st.dataframe(df.head(20), use_container_width=True)


# ============================================================
# 그래프 1
# 영화별 날짜에 따른 일관객 변화
# ============================================================

st.divider()

st.header("그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 변화를 볼 수 있습니다."
)


# 영화 목록 만들기
movie_list = (
    df["영화명"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

movie_list = sorted(movie_list)


# 영화 선택
selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)


# 선택한 영화의 데이터만 가져오기
movie_df = df[
    df["영화명"].astype(str) == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# 그래프 만들기
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
)


# 마우스를 올렸을 때 표시되는 내용
fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>"
        "일관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)


# 그래프 모양 설정
fig.update_layout(
    hovermode="x",
    xaxis_title="날짜",
    yaxis_title="일관객",
)


# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True,
)


# 그래프 설명 영역
st.markdown("### 이 그래프로 알 수 있는 것")

st.write(
    "선택한 영화의 날짜별 일관객이 언제 많고 적었는지와 "
    "시간에 따른 관객 변화 추이를 알 수 있습니다."
)


# ============================================================
# 그래프 2
# 앞으로 추가할 공간
# ============================================================

st.divider()

st.header("그래프 2")

st.info(
    "앞으로 새로운 그래프를 이 구역에 추가할 수 있습니다."
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.write(
    "여기에 그래프를 통해 알 수 있는 내용을 한 문장으로 적습니다."
)


# ============================================================
# 그래프 3
# 앞으로 추가할 공간
# ============================================================

st.divider()

st.header("그래프 3")

st.info(
    "앞으로 새로운 그래프를 이 구역에 추가할 수 있습니다."
)

st.markdown("### 이 그래프로 알 수 있는 것")

st.write(
    "여기에 그래프를 통해 알 수 있는 내용을 한 문장으로 적습니다."
)
```
