SELECT VERSION();
CREATE DATABASE customerpulse;
use customerpulse;
CREATE TABLE customer_data(
    Customer_ID VARCHAR(20),
    Subscription_Length INT,
    Customer_Satisfaction INT,
    Daily_Watch_Time DECIMAL(4,2),
    Engagement_Rate INT,
    Device VARCHAR(50),
    Genre VARCHAR(50),
    Region VARCHAR(50),
    Payment_History VARCHAR(30),
    Subscription_Plan VARCHAR(30),
    Churn VARCHAR(10),
    Support_Queries INT,
    Age INT,
    Monthly_Income DECIMAL(10,2),
    Promotional_Offers INT,
    Profiles_Created INT,
    Days_Since_Last_Activity INT
);

CREATE TABLE prediction_history (

    Prediction_ID INT AUTO_INCREMENT PRIMARY KEY,

    Customer_Name VARCHAR(100),

    Subscription_Length INT,

    Customer_Satisfaction INT,

    Daily_Watch_Time DECIMAL(4,2),

    Engagement_Rate INT,

    Device VARCHAR(50),

    Genre VARCHAR(50),

    Region VARCHAR(50),

    Payment_History VARCHAR(30),

    Subscription_Plan VARCHAR(30),

    Support_Queries INT,

    Age INT,

    Monthly_Income DECIMAL(10,2),

    Promotional_Offers INT,

    Profiles_Created INT,

    Days_Since_Last_Activity INT,

    Predicted_Churn VARCHAR(20),

    Prediction_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE reminders (

    Reminder_ID INT AUTO_INCREMENT PRIMARY KEY,

    Customer_Name VARCHAR(100),

    Reminder_Date DATE,

    Reminder_Type VARCHAR(50),

    Priority VARCHAR(20),

    Status VARCHAR(20) DEFAULT 'Pending',

    Notes TEXT

);

SHOW TABLES;
