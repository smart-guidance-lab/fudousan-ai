import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルからAPIキーを読み込む
load_dotenv()

def run_real_estate_app():
    """
    不動産広告生成アプリのメインロジック。
    
    Args:
        None (StreamlitのUI入力を直接利用)
        
    Returns:
        None (画面上に結果を表示)
        
    計算上のエッジケース:
        APIキーが設定されていない場合、エラーメッセージを表示して停止する。
    """
    # APIキーの確認
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("APIキーが設定されていません。.envファイルを確認してください。")
        return

    client = OpenAI(api_key=api_key)

    # UIの設定
    st.title("🏠 不動産広告自動生成ツール")
    st.caption("物件情報を入力するだけで、SNS向けのキャッチコピーを生成します。")

    # 入力フォーム
    property_info = st.text_area("物件概要を貼り付けてください", placeholder="例：港区 3LDK 25万円 駅から徒歩3分...", height=200)

    if st.button("広告文を生成する"):
        if not property_info:
            st.warning("情報を入力してください。")
            return

        try:
            # 中間ログ：API呼び出し開始
            st.info("AIが文章を考えています...")

            response = client.chat.completions.create(
                model="gpt-4o",  # 2026年時点で最も安定した「枯れた最高級」モデル
                messages=[
                    {"role": "system", "content": "あなたはプロの不動産ライターです。入力された情報を元に、Instagramで目を引く絵文字付きの広告文を作成してください。"},
                    {"role": "user", "content": property_info}
                ]
            )

            # 結果の出力
            result = response.choices[0].message.content
            st.success("生成完了！")
            st.subheader("生成された広告文")
            st.write(result)
            st.copy_config = result # コピーしやすいように表示

        except Exception as error:
            st.error(f"エラーが発生しました: {str(error)}")

if __name__ == "__main__":
    run_real_estate_app()
