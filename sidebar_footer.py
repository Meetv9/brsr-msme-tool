"""
Shared sidebar footer for Ecosetu.
Import and call render_sidebar_footer() at the top of every page.
"""
import streamlit as st


def render_sidebar_footer():
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align:center; padding: 4px 0;'>
                <a href='https://forms.gle/ZAvGwN25sCPT3gU3A' target='_blank'
                   style='display:inline-block; padding:8px 14px;
                          background:#0F4C2C; color:white;
                          border-radius:8px; text-decoration:none;
                          font-size:13px; font-weight:600;'>
                    🌱 Join the Founding 100
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style='font-size:11.5px; color:#666; text-align:center;
                        line-height:1.6; padding: 10px 4px 4px;'>
                Built by <b style='color:#0F4C2C;'>Meet Vaghani</b><br>
                Certified ESG Professional<br><br>
                <a href='mailto:meet.vaghani9909@gmail.com'
                   style='color:#666; text-decoration:none;'>
                   meet.vaghani9909@gmail.com
                </a><br>
                <a href='https://ecosetu.co.in'
                   style='color:#0F4C2C; text-decoration:none; font-weight:600;'>
                   ecosetu.co.in
                </a>
            </div>
            <div style='font-size:10.5px; color:#999; text-align:center;
                        margin-top:14px; padding-top:8px;
                        border-top:1px solid #eee;'>
                Made in India 🇮🇳<br>
                An initiative by Keprin Overseas Corporation<br>
                © 2026 Ecosetu
            </div>
            """,
            unsafe_allow_html=True,
        )