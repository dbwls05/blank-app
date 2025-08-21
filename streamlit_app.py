import streamlit as st
import random
import time
import pandas as pd

# 앱의 제목 설정
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# 커스텀 CSS를 사용하여 전체적인 디자인을 개선합니다.
st.markdown("""
<style>
/* Streamlit 기본 스타일 재정의 */
.stApp {
    background-color: #f0f2f6;
    color: #333333;
}

/* 제목 스타일 */
h1 {
    color: #0078d4;
    text-align: center;
    font-size: 2.5em;
    font-weight: bold;
}

/* 버튼 스타일 */
.stButton>button {
    background-color: #ffffff;
    color: #0078d4;
    border: 2px solid #0078d4;
    border-radius: 12px;
    padding: 10px 24px;
    font-size: 1.2em;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease-in-out;
}

.stButton>button:hover {
    background-color: #0078d4;
    color: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

/* 인포 박스 스타일 */
.stAlert {
    border-radius: 10px;
    background-color: #e6f7ff;
    color: #0078d4;
    border: none;
}

/* 성공 메시지 스타일 */
.stSuccess {
    border-radius: 10px;
    background-color: #e9f7ef;
    color: #28a745;
    border: none;
}

/* 입력 필드 스타일 */
.stTextInput>div>div>input {
    border-radius: 8px;
    border: 1px solid #cccccc;
    padding: 8px;
}

/* 랭킹 테이블 스타일 */
.dataframe {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'ready'
    st.session_state.start_time = None
    st.session_state.end_time = None
    st.session_state.delay_time = None
    st.session_state.scores = pd.DataFrame(columns=['이름', '기록(ms)'])

scores_df = st.session_state.scores

# 게임 시작 및 진행 로직
if st.session_state.game_state == 'ready':
    st.info("버튼을 누르면 테스트가 시작됩니다. '클릭하세요!' 메시지가 나타나면 바로 클릭하세요!")
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if st.button("테스트 시작", use_container_width=True):
        st.session_state.game_state = 'waiting'
        st.session_state.delay_time = random.uniform(1.5, 4.0)
        st.rerun()

elif st.session_state.game_state == 'waiting':
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    placeholder = st.empty()
    placeholder.markdown("<h1 style='text-align: center;'>준비...</h1>", unsafe_allow_html=True)
    
    # '테스트 시작' 버튼을 '아직입니다'로 변경
    if st.button("아직입니다", use_container_width=True, disabled=True):
        pass # 비활성화된 버튼이므로 아무 동작도 하지 않음
        
    time.sleep(st.session_state.delay_time)
    
    st.session_state.game_state = 'go'
    st.session_state.start_time = time.time()
    st.rerun()

elif st.session_state.game_state == 'go':
    st.markdown("<br><br>", unsafe_allow_html=True)

    placeholder = st.empty()
    placeholder.markdown("<h1 style='text-align: center; color: green;'>클릭하세요!</h1>", unsafe_allow_html=True)
    
    if st.button("클릭!", use_container_width=True):
        st.session_state.end_time = time.time()
        st.session_state.game_state = 'result'
        st.rerun()

    if st.session_state.start_time is None:
        st.session_state.game_state = 'too_soon'
        st.rerun()

elif st.session_state.game_state == 'too_soon':
    st.error("너무 빨리 클릭했습니다! '클릭하세요!' 메시지가 나타날 때까지 기다려주세요.")
    if st.button("다시 시작", use_container_width=True):
        st.session_state.game_state = 'ready'
        st.rerun()

elif st.session_state.game_state == 'result':
    reaction_time_ms = int((st.session_state.end_time - st.session_state.start_time) * 1000)
    st.success(f"🎉 당신의 반응 속도는 **{reaction_time_ms}ms** 입니다!")

    name = st.text_input("이름을 입력하고 랭킹에 등록하세요.", value="이름을 입력하세요")
    if st.button("랭킹 등록", use_container_width=True) and name and name != "이름을 입력하세요":
        new_score = {'이름': name, '기록(ms)': reaction_time_ms}
        st.session_state.scores = pd.concat([scores_df, pd.DataFrame([new_score])], ignore_index=True)
        st.session_state.scores = st.session_state.scores.sort_values(by='기록(ms)').reset_index(drop=True)
        st.session_state.game_state = 'ready'
        st.rerun()
    
    if st.button("다시 시도", use_container_width=True):
        st.session_state.game_state = 'ready'
        st.rerun()

# 랭킹 표시
st.markdown("---")
st.markdown("## 🏆 랭킹")

if not st.session_state.scores.empty:
    st.dataframe(st.session_state.scores.head(10))
else:
    st.info("아직 랭킹 기록이 없습니다.")
