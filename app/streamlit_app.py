import streamlit as st
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS

st.title("Body Fat App")

st.write("This app is maintained by STAT-628 Module-2 Group-20 (YUANHAO GENG, JIAYANG WANG, MINGYU WANG and YUXIN ZHAO). If you have any question about this app, please contact us through geng29@wisc.edu.")

st.header("Predict Your Body Fat Now!")

@st.cache
def load_model():
    df = pd.read_csv("../data/cleaned_data.csv")
    Y = df.BODYFAT
    X = df[["ABDOMEN", "FOREARM", "WEIGHT", "WRIST"]]
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    return model.fit()

model_load_state = st.text('Loading model...')
model = load_model()
model_load_state.text("Model Loading Done! (using st.cache)")

txt = "Please slide values according to your abdomen, forearm, weight and wrist information. When the prediction is negative or larger than 50%, warning information will be displayed."
st.markdown("\
<style>\
p.dashed {border-style: dashed;}\
</style>\
", unsafe_allow_html=True)
st.markdown(
    f"<p class='dashed'>{txt}</p>",
    unsafe_allow_html=True
)

abdomen = st.slider("Abdomen 2 Circumference (cm) (laterally, at the level of the iliac crests, and anteriorly, at the umbilicus)", 70.0, 150.0, 110.0)
forearm = st.slider("Forearm Circumference (cm)", 20.0, 35.0, 28.0)
weight = st.slider("Weight (lbs)", 125.0, 365.0, 220.0)
wrist = st.slider("Wrist Circumference (cm)", 15.0, 25.0, 18.0)
bodyfat = model.predict([[1, abdomen, forearm, weight, wrist]])[0]
bodyfat = round(bodyfat, 2)

font_size = 100
if bodyfat < 0:
    bodyfat = "Please Check Your Input! The Prediction is Negative!"
    font_size = 30
elif bodyfat > 50:
    bodyfat = "Please Check Your Input! The Prediction is too Large!"
    font_size = 30
bodyfat = str(bodyfat)
bodyfat += "%"

st.markdown("\
<style>\
.big-font {\
    font-size:%dpx !important;\
}\
</style>\
"%font_size, unsafe_allow_html=True)
st.subheader("Your Body Fat Percentage is")
st.markdown(
    f"<center><p class='big-font'>{bodyfat}</p></center>",
    unsafe_allow_html=True
)
