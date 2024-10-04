# In streamlit_app.py or style.py
st.markdown("""
    <style>
    .button {
        display: block;
        padding: 0.75em 1.5em;
        text-decoration: none;
        font-weight: bold;
        border-radius: 5px;
        margin: 10px auto;
        color: white !important;
        text-align: center;
        width: 200px;
    }
    .goodreads {
        background-color: #D7A168;
    }
    .amazon {
        background-color: #FF9900;
    }
    .abebooks {
        background-color: #CC3333;
    }
    .libby {
        background-color: #8E5A9E;
    }
    .lapl {
        background-color: #003C71;
    }
    .bookshop {
        background-color: #017AFF;
    }
    .storygraph {
        background-color: #5B21B6;
    }
    </style>
""", unsafe_allow_html=True)
