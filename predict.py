"""This create prediction page"""

# Import necessary module
from math import sqrt
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_log_error, mean_squared_error

def app(df):
    # Use markdown to give title
    st.markdown("<p style='color:yellow; font-size: 30px'>This app uses <b>Lasso regression</b> to predict the price of a car based on your inputs.</p>", unsafe_allow_html=True)

    # Create a section for user to input data.
    st.header("Select Values:")
    
    # Create sliders.
    car_width = st.slider("Car Width", float(df["carwidth"].min()), float(df["carwidth"].max()))
    car_height = st.slider("Car Height", float(df["carheight"].min()), float(df["carheight"].max()))
    engine_size = st.slider("Engine Size", float(df["enginesize"].min()), float(df["enginesize"].max()))
    horse_power = st.slider("Horse Power", float(df["horsepower"].min()), float(df["horsepower"].max()))
    peakrpm = st.slider("Peak RPM", int(df["peakrpm"].min()), int(df["peakrpm"].max()))
    wheelbase = st.slider("Wheel Base", int(df["wheelbase"].min()), int(df["wheelbase"].max()))
    curbweight = st.slider("Curb Weight", int(df["curbweight"].min()), int(df["curbweight"].max()))
    boreratio = st.slider("Bore Ratio", int(df["boreratio"].min()), int(df["boreratio"].max()))
    stroke = st.slider("Stroke", int(df["stroke"].min()), int(df["stroke"].max()))
    compressionratio = st.slider("Compression Ratio", int(df["compressionratio"].min()), int(df["compressionratio"].max()))
    citympg = st.slider("City Milage", int(df["citympg"].min()), int(df["citympg"].max()))
    highwaympg = st.slider("Highway Milage", int(df["highwaympg"].min()), int(df["highwaympg"].max()))
    # Creat two radio selection for 0 1 input.
    drivewheel_fwd = st.radio("Is if forward drive wheel car?", ("Yes", "No"))
    car_company_buick = st.radio("Is the car manufactured by Buick?", ("Yes", "No"))

    # Modify radio data.
    if (drivewheel_fwd == "Yes"):
        drivewheel_fwd = 1;
    else:
        drivewheel_fwd = 0;
    
    if (car_company_buick == "Yes"):
        car_company_buick = 1;
    else:
        car_company_buick = 0;

    # Create a list of all input.
    feature_list = [[car_width,car_height, engine_size, horse_power,peakrpm, wheelbase,citympg,highwaympg,compressionratio,stroke,boreratio,curbweight, drivewheel_fwd, car_company_buick]]
    
    # Create a button to predict.
    if st.button("Predict"):
        # Get the all values from predict funciton.
        score, pred_price = predict(df, feature_list)

        # Display all the values.
        st.success(f"The predicted price of the car: Rs.{int(pred_price):,}")
        st.info(f"Accuracy score of this model is: {score:.2%}")
       
       
@st.cache()
def predict(df, feature_list):
    # Create feature and target variable
    X = df.iloc[:, :-1]
    y = df["price"]

    # Split the data in train test.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Create the regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Store score and predicted price in a variable.
    score = model.score(X_train, y_train)
    pred_price = model.predict(feature_list)
    pred_price = pred_price[0]

    # Calculate statical data from the model.
    y_test_pred = model.predict(X_test)
   
   #lasso value
    k = -0000.1
    # Return the values.
    return score, pred_price*k

