-- Total Customers
SELECT COUNT(*) AS Total_Customers
FROM netflix_churn;

-- Churn Distribution
SELECT Churn,
COUNT(*) AS Total_Customers
FROM netflix_churn GROUP BY Churn;

-- Average Watch Time
SELECT AVG(Daily_Watch_Time) AS Average_Watch_Time
FROM netflix_churn;

-- Average Satisfaction
SELECT AVG(Customer_Satisfaction) AS Average_Satisfaction
FROM netflix_churn;

-- Customers by Subscription Plan
SELECT Subscription_Plan, COUNT(*) AS Customers 
FROM netflix_churn
GROUP BY Subscription_Plan;

-- Customers by Region
SELECT Region,
COUNT(*) AS Customers
FROM netflix_churn
GROUP BY Region;

-- Customers by Device
SELECT Device,
COUNT(*) AS Customers
FROM netflix_churn
GROUP BY Device;