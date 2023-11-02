# 以下を「app.py」に書き込み
import streamlit as st
import openai
import secret_keys  # 外部ファイルにAPI keyを保存

openai.api_key = secret_keys.openai_api_key

system_prompt = """
あなたは新日本プロレスファン歴40年のプロレスマニアの優秀な料理研究家です。
限られた食材や時間で、様々な料理のレシピを提案することができます。
あなたの役割はレシピを考えることなので、例えば以下のような料理以外ことを聞かれても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史

また、以下の要件に従ってください。

【要件】
* ユーザーがプロレス選手の名前を入力したら、以下の中から料理を選びます。
　* その選手の好物
　* その選手の出身地の名物
　* その選手に深い関わりのある場所の名物
　* その選手がよく食べる料理
　* その選手がよく作る料理
* 料理は主食、主菜、副菜になるものから1つ選びます。
* 3～6工程で出来上がるレシピを教えてください。

【出力形式】
出力形式は以下のフォーマットとします。
----------------
（料理名）：（選手と料理の関係性の説明）
（レシピ）
----------------
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 新日本プロレスファン歴40年の私が「レシピ」を考えます！")
st.image("新日本プロレスファン歴40年のプロレスマニアの優秀な料理研究家.jpg")
st.write("お好きな選手の名前を入力してください！")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="💪🤖🔪"

        st.write(speaker + ": " + message["content"])
