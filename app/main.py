import streamlit as st
import urllib.parse
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.markdown("""
    <style>

    .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
    }

    .stTextInput input{
        border-radius:12px;
        border:1px solid #4b5563;
        padding:12px 16px;
        font-size:16px;
    }

    .stTextInput input:focus{
        border-color:#2563eb;
        box-shadow:0 0 0 3px rgba(37,99,235,.18);
    }

    .stButton>button{
        border-radius:12px;
        background:#2563eb;
        color:white;
        border:none;
        padding:0.7rem 1.5rem;
        font-weight:600;
        font-size:15px;
        transition:.25s;
    }

    .stButton>button:hover{
        background:#1d4ed8;
        color:white;
    }

    .stLinkButton>a{
        background:#EA4335;
        color:white !important;
        border-radius:12px;
        padding:0.7rem 1.5rem;
        text-decoration:none;
        font-weight:600;
    }

    .stLinkButton>a:hover{
        background:#d93025;
        color:white !important;
    }

    textarea{
        border-radius:12px !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title("📧 AI Cold Email Generator")

    st.markdown(
        """
        Generate personalised cold emails from job postings.

        Paste a job URL below and let AI generate a tailored outreach email in seconds.
        """
    )

    st.divider()

    st.subheader("🔗 Job Posting URL")

    url_input = st.text_input(
        "",
        placeholder="https://company.com/careers/job-id"
    )

    submit_button = st.button("🚀 Generate Cold Email")

    if submit_button:
        if not url_input.strip():
            st.warning("Please enter a valid job URL.")
            return
        
        try:
            with st.spinner("Generating your cold email..."):
                loader = WebBaseLoader([url_input])
                data = clean_text(
                    loader.load().pop().page_content
                )

                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                for job in jobs:
                    skills = job.get("skills", [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.divider()
                    company = job.get("company", "Not Available")
                    role = job.get("role", "Not Available")
                    experience = job.get("experience", "Not Available")
                    left, right = st.columns([1, 2], gap="large")

                    with left:

                        with st.container(border=True):
                            st.subheader("💼 Job Details")
                            st.markdown("#### 🏢 Company")
                            st.write(company)
                            st.markdown("#### 💼 Role")
                            st.write(role)
                            st.markdown("#### 📈 Experience")
                            st.write(experience)
                            st.markdown("#### 🛠 Skills")

                            if skills:
                                badge_html = ""

                                for skill in skills:
                                    badge_html += f"""
                                    <span style="
                                        display:inline-block;
                                        background:#2563eb;
                                        color:white;
                                        padding:6px 12px;
                                        margin:4px;
                                        border-radius:20px;
                                        font-size:13px;
                                        font-weight:500;">
                                        {skill}
                                    </span>
                                    """

                                st.markdown(
                                    badge_html,
                                    unsafe_allow_html=True
                                )

                            else:
                                st.info("No skills detected.")

                    with right:

                        with st.container(border=True):
                            st.subheader("📝 Generated Email")
                            st.text_area(
                                "",
                                value=email,
                                height=500,
                                key="generated_email",
                            )

                            st.write("")
                            subject = f"Regarding {role} Opportunity"

                            gmail_url = (
                                "https://mail.google.com/mail/?view=cm&fs=1"
                                f"&su={urllib.parse.quote(subject)}"
                                f"&body={urllib.parse.quote(email)}"
                            )

                            col1, col2, col3 = st.columns([1,2,1])

                            with col2:
                                st.link_button(
                                    "📧 Gmail",
                                    gmail_url,
                                )

        except Exception as e:
            st.error(f"An Error Occurred: {e}")

            st.divider()

        st.markdown(
            """
        <div style="text-align:center; color:grey;">

        Built with ❤️ using

        <b>llama 3.3</b> •
        <b>ChromaDB</b>  •
        <b>LangChain</b> •
        <b>Streamlit</b> 

        </div>
        """,
            unsafe_allow_html=True
        )


if __name__ == "__main__":

    st.set_page_config(
        page_title="Cold Email Generator",
        page_icon="📧",
        layout="wide"
    )

    chain = Chain()
    portfolio = Portfolio()

    create_streamlit_app(chain, portfolio, clean_text)