import streamlit as st
import math

st.set_page_config(page_title="Advanced Calculator", layout="centered")

# ---------------- SESSION STATE ----------------
if "expression" not in st.session_state:
    st.session_state.expression = st.session_state.expression.split("=")[0]

if "history" not in st.session_state:
    st.session_state.history = []

if "memory" not in st.session_state:
    st.session_state.memory = 0

# ---------------- SAFE EVAL ----------------
def safe_eval(expr):
    allowed = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log10,
        "ln": math.log,
        "pi": math.pi,
        "e": math.e,
        "pow": pow,
        "abs": abs
    }
    return eval(expr, {"__builtins__": None}, allowed)

# ---------------- CALCULATE ----------------
def calculate():
    try:
        result = str(safe_eval(st.session_state.expression))
        st.session_state.expression = f"{st.session_state.expression} = {result}"
        st.session_state.history.append(st.session_state.expression)
    except:
        st.session_state.expression = "Error"

# ---------------- ENTER KEY ----------------
def enter_pressed():
    calculate()  # Keyboard Enter → show question + result

# ---------------- DISPLAY ----------------
st.title("🧮 Advanced Calculator")

# Display + Keyboard support
st.text_input(
    "Display (Type & Press Enter)",
    key="expression",
    on_change=enter_pressed
)

# ---------------- BUTTON FUNCTION ----------------
def press(val):
    # Clear previous result if typing new number
    if "=" in st.session_state.expression and val not in ["=", "C", "DEL", "M+", "M-", "MR", "MC"]:
        st.session_state.expression = ""
    
    if val == "C":
        st.session_state.expression = ""
    elif val == "DEL":
        st.session_state.expression = st.session_state.expression[:-1]
    elif val == "=":
        calculate()  # Mouse click → question + result
    # Memory
    elif val == "M+":
        try:
            st.session_state.memory += float(st.session_state.expression.split('=')[0])
        except:
            pass
    elif val == "M-":
        try:
            st.session_state.memory -= float(st.session_state.expression.split('=')[0])
        except:
            pass
    elif val == "MR":
        st.session_state.expression += str(st.session_state.memory)
    elif val == "MC":
        st.session_state.memory = 0
    else:
        st.session_state.expression += str(val)

# ---------------- BUTTONS ----------------
buttons = [
    ["MC", "MR", "M+", "M-"],
    ["7","8","9","/"],
    ["4","5","6","*"],
    ["1","2","3","-"],
    ["0",".","+","="],
    ["C","DEL","(",")"]
]

for row in buttons:
    cols = st.columns(4)
    for i, btn in enumerate(row):
        cols[i].button(btn, on_click=press, args=(btn,), use_container_width=True)

# ---------------- MEMORY ----------------
st.write(f"🧠 Memory: {st.session_state.memory}")

# ---------------- HISTORY ----------------
st.subheader("History")
for item in reversed(st.session_state.history[-10:]):
    st.write(item)