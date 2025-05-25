# All-in-One Calculator App using Streamlit
import streamlit as st
import math
import datetime
import numpy as np
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="All-in-One Calculator", layout="wide")
st.title("🧮 All-in-One Calculator App")

with st.sidebar:
    option = st.selectbox("Choose a Calculator", [
        "Basic Calculator", "Scientific Calculator", "BMI Calculator",""
        "Age Calculator", "Loan EMI Calculator", "Currency Converter (Static)",
        "Unit Converter", "Date Calculator", "Tip Calculator", "GST Calculator"
    ])

# -------- BASIC CALCULATOR --------
if option == "Basic Calculator":
    st.header("Basic Calculator")
    num1 = st.number_input("Enter first number")
    num2 = st.number_input("Enter second number")
    operation = st.selectbox("Choose operation", ["Add", "Subtract", "Multiply", "Divide","Modular","Power","Square root","Square","Cube","LMC","HCF"])

    if operation == "Add":
        st.success(f"Result: {num1 + num2}")
    elif operation == "Subtract":
        st.success(f"Result: {num1 - num2}")
    elif operation == "Multiply":
        st.success(f"Result: {num1 * num2}")
    elif operation == "Divide":
        if num2 != 0:
            st.success(f"Result: {num1 / num2}")
        else:
            st.error("Cannot divide by zero")
    elif operation =="Modular":
        st.success(f"Result: {int(num1) % int(num2)}")
    elif operation == "Power":
        st.success(f"Result: {num1 ** num2}")
    elif operation == "Square root":
        st.success(f"Result: {math.sqrt(num1)}")
    elif operation == "Square":
        st.success(f"Result: {num1 ** 2}")
    elif operation == "Cube":
        st.success(f"Result: {num1 ** 3}")
    elif operation == "LMC":
        st.success(f"Result: {math.lcm(int(num1), int(num2))}")
    elif operation == "HCF":
        st.success(f"Result: {math.gcd(int(num1), int(num2))}")
        

# -------- SCIENTIFIC CALCULATOR --------
elif option == "Scientific Calculator":
    st.header("Scientific Calculator")
    expression = st.text_input("Enter expression (e.g., sin(30), log(100), sqrt(16),log(10),sqrt(5),lcm(10,2),hcf(10,2))")
    try:
        result = eval("math." + expression)
        st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")

# -------- BMI CALCULATOR --------
elif option == "BMI Calculator":
    st.header("BMI Calculator")
    weight = st.number_input("Weight (kg)", min_value=1.0)
    height = st.number_input("Height (cm)", min_value=1.0)
    if st.button("Calculate BMI"):
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        st.success(f"Your BMI is {bmi:.2f}")

# -------- AGE CALCULATOR --------
elif option == "Age Calculator":
    st.header("Age Calculator")
    dob = st.date_input("Enter your date of birth")
    today = datetime.date.today()
    delta = relativedelta(today, dob)
    st.info(f"You are {delta.years} years, {delta.months} months, and {delta.days} days old.")

# -------- LOAN EMI CALCULATOR --------
elif option == "Loan EMI Calculator":
    st.header("Loan EMI Calculator")
    P = st.number_input("Loan Amount", min_value=1000.0)
    R = st.number_input("Annual Interest Rate (%)", min_value=0.1) / 12 / 100
    N = st.number_input("Tenure (in months)", min_value=1.0)
    emi = P * R * ((1 + R) ** N) / (((1 + R) ** N) - 1)
    st.success(f"Your EMI is ₹{emi:.2f}")

# -------- CURRENCY CONVERTER (STATIC) --------
elif option == "Currency Converter (Static)":
    st.header("Currency Converter")
    amount = st.number_input("Amount in USD")
    rates = {"INR": 83.2, "EUR": 0.92, "GBP": 0.79}
    target = st.selectbox("Convert to", list(rates.keys()))
    st.success(f"Converted amount: {amount * rates[target]:.2f} {target}")

# -------- UNIT CONVERTER --------
elif option == "Unit Converter":
    st.header("Unit Converter")
    category = st.selectbox("Select Category", ["Length (m to km)", "Weight (kg to lb)", "Temperature (C to F)"])
    value = st.number_input("Enter value")
    if category == "Length (m to km)":
        st.success(f"{value} m = {value/1000} km")
    elif category == "Weight (kg to lb)":
        st.success(f"{value} kg = {value*2.20462:.2f} lb")
    elif category == "Temperature (C to F)":
        st.success(f"{value} °C = {(value * 9/5) + 32:.2f} °F")

# -------- DATE CALCULATOR --------
elif option == "Date Calculator":
    st.header("Date Calculator")
    d1 = st.date_input("Start Date")
    d2 = st.date_input("End Date")
    st.success(f"Days between: {(d2 - d1).days} days")

# -------- TIP CALCULATOR --------
elif option == "Tip Calculator":
    st.header("Tip Calculator")
    bill = st.number_input("Bill Amount")
    tip_percent = st.slider("Tip %", 0, 100, 15)
    tip = bill * tip_percent / 100
    st.success(f"Tip: ₹{tip:.2f}, Total: ₹{bill + tip:.2f}")

# -------- GST CALCULATOR --------
elif option == "GST Calculator":
    st.header("GST Calculator")
    price = st.number_input("Original Price")
    gst_percent = st.slider("GST %", 0, 50, 18)
    gst_amount = price * gst_percent / 100
    total_price = price + gst_amount
    st.success(f"GST Amount: ₹{gst_amount:.2f}, Final Price: ₹{total_price:.2f}")
