import streamlit as st
import random

# --- Page config ---
st.set_page_config(page_title="Number Guessing Game", page_icon="🎮", layout="centered")

# --- CSS Background ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80");
    color: RGB(15 119 223);
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Session state for navigation and game ---
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "random_number" not in st.session_state:
    st.session_state.random_number = None
if "guesses" not in st.session_state:
    st.session_state.guesses = 0
if "top_of_range" not in st.session_state:
    st.session_state.top_of_range = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "high_score" not in st.session_state:   # 🏆 Highest Score tracker
    st.session_state.high_score = None

# --- Welcome Page ---
if st.session_state.page == "welcome":
    st.markdown("<h1 style='text-align:center;'>🎮 Welcome to the Number 🎮  Guessing Game </h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Try to guess the secret number!</h3>", unsafe_allow_html=True)

    # Show highest score if available
    if st.session_state.high_score:
        st.info(f"🏆 Highest Score: {st.session_state.high_score} guesses")

    if st.button("▶️ Play", use_container_width=True):
        st.session_state.page = "game"
        st.rerun()

# --- Game Page ---
elif st.session_state.page == "game":
    st.title("🎯 Number Guessing Game")

    # --- Start game form ---
    with st.form("start_form"):
        top_of_range = st.number_input("🔢 Enter the maximum number:", min_value=1, step=1, key="range_input")
        start_game = st.form_submit_button("🚀 Start Game")
        if start_game:
            st.session_state.top_of_range = top_of_range
            st.session_state.random_number = random.randint(0, top_of_range)
            st.session_state.guesses = 0
            st.session_state.history = []
            st.success(f"Game started! Guess a number between 0 and {top_of_range}.")

    st.divider()

    # --- Guessing form ---
    if st.session_state.random_number is not None:
        with st.form("guess_form"):
            user_guess = st.number_input("🎯 Enter your guess:", min_value=0, step=1, key="guess_input")
            check_guess = st.form_submit_button("✅ Check Guess")
            
            if check_guess:
                st.session_state.guesses += 1
                st.session_state.history.append(user_guess)

                if user_guess == st.session_state.random_number:
                    st.success(f"🎉 You got it in {st.session_state.guesses} guesses!")
                    st.balloons()

                    # 🏆 Update highest score
                    if (st.session_state.high_score is None) or (st.session_state.guesses < st.session_state.high_score):
                        st.session_state.high_score = st.session_state.guesses
                        st.success("🥇 New High Score!")

                    st.session_state.random_number = None
                elif user_guess > st.session_state.random_number:
                    st.warning("📈 Your guess is too high!")
                else:
                    st.info("📉 Your guess is too low!")

        # Show previous guesses
        if st.session_state.history:
            st.subheader("📜 Previous Guesses")
            st.write(", ".join(map(str, st.session_state.history)))

    # --- Show Highest Score during game ---
    if st.session_state.high_score:
        st.info(f"🏆 Current Highest Score: {st.session_state.high_score} guesses")

    # --- Play Again or Back to Home ---
    if st.session_state.random_number is None and st.session_state.guesses > 0:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Play Again", use_container_width=True):
                st.session_state.random_number = None
                st.session_state.guesses = 0
                st.session_state.history = []
                st.session_state.top_of_range = 0
                st.rerun()
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.page = "welcome"
                st.rerun()
