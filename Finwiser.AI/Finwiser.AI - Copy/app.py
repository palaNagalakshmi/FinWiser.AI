import streamlit as st
import requests

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="FINWISER.AI – SEC Filing Q&A",
    page_icon="📊",
    layout="wide"
)

API_URL = "http://localhost:8000/ask"

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("## 📊 FINWISER.AI")
    st.caption("SEC Filing Intelligence")
    st.divider()

    st.markdown(
        """
        **What this does**
        - Query SEC 10-K / 10-Q filings  
        - Grounded answers only  
        - Transparent source citations  

        **Tech Stack**
        - FastAPI  
        - Pinecone  
        - Sentence Transformers  
        - OpenAI (LLM)  
        """
    )

    st.divider()
    st.caption("Hackathon Track: F7 – SEC Filing Summarizer & Q&A")

# -------------------------------------------------
# Main Header
# -------------------------------------------------
st.markdown(
    """
    <h1 style='text-align: center;'>📊 FINWISER.AI</h1>
    <p style='text-align: center; font-size:18px;'>
        Ask investor-focused questions over SEC filings<br>
        <span style='color:gray;'>Answers are grounded with citations</span>
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# Question Input
# -------------------------------------------------
col1, col2 = st.columns([4, 1])

with col1:
    question = st.text_input(
        "Ask a question",
        placeholder="What does the Outside Directors Stock Based Compensation Plan provide?",
        label_visibility="collapsed"
    )

with col2:
    ask_button = st.button("🔍 Ask", use_container_width=True)

# -------------------------------------------------
# Result Section
# -------------------------------------------------
if ask_button and question.strip():
    with st.spinner("🔎 Analyzing SEC filings..."):
        try:
            response = requests.post(
                API_URL,
                json={"question": question},
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()

                # -----------------------------
                # Answer Card
                # -----------------------------
                st.markdown("### ✅ Answer")
                st.markdown(
                    f"""
                    <div style="
                        background-color:#0e1117;
                        padding:20px;
                        border-radius:10px;
                        border:1px solid #2b2f38;
                        font-size:16px;
                        line-height:1.6;
                         color: #ffffff;
                    ">
                        {data.get("answer", "No answer returned.")}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # -----------------------------
                # Sources
                # -----------------------------
                sources = data.get("sources", [])

                if sources:
                    st.markdown("### 🔗 Source Citations")
                    cols = st.columns(min(len(sources), 4))

                    for i, src in enumerate(sources):
                        with cols[i % len(cols)]:
                            st.markdown(
                                f"""
                                <div style="
                                    background-color:#1f2933;
                                    padding:10px;
                                    border-radius:8px;
                                    text-align:center;
                                    font-size:13px;
                                    color: #ffffff;
                                ">
                                    {src}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                else:
                    st.info("No sources were relevant enough to cite.")

            else:
                st.error(f"API Error {response.status_code}")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error("❌ Could not connect to FastAPI backend.")
            st.text(str(e))

elif ask_button:
    st.warning("Please enter a question.")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()
st.caption(
    "FINWISER.AI – Retrieval-Augmented Generation over SEC filings | Hackathon Demo"
)
