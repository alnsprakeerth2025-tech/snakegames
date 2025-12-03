import streamlit as st
import time
import random

# --- Streamlit page setup ---
st.set_page_config(page_title="Snake Game", layout="centered")
st.title("🐍 Simple Snake Game")

# --- Game board size ---
ROWS = 20
COLS = 20

# --- Initialize game state ---
if "snake" not in st.session_state:
    st.session_state.snake = [(10, 10)]  # snake head in the middle
if "direction" not in st.session_state:
    st.session_state.direction = "RIGHT"
if "food" not in st.session_state:
    st.session_state.food = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
if "game_over" not in st.session_state:
    st.session_state.game_over = False


# --- Helper functions ---
def move_snake():
    head = st.session_state.snake[0]
    r, c = head

    if st.session_state.direction == "UP":
        r -= 1
    elif st.session_state.direction == "DOWN":
        r += 1
    elif st.session_state.direction == "LEFT":
        c -= 1
    elif st.session_state.direction == "RIGHT":
        c += 1

    new_head = (r, c)
    return new_head


def reset_game():
    st.session_state.snake = [(10, 10)]
    st.session_state.direction = "RIGHT"
    st.session_state.food = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    st.session_state.game_over = False


# --- Direction Controls ---
st.write("Use the buttons to move the snake:")

col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️"):
        st.session_state.direction = "UP"

with col1:
    if st.button("⬅️"):
        st.session_state.direction = "LEFT"

with col3:
    if st.button("➡️"):
        st.session_state.direction = "RIGHT"

with col2:
    if st.button("⬇️"):
        st.session_state.direction = "DOWN"


# --- Game Loop ---
if not st.session_state.game_over:
    new_head = move_snake()

    # Check collisions
    r, c = new_head
    if (
        r < 0 or r >= ROWS or
        c < 0 or c >= COLS or
        new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
    else:
        # Move snake
        st.session_state.snake.insert(0, new_head)

        # Check if food eaten
        if new_head == st.session_state.food:
            st.session_state.food = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        else:
            st.session_state.snake.pop()


# --- Draw the board ---
board = [["⬛" for _ in range(COLS)] for _ in range(ROWS)]

# Draw food
fr, fc = st.session_state.food
board[fr][fc] = "🍎"

# Draw snake
for i, (r, c) in enumerate(st.session_state.snake):
    board[r][c] = "🟩" if i == 0 else "🟢"

# Display board
game_board = "\n".join("".join(row) for row in board)
st.code(game_board)

# Game over text
if st.session_state.game_over:
    st.error("💀 Game Over!")
    if st.button("Restart Game"):
        reset_game()

# Auto-refresh every 200ms
time.sleep(0.2)
st.experimental_rerun()
