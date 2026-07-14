import streamlit as st

st.title("📚 学習履歴")

history = st.session_state.get("history", [])

if not history:
    st.info("まだ履歴はありません。")
else:
    for i, data in enumerate(history):
        st.subheader(f"問題 {i+1}")

        st.write("### 問題")
        st.write(data["problem"])

        st.write("### 解答時間")
        st.write(f"{int(data['time'])} 秒")

        st.write("### AIヒント")
        for hint in data["hints"]:
            st.info(hint)

        st.divider()
