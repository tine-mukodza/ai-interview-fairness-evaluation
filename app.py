import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re
import random

# ---------------------------------------------------------
# PAGE CONFIG + GLOBAL CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="st.title("Human-Centered AI Interview Fairness Evaluation")
",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    div.block-container {
        max-width: 1100px;
        padding-top: 1.2rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* General typography tweaks */
    h1, h2, h3 {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .stMarkdown h3 {
        font-size: 1.05rem !important;
        margin-bottom: 0.35rem;
    }

    /* Card feel for containers */
    .st-emotion-cache-1r6slb0, .st-emotion-cache-1r6slb0 div[role="group"] {
        border-radius: 10px;
    }

    /* Step tracker chips */
    .step-chip {
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.8rem;
        text-align: center;
        border: 1px solid #374151;
        background: #020617;
        color: #e5e7eb;
        opacity: 0.7;
    }
    .step-chip-active {
        border-color: #3b82f6;
        background: linear-gradient(90deg, #1d4ed8, #3b82f6);
        color: white;
        opacity: 1;
        font-weight: 600;
    }
    .step-chip-done {
        border-color: #16a34a;
        background: #022c22;
        color: #bbf7d0;
        opacity: 0.9;
    }

    /* Make expander headers a bit stronger */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# HELPERS & CORE LOGIC
# ---------------------------------------------------------
def card(title, body="", icon=""):
    """Simple bordered card block with optional title."""
    with st.container(border=True):
        if title:
            st.markdown(f"### {icon} {title}")
        if body:
            st.write(body)


def extract_keywords(text: str):
    """Very lightweight keyword extractor (no ML)."""
    words = re.findall(r"[A-Za-z']+", text.lower())
    stop = set(
        [
            "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with",
            "my", "your", "our", "their", "you", "i", "we", "was", "were", "is",
            "are", "that", "this", "from", "have", "has", "had", "been", "at",
            "as", "by", "it", "itself",
        ]
    )
    keywords = [w for w in words if w not in stop and len(w) > 3]
    return list(dict.fromkeys(keywords))[:8]  # top 8, unique, ordered


# ---------------------------------------------------------
# VALUES, SCENARIOS & FOLLOW-UPS
# ---------------------------------------------------------
VALUES = {
    "Collaboration": ["team", "together", "support", "conflict", "help"],
    "Integrity": ["ethical", "honest", "truth", "responsible", "fair"],
    "Ownership": ["initiative", "led", "managed", "owned", "accountable"],
    "Customer Focus": ["customer", "client", "user", "service", "needs"],
    "Data Responsibility": ["data", "privacy", "security", "accuracy", "bias"],
}

SCENARIOS = [
    {
        "name": "Scenario 1 – Collaboration (Team Conflict)",
        "prompt": "Tell me about a time you worked with a team to solve a difficult problem.",
        "value": "Collaboration",
    },
    {
        "name": "Scenario 2 – Integrity (Ethical Dilemma)",
        "prompt": "Describe a situation where you had to choose the ethical option under pressure.",
        "value": "Integrity",
    },
    {
        "name": "Scenario 3 – Ownership (Taking Initiative)",
        "prompt": "Tell me about a time you took initiative without being asked.",
        "value": "Ownership",
    },
    {
        "name": "Scenario 4 – Data Responsibility (Handling Sensitive Info)",
        "prompt": "Describe a moment when you handled sensitive data or ensured data accuracy.",
        "value": "Data Responsibility",
    },
    {
        "name": "Scenario 5 – Customer Focus (User Impact)",
        "prompt": "Tell me about a time you improved a customer or user experience.",
        "value": "Customer Focus",
    },
]

FOLLOWUP_BANK = {
    "Collaboration": [
        "What role did you personally play in helping the team succeed?",
        "How did you handle disagreement or tension in the group?",
        "What did you learn about teamwork from that experience?",
    ],
    "Integrity": [
        "What made that decision ethically difficult?",
        "How did you communicate your choice to others?",
        "Looking back, would you do anything differently?",
    ],
    "Ownership": [
        "What motivated you to take initiative in that situation?",
        "How did you measure success for that project?",
        "What obstacles did you face and how did you handle them?",
    ],
    "Customer Focus": [
        "How did you identify what the customer or user actually needed?",
        "What change did you make and what was its impact?",
        "How did you gather feedback after your solution?",
    ],
    "Data Responsibility": [
        "How did you make sure the data was accurate or handled safely?",
        "What risks did you consider when working with that data?",
        "How did your actions protect stakeholders or users?",
    ],
}


def detect_value_tag(answer_text: str):
    """Heuristic value detector based on word matches."""
    answer_text = answer_text.lower()
    scores = {v: 0 for v in VALUES.keys()}

    for v, kws in VALUES.items():
        for k in kws:
            if k in answer_text:
                scores[v] += 1

    best_value = max(scores, key=scores.get)
    if scores[best_value] == 0:
        return "General Professionalism", "Low"
    elif scores[best_value] <= 2:
        return best_value, "Medium"
    else:
        return best_value, "High"


def generate_followup(resume_text: str, answer_text: str, chosen_value: str):
    """Generates a follow-up question + explanation using earlier logic."""
    detected_value, confidence = detect_value_tag(answer_text)

    # Respect the scenario target value; report detected as internal guess only
    value_tag = chosen_value
    followup = random.choice(FOLLOWUP_BANK[value_tag])

    resume_kws = extract_keywords(resume_text)
    answer_kws = extract_keywords(answer_text)

    reasoning = (
        f"The follow-up targets **{value_tag}** based on the scenario you selected. "
        f"In your resume, I noticed: {', '.join(resume_kws) or 'no clear keywords'}. "
        f"In your answer, I noticed: {', '.join(answer_kws) or 'no clear keywords'}. "
        f"The system's internal guess from your answer alone was **{detected_value}** "
        f"with **{confidence}** confidence."
    )

    return followup, reasoning, value_tag, confidence, resume_kws, answer_kws


def neutralize_question(q: str) -> str:
    """Softens a question if the participant flags it as unfair."""
    if not q:
        return ""
    return "In any context you’re comfortable sharing, " + q[0].lower() + q[1:]


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------
LOG_FILE = "interview_logs.csv"


def log_row(row: dict):
    df_row = pd.DataFrame([row])
    if os.path.exists(LOG_FILE):
        df_existing = pd.read_csv(LOG_FILE)
        df_all = pd.concat([df_existing, df_row], ignore_index=True)
    else:
        df_all = df_row
    df_all.to_csv(LOG_FILE, index=False)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
defaults = {
    "consent": False,
    "resume_done": False,
    "scenario_done": False,
    "answer_done": False,
    "followup_done": False,
    "active_step": 1,  # 1–5 (after consent)
    "exp1_open": True,
    "exp2_open": False,
    "exp3_open": False,
    "exp4_open": False,
    "exp5_open": False,
    "scenario_prompt": "",
    "scenario_name": SCENARIOS[0]["name"],
    "prev_scenario_name": None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ---------------------------------------------------------
# UI HELPERS – STEP TRACKER
# ---------------------------------------------------------
def render_step_tracker():
    labels = [
        "1. Resume",
        "2. Scenario",
        "3. Response",
        "4. AI Question",
        "5. Feedback",
    ]
    cols = st.columns(len(labels))

    for idx, (col, label) in enumerate(zip(cols, labels), start=1):
        with col:
            if st.session_state.active_step == idx:
                cls = "step-chip step-chip-active"
            elif (
                (idx == 1 and st.session_state.resume_done)
                or (idx == 2 and st.session_state.scenario_done)
                or (idx == 3 and st.session_state.answer_done)
                or (idx == 4 and st.session_state.followup_done)
                or (idx == 5 and st.session_state.followup_done)
            ):
                cls = "step-chip step-chip-done"
            else:
                cls = "step-chip"
            st.markdown(f"<div class='{cls}'>{label}</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.header("Study Settings")
    st.text_input(
        "Participant ID (optional)",
        key="participant_id",
        placeholder="P01, P02 …",
    )
    st.markdown("---")
    st.caption("Target values in this study:")
    st.write(", ".join(VALUES.keys()))
    st.markdown("---")
    if st.button("Reset session"):
        st.session_state.clear()
        st.rerun()

# ---------------------------------------------------------
# TITLE + GLOBAL PROGRESS
# ---------------------------------------------------------
st.title("🤖 Human-Centered AI Interview Prototype")
st.caption("Explainable Fairness Prototype • Pace University Seidenberg")

st.markdown(f"**Step {st.session_state.active_step} of 5**")
st.progress((st.session_state.active_step - 1) / 5)
render_step_tracker()
st.caption(
    "Only the current step is expanded. You can re-open earlier steps any time to review or edit."
)

with st.expander("What is this study about?"):
    st.write(
        "- Test an AI interviewer that generates value-aligned follow-up questions.\n"
        "- Show how the AI uses your resume and answer (transparency).\n"
        "- Let you rate how fair and clear everything feels.\n"
        "- You can use a fictitious resume if you prefer; no real name is required."
    )

# ---------------------------------------------------------
# CONSENT GATE
# ---------------------------------------------------------
card(
    "Consent to Participate",
    icon="✅",
    body=(
        "- Participation is voluntary.\n"
        "- You may paste either a short summary or a fictitious resume.\n"
        "- We only use responses for a classroom research project on fairness and usability.\n"
        "- You can stop at any time by closing the page or using the reset button."
    ),
)

consent = st.checkbox(
    "I have read this summary and I agree to take part in this prototype study.",
    value=st.session_state.consent,
)
st.session_state.consent = consent

if not st.session_state.consent:
    st.info("Please give your consent above to start the interview steps.")
    st.stop()

st.success("Thank you for consenting. Step 1 will guide you through the process.")

# ---------------------------------------------------------
# STEP 1 – RESUME / EXPERIENCE
# ---------------------------------------------------------
step1_label = "Step 1 – Resume / Experience Context"
if st.session_state.resume_done and st.session_state.active_step != 1:
    rt_len = len(st.session_state.get("resume_text", "").strip())
    step1_label += f"  ✅ (about {rt_len} characters)"

with st.expander(step1_label, expanded=st.session_state.exp1_open):
    card(
        "",
        icon="📄",
        body=(
            "Paste a short summary or your full resume text. Personal details are optional. "
            "We only use this text so the AI can personalise its follow-up question."
        ),
    )

    st.text_area(
        "Resume or summary",
        key="resume_text",
        height=220,
        placeholder=(
            "Example:\n"
            "I have experience in SQL, Power BI, and team-based analytics projects in finance "
            "and operations. Recently I..."
        ),
    )

    if st.session_state.get("resume_text"):
        st.caption(f"Characters provided: {len(st.session_state['resume_text'])}")

    if st.button("Save and continue to Step 2", key="btn_step1"):
        if not st.session_state["resume_text"].strip():
            st.error("Please add at least a short summary or resume text before continuing.")
        else:
            st.session_state.resume_done = True
            st.session_state.active_step = 2
            st.session_state.exp1_open = False
            st.session_state.exp2_open = True
            st.success("Resume saved. Moving to Step 2.")
            st.rerun()

# ---------------------------------------------------------
# STEP 2 – SCENARIO SELECTION (updated text + read-only prompt)
# ---------------------------------------------------------
if st.session_state.resume_done:
    step2_label = "Step 2 – Choose Interview Scenario"
    if st.session_state.scenario_done and st.session_state.active_step != 2:
        step2_label += f"  ✅ ({st.session_state.get('scenario_name', '')})"

    with st.expander(step2_label, expanded=st.session_state.exp2_open):
        card(
            "",
            icon="🎯",
            body="Pick one scenario.",
        )

        scenario_names = [s["name"] for s in SCENARIOS]

        st.selectbox(
            "Scenario",
            options=scenario_names,
            key="scenario_name",
        )

        # Reset prompt when scenario changes
        if st.session_state.prev_scenario_name != st.session_state.scenario_name:
            base_scenario = next(
                s for s in SCENARIOS if s["name"] == st.session_state.scenario_name
            )
            st.session_state.scenario_prompt = base_scenario["prompt"]
            st.session_state.prev_scenario_name = st.session_state.scenario_name

        # Read-only scenario prompt
        st.text_area(
            "Scenario prompt",
            key="scenario_prompt",
            height=80,
            disabled=True,
        )

        if st.button("Save and continue to Step 3", key="btn_step2"):
            st.session_state.scenario_done = True
            st.session_state.active_step = 3
            st.session_state.exp2_open = False
            st.session_state.exp3_open = True
            st.success("Scenario saved. Moving to Step 3.")
            st.rerun()
else:
    st.info("Complete Step 1 first. Step 2 will appear after you save your resume/experience.")

# ---------------------------------------------------------
# STEP 3 – CANDIDATE ANSWER
# ---------------------------------------------------------
if st.session_state.scenario_done:
    step3_label = "Step 3 – Your Response"
    if st.session_state.answer_done and st.session_state.active_step != 3:
        step3_label += "  ✅ (answer saved)"

    with st.expander(step3_label, expanded=st.session_state.exp3_open):
        card(
            "",
            icon="🗣️",
            body="Answer the scenario in your own words. There is no ‘right’ length.",
        )

        chosen_scenario = next(
            s for s in SCENARIOS
            if s["name"] == st.session_state.get("scenario_name", SCENARIOS[0]["name"])
        )
        scenario_text = st.session_state.get("scenario_prompt", chosen_scenario["prompt"])

        st.markdown(f"**Scenario:** {scenario_text}")

        st.text_area(
            "Your answer",
            key="answer_text",
            height=150,
            placeholder="Type your answer here…",
        )

        if st.button("Save and continue to Step 4", key="btn_step3"):
            if not st.session_state["answer_text"].strip():
                st.error("Please write your answer before continuing.")
            else:
                st.session_state.answer_done = True
                st.session_state.active_step = 4
                st.session_state.exp3_open = False
                st.session_state.exp4_open = True
                st.success("Answer saved. Moving to Step 4.")
                st.rerun()
else:
    st.info("Complete Step 2 first. Step 3 will appear after you save your scenario choice.")

# ---------------------------------------------------------
# STEP 4 – AI FOLLOW-UP + EXPLAINABILITY
# ---------------------------------------------------------
if st.session_state.answer_done:
    step4_label = "Step 4 – AI Follow-Up Question & Explanation"
    if st.session_state.followup_done and st.session_state.active_step != 4:
        step4_label += "  ✅ (question generated)"

    with st.expander(step4_label, expanded=st.session_state.exp4_open):
        card(
            "",
            icon="✨",
            body="Now the AI generates a follow-up question and explains why it chose it.",
        )

        resume_text = st.session_state.get("resume_text", "")
        answer_text = st.session_state.get("answer_text", "")
        chosen_scenario = next(
            s for s in SCENARIOS
            if s["name"] == st.session_state.get("scenario_name", SCENARIOS[0]["name"])
        )

        gen = st.button(
            "Generate / Refresh Follow-Up Question",
            key="btn_generate",
            type="primary",
        )

        if gen:
            if not (resume_text.strip() and answer_text.strip()):
                st.error("Please make sure both your resume/experience and your answer are filled in.")
            else:
                (
                    followup,
                    reasoning,
                    value_tag,
                    confidence,
                    resume_kws,
                    answer_kws,
                ) = generate_followup(
                    resume_text, answer_text, chosen_scenario["value"]
                )
                st.session_state["followup"] = followup
                st.session_state["reasoning"] = reasoning
                st.session_state["value_tag"] = value_tag
                st.session_state["confidence"] = confidence
                st.session_state["resume_kws"] = resume_kws
                st.session_state["answer_kws"] = answer_kws
                st.session_state.followup_done = True
                st.session_state.active_step = 5
                st.session_state.exp4_open = False
                st.session_state.exp5_open = True
                st.success("Follow-up generated. Moving to Step 5.")
                st.rerun()

        if "followup" in st.session_state:
            # Highlighted AI question card
            st.markdown(
                f"""
                <div style='margin-top:0.5rem; margin-bottom:0.5rem;
                            padding:0.9rem 1rem; border-radius:10px;
                            border-left:4px solid #3b82f6;
                            background-color:#020617;'>
                    <div style='font-size:0.85rem; text-transform:uppercase;
                                letter-spacing:0.05em; color:#9ca3af; margin-bottom:0.25rem;'>
                        AI Follow-Up Question
                    </div>
                    <div style='font-size:1rem; color:#e5e7eb;'>
                        <b>{st.session_state['followup']}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.container(border=True):
                st.markdown("#### 🧠 Why this question?")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Target value (scenario)**")
                    st.write(st.session_state.get("value_tag", "N/A"))
                    dv, conf = detect_value_tag(answer_text)
                    st.markdown("**System value guess (from your answer)**")
                    st.write(f"{dv} ({conf} confidence)")

                with col2:
                    st.markdown("**Resume keywords detected**")
                    resume_kws_str = ", ".join(st.session_state.get("resume_kws", [])) or "None detected"
                    st.write(resume_kws_str)

                    st.markdown("**Answer keywords detected**")
                    answer_kws_str = ", ".join(st.session_state.get("answer_kws", [])) or "None detected"
                    st.write(answer_kws_str)

                st.markdown("**Reasoning summary**")
                st.write(st.session_state.get("reasoning", ""))

else:
    st.info("Complete Step 3 first. Step 4 will appear after you save your answer.")

# ---------------------------------------------------------
# STEP 5 – FAIRNESS & EXPERIENCE FEEDBACK (updated ratings)
# ---------------------------------------------------------
if st.session_state.followup_done:
    step5_label = "Step 5 – Fairness & Experience Feedback"
    with st.expander(step5_label, expanded=st.session_state.exp5_open):
        card(
            "",
            icon="⚖️",
            body=(
                "Rate how this follow-up question felt. You can also flag it as unfair or uncomfortable."
            ),
        )

        st.markdown("**Follow-up question shown to you:**")
        st.write(f"_{st.session_state['followup']}_")

        flag_unfair = st.checkbox("I felt this follow-up was unfair, biased, or uncomfortable.")

        unfair_comment = ""
        neutral_q = ""
        if flag_unfair:
            neutral_q = neutralize_question(st.session_state["followup"])
            st.warning("Suggested neutral rephrasing:")
            st.write(f"**{neutral_q}**")
            unfair_comment = st.text_input(
                "Optional: What felt unfair?",
                placeholder="E.g., too personal, unclear, stereotype risk…",
            )

        st.markdown("#### Quick ratings")

        col_a, col_b = st.columns(2)
        with col_a:
            fairness_score = st.slider(
                "How fair did the AI’s follow-up question feel?",
                1, 5, 3
            )
            relevance_score = st.slider(
                "How appropriate was this question for your scenario and answer?",
                1, 5, 3
            )
        with col_b:
            comfort_score = st.slider(
                "How comfortable would you feel answering this question in a real interview?",
                1, 5, 3
            )
            trust_score = st.slider(
                "How much would you trust an interviewer that uses an AI like this?",
                1, 5, 3
            )

        accept_ai = st.radio(
            "Would you accept this type of AI interviewer in a real hiring process?",
            ["Yes", "No", "Not sure"],
        )

        open_feedback = st.text_area(
            "Anything else you want to tell us about this question or interface?",
            height=80,
        )

        if st.button("Save my feedback and finish", key="btn_save_feedback", type="primary"):
            chosen_scenario = next(
                s for s in SCENARIOS
                if s["name"] == st.session_state.get("scenario_name", SCENARIOS[0]["name"])
            )
            scenario_text = st.session_state.get("scenario_prompt", chosen_scenario["prompt"])

            row = {
                "timestamp": datetime.now().isoformat(),
                "participant_id": st.session_state.get("participant_id", ""),
                "scenario": chosen_scenario["name"],
                "scenario_prompt_used": scenario_text,
                "target_value": chosen_scenario["value"],
                "resume_text": st.session_state.get("resume_text", ""),
                "answer_text": st.session_state.get("answer_text", ""),
                "followup_question": st.session_state["followup"],
                "reasoning_summary": st.session_state.get("reasoning", ""),
                "resume_keywords": ", ".join(st.session_state.get("resume_kws", [])),
                "answer_keywords": ", ".join(st.session_state.get("answer_kws", [])),
                "value_tag": st.session_state.get("value_tag", ""),
                "confidence": st.session_state.get("confidence", ""),

                # HCI-standard metrics
                "fairness_score": fairness_score,
                "relevance_score": relevance_score,
                "comfort_score": comfort_score,
                "trust_score": trust_score,

                "flag_unfair": flag_unfair,
                "unfair_comment": unfair_comment,
                "neutralized_question": neutral_q,
                "accept_ai": accept_ai,
                "open_feedback": open_feedback,
            }

            log_row(row)
            st.success("Thank you! Your feedback has been saved to interview_logs.csv.")

            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "rb") as f:
                    st.download_button(
                        "Download interview_logs.csv",
                        data=f,
                        file_name="interview_logs.csv",
                        mime="text/csv",
                    )

            st.caption("You can close this window or use the reset button in the sidebar to start again.")

st.caption("Prototype for IS 617 • Human-Centered Computing • Pace University Seidenberg")
