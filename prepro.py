"""This module helps to preprocess the data."""

# Import necessary modules.
import pandas as pd
import streamlit as st

# Load the dataset.
@st.cache()
def load_data():
    """This function perform preprocessing on dataset and return that"""
    # read the dataset.
    df = pd.read_csv("./car-prices.csv")
    
    # Extract the name of the car manufactures.
    car_companies = pd.Series([car.split(" ")[0] for car in df['CarName']], index = df.index)
    
    # Create new column for car company names.
    df['car_company'] = car_companies

    # Replace the misspelled car company names.
    df.loc[(df['car_company'] == "vw") | (df['car_company'] == "vokswagen"), 'car_company'] = 'volkswagen'
    df.loc[df['car_company'] == "porcshce", 'car_company'] = 'porsche'
    df.loc[df['car_company'] == "toyouta", 'car_company'] = 'toyota'
    df.loc[df['car_company'] == "Nissan", 'car_company'] = 'nissan'
    df.loc[df['car_company'] == "maxda", 'car_company'] = 'mazda'
    df.drop(columns= ['CarName'], axis = 1, inplace = True)
    cars_numeric_df = df.select_dtypes(include = ['int64', 'float64']) 
    cars_numeric_df.drop(columns = ['car_ID'], axis = 1, inplace = True)

    # Map the values for the doornumbers and cylindernumbers.
    df[['cylindernumber', 'doornumber']] = df[['cylindernumber', 'doornumber']].apply(num_map, axis = 1)

    # Create dummy for car_body.
    car_body_dummies = pd.get_dummies(df['carbody'], dtype=int)

    # Create dummy for car_body and drop first column
    car_body_new_dummies = pd.get_dummies(df['carbody'], drop_first=True, dtype=int)

    # Creating a dataframe for non-numerical values.
    car_catagorical_df = df.select_dtypes(include=[object])

    # Get dummy for catagorical columns.
    cars_dummy_df = pd.get_dummies(car_catagorical_df, drop_first=True, dtype=int)

    # Drop catagorical columns from the dataset.
    df.drop(list(car_catagorical_df.columns), axis=1, inplace=True)

    # Concat df with car_dummy_df
    df = pd.concat([df, cars_dummy_df], axis=1)

    # Drop the car_ID.
    df.drop('car_ID', axis=1, inplace=True)

    # Create list of final columns.
    final_col =  ['carwidth','carheight','enginesize','horsepower','peakrpm','wheelbase','curbweight','boreratio','drivewheel_fwd','stroke','compressionratio','citympg','highwaympg','car_company_buick', 'price']

    # Return the processed dataset.
    return df[final_col]

def num_map(series):
    """This function changes nominal data to numerical data."""
    word_dict = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "eight": 8, "twelve": 12}
    return series.map(word_dict)