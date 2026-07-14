import streamlit as st
import time
from streamlit_ace import st_ace
from ai_hint import get_hint

import io
import contextlib
# =========================
# セッション初期化
# =========================

if "history" not in st.session_state:
    st.session_state.history = []

if "current_hints" not in st.session_state:
    st.session_state.current_hints = []

if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "mode" not in st.session_state:
    st.session_state.mode = "study"

if "selected_history" not in st.session_state:
    st.session_state.selected_history = None

def run_code(code):
    output = io.StringIO()

    try:
        with contextlib.redirect_stdout(output):
            exec(code)

        return output.getvalue()

    except Exception as e:
        return f"エラー:\n{e}"
st.sidebar.title("📚 メニュー")

if st.sidebar.button("💻 学習画面"):
    st.session_state.mode = "study"
    st.rerun()

if st.sidebar.button("📖 学習履歴"):
    st.session_state.mode = "history"
    st.rerun()

if st.session_state.mode == "history":

    st.title("📖 学習履歴")

    history = load_history()

    if not history:
        st.info("まだ履歴がありません")
        st.stop()

    for i, h in enumerate(history, 1):

        with st.expander(f"{i}. {h['created_at']}"):

            st.write("### 問題")

            st.write(h["problem"])

            st.write(f"⏰ 解答時間：{int(h['solve_time'])} 秒")

            st.write(f"💡 ヒント回数：{h['hint_count']} 回")

            if st.button(
                "詳細を見る",
                key=h["id"]
            ):

                st.session_state.selected_history = h

                st.session_state.mode = "history_detail"

                st.rerun()

    st.stop()
if st.session_state.mode == "history_detail":

    data = st.session_state.selected_history

    st.title("📖 学習履歴")

    st.subheader("問題")

    st.code(data["problem"])

    st.subheader("コード")

    st.code(data["code"])

    st.subheader("AIヒント")

    st.write(data["hint"])

    st.subheader("解答時間")

    st.write(f"{int(data['solve_time'])} 秒")

    if st.button("⬅ 履歴一覧へ戻る"):

        st.session_state.mode = "history"

        st.rerun()

    st.stop()
st.title("Python学習支援システム")

# 問題入力
problem = st.text_area(
    "問題文",
    height=200
)
# 問題を入力したら開始時間を記録
if problem and st.session_state.start_time is None:
    st.session_state.start_time = time.time()
    
st.write("コード")

# コード入力
code = st_ace(
    language="python",
    theme="github",
    height=400,
    key="code_editor"
)
if st.button("コードを実行"):
    result = run_code(code)

    st.subheader("実行結果")
    st.code(result)
# ヒントボタン
with st.form("hint_form"):
    submitted = st.form_submit_button("ヒントをもらう（一度で一回だけ押してください）")

    if submitted:

        hint = get_hint(problem, code)

        st.session_state.current_hints.append(hint)

        st.write(hint)

# =========================
# 停止時間の計測
# =========================

if "last_code" not in st.session_state:
    st.session_state.last_code = ""
    st.session_state.last_time = time.time()

# コードが変わったら時間リセット
if code != st.session_state.last_code:
    st.session_state.last_code = code
    st.session_state.last_time = time.time()

# 停止時間計算
idle_time = time.time() - st.session_state.last_time

st.write(f"停止時間: {int(idle_time)}秒")
# =========================
# 解答時間
# =========================

if st.session_state.start_time is not None:
    solve_time = time.time() - st.session_state.start_time
    st.write(f"解答時間: {int(solve_time)}秒")
# =========================
# 自動ヒント
# =========================

IDLE_LIMIT = 30

if idle_time > IDLE_LIMIT:
    st.warning("悩んでいる？ヒントをあげるよ")

    hint = get_hint(problem, code)
    st.info(hint)

# =========================
# 問題終了
# =========================

if st.button("問題を終了"):

    if st.session_state.start_time is not None:

        solve_time = time.time() - st.session_state.start_time

        st.session_state.history.append(
            {
                "problem": problem,
                "time": solve_time,
                "hints": st.session_state.current_hints.copy()
            }
        )

        st.success("履歴に保存しました！")

        st.session_state.current_hints = []
        st.session_state.start_time = None
