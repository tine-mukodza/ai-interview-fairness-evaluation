# AI Interview Transparency (HCI Case Study)

> Human-centered AI case study exploring transparency, fairness, and trust in AI-assisted interview systems through an interactive prototype.

**Topics:** human-centered-ai · explainable-ai · systems-design · hci · ai-transparency · streamlit

---

## Overview
This repository contains a human-centered AI prototype developed as a case study in transparency, fairness, and trust within AI-assisted interview systems.

The project examines how candidates experience AI-generated interview follow-up questions when system reasoning is made visible and when users are given agency through optional alternative phrasing. The prototype is designed as an **interaction and systems design study**, not a production hiring tool.

---

## Why This Project Matters
AI-driven interview and assessment tools are increasingly used in recruitment, yet most operate as black boxes from the candidate’s perspective.

Candidates rarely see:
- why specific follow-up questions are asked  
- how their responses are interpreted  
- whether alternative, less intrusive question phrasing is possible  

This project explores how **transparency and user agency at the interface level** affect perceived fairness, comfort, relevance, and trust.

---

## What the Prototype Demonstrates
- Resume-aware contextual interaction  
- Scenario-based interview flow  
- AI-generated follow-up interview questions  
- Plain-language explanation of system behavior  
- Optional neutral alternative phrasing  
- Candidate ratings of fairness, comfort, relevance, and trust  

> The AI logic is intentionally lightweight and rule-based to keep the focus on interaction quality and decision transparency rather than model performance.

---

## What This Is — and What It Is Not

### This project **is**:
- A human-centered interaction design case study  
- An example of explainable AI at the interface level  
- A candidate-side transparency and trust prototype  

### This project **is not**:
- A real hiring or recruitment system  
- A candidate scoring or ranking model  
- A claim of improved hiring accuracy  

---

## Technology Stack
- Python  
- Streamlit  
- Pandas  
- CSV and Excel exports for analysis  

---

## Repository Structure
- **app.py** — Streamlit application  
- **requirements.txt** — Python dependencies  
- **README.md** — Project documentation  

---

## Running the Prototype Locally
```bash
pip install -r requirements.txt
streamlit run app.py

```
# The application will open in your browser.

## Data and Ethics

Participation is voluntary.
Users may provide fictional or anonymized resume content.
No real hiring decisions are made.
Collected data is used solely for educational and research purposes.


## Relevance for Industry

This project is relevant for roles involving:

systems analysis and design

business or product analytics

human-centered AI and governance

decision-support and transparency tooling

It demonstrates the ability to design, implement, and explain systems that have real human impact.


## Project Status

Work-in-progress prototype developed for an academic Human–Computer Interaction course and poster submission.

