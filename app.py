import streamlit as st
from openai import OpenAI

def run_real_estate_app():
    """
    パスワード制限付きの不動産広告生成アプリ。
    
    Args:
        None: StreamlitのUIから直接取得
    Returns:
        None: 画面に結果を表示
    計算上のエッジケース:
        パスワードが未入力または誤っている場合に、API呼び出しを物理的に遮断する。
    """
    st.set_page_config(page_title="不動産広告AI プレミアム", layout="centered")
    
    # サイドバーにパスワード入力を設置
    with st.sidebar:
        st.title("🔑 認証")
        user_password = st.text_input("パスワードを入力", type="password")
        st.info("※現在はテスト期間中です。パスワード『trial2026』でフル機能が使えます。")
        st.divider()
        st.write("### 💎 有料版の登録")
        st.link_button("無制限プランに加入する", "https://buy.stripe.com/あなたのリンク")

    st.title("🏠 不動産広告自動生成ツール")
    
    # ユーザー入力
    property_details = st.text_area("物件情報を入力してください", height=150)

    if st.button("広告文を生成"):
        # パスワードチェックの論理的帰結
        if user_password != "trial2026":
            st.error("パスワードが正しくありません。")
            return
            
        if not property_details:
            st.warning("情報を入力してください。")
            return

        try:
            # SecretsからAPIキーを取得
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            with st.spinner("AIが最高の一句を考案中..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "あなたは不動産専門のコピーライターです。絵文字を効果的に使い、成約率の高いSNS用広告文を作成してください。"},
                        {"role": "user", "content": property_details}
                    ]
                )
                st.success("生成完了！")
                st.write(response.choices[0].message.content)
                
        except Exception as e:
            st.error(f"エラーが発生しました。管理者にお問い合わせください。")
            

if __name__ == "__main__":
    run_real_estate_app()
