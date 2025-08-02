import streamlit as st
import pandas as pd
from datetime import datetime
from src.agent import WaterIntakeAgent
from src.database import log_intake,get_intake_history

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

# Welcome section

if not st.session_state.tracker_started:
    st.title("Welcome To AI Water Tracker")
    st.markdown("""
    Track your daily hydration with help of AI assistant
    log your intake, get smart feedback and stay healthy effortlessy
                
    """)
    if st.button("Start Tracking"):
        st.session_state.tracker_started = True
        st.experimental_rerun()
else:
    st.title("AI Water Tracker Dashboard")

    #sidebar: Intake Input
    st.sidebar.header("Log Your Water Intake")
    user_id = st.sidebar.text_input("User ID",value="skouza")
    intake_ml = st.sidebar.number_input("Water Intake (ml)",min_value=0,step=100)

    if st.sidebar.button("Submit"):
        if user_id and intake_ml:
            log_intake(user_id,intake_ml)
            st.success(f"logged {intake_ml}ml for {user_id}")

            agent = WaterIntakeAgent()
            feedback = agent.analyze_intake(intake_ml)
            st.info(f"AI Feedback: {feedback}")

    # divider
    st.markdown("---")

    # History Section
    st.header("Water Intake History")

    if user_id:
        history = get_intake_history(user_id)
        if history:
            dates = [datetime.strptime(row[1],"%Y-%m-%d") for row in history]
            values = [row[0] for row in history]

            df = pd.DataFrame({
                "Date":dates,
                "Water Intake (ml)":values
            })

            st.dataframe(df)
            st.line_chart(df,x="Date",y="Water Intake (ml)")
        else:
            st.warning("No Water intake data found. Please log your intake first !")

