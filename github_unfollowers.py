import streamlit as st
import requests

st.set_page_config(page_title="GitHub Unfollowers", page_icon="♛", layout="centered")

# Uygulama için özel CSS stilleri

st.markdown("""
    <style>
    @keyframes gradientBackground {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .stApp {
        background: linear-gradient(135deg, #FF914D, #4FD1C5, #6EC1E4, #D6BCFA);
        background-size: 600% 600%;
        animation: gradientBackground 20s ease infinite;
        font-family: 'Segoe UI', sans-serif;
        color: #1a1a1a;
    }

    h1, h2, h3, h4, h5, h6, p, li, span {
        color: #1a1a1a !important;
    }

    .css-18e3th9 {
        background-color: rgba(255, 255, 255, 0.92);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.07);
    }

    .stButton>button {
        background-color: #FF914D;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.8rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    .stButton>button:hover {
        background-color: #ff7f2a;
        transform: scale(1.05);
    }

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        padding: 2rem 1rem;
        border-radius: 20px;
        box-shadow: 0 0 20px rgba(0,0,0,0.07);
        margin-top: 20px;
        margin-bottom: 20px;
    }

    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Uygulama başlığı ve açıklama

st.image("logo.png", width=150)
st.title("Github Geri Takip Etmeyenler")

st.markdown("""
Bu uygulama, takip ettiğiniz ama sizi geri takip etmeyen GitHub kullanıcılarını listeler.  
Kullanmak için sadece GitHub kullanıcı adınızı girmeniz yeterlidir.  
**Token girerseniz** daha fazla sorgu hakkınız olur ve hata almazsınız.
""")

st.sidebar.header("Giriş")
username = st.sidebar.text_input("👤 GitHub kullanıcı adı", value="username")
token = st.sidebar.text_input("🔑 GitHub Token (opsiyonel)", type="password")

headers = {
    "Authorization": f"token {token}" if token else None
}

def get_users_list(username, endpoint):
    users = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/{endpoint}?page={page}&per_page=100"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            st.error(f"Hata [{response.status_code}]: {response.json().get('message')}")
            break

        data = response.json()
        if not data:
            break
        users.extend([user["login"] for user in data])
        page += 1
    return users

if st.button("🚀 Analizi Başlat"):
    if not username:
        st.warning("❗ Lütfen bir kullanıcı adı girin.")
    else:
        with st.spinner("🔍 Veriler alınıyor..."):
            following = set(get_users_list(username, "following"))
            followers = set(get_users_list(username, "followers"))
            not_following_back = sorted(following - followers)

        st.markdown("---")
        st.subheader("🚫 Geri Takip Etmeyenler")

        if not_following_back:
            st.write(f"Toplam **{len(not_following_back)}** kişi seni geri takip etmiyor:")
            for user in not_following_back:
                st.markdown(f"- [@{user}](https://github.com/{user})")
        else:
            st.success("🎉 Harika! Herkes seni geri takip ediyor. 😇")

st.markdown("---")
st.caption("© 2025 • Hazırlayan: Büşra Deveci • GitHub API kullanılmıştır")
