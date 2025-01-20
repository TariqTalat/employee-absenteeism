-- Select the Reason Count Per Reason:
SELECT 
    'Reason_1' AS Reason_Column, 
    [Reason_1] AS Reason_Value, 
    COUNT(*) AS Reason_Count
FROM AbsenteeismData
GROUP BY [Reason_1]

UNION ALL

SELECT 
    'Reason_2' AS Reason_Column, 
    [Reason_2] AS Reason_Value, 
    COUNT(*) AS Reason_Count
FROM AbsenteeismData
GROUP BY [Reason_2]

UNION ALL

SELECT 
    'Reason_3' AS Reason_Column, 
    [Reason_3] AS Reason_Value, 
    COUNT(*) AS Reason_Count
FROM AbsenteeismData
GROUP BY [Reason_3]

UNION ALL

SELECT 
    'Reason_4' AS Reason_Column, 
    [Reason_4] AS Reason_Value, 
    COUNT(*) AS Reason_Count
FROM AbsenteeismData
GROUP BY [Reason_4]
ORDER BY Reason_Column, Reason_Value;

-- Average Age and Absenteeism by Day of the Week
WITH Daywise_Absenteeism AS (
    SELECT 
        Day_of_the_week, 
        AVG(Age) AS Avg_Age,
        COUNT(*) AS Absenteeism_Count
    FROM AbsenteeismData
    GROUP BY Day_of_the_week
)
SELECT 
    Day_of_the_week, 
    Avg_Age,
    Absenteeism_Count,
    AVG(Absenteeism_Count) OVER () AS Overall_Avg_Absenteeism_Count
FROM Daywise_Absenteeism
ORDER BY Day_of_the_week;

-- Comparison of Absenteeism Across Different Education Levels
WITH Education_Absenteeism AS (
    SELECT 
        Education, 
        COUNT(*) AS Total_Absenteeism,
        AVG([Age]) AS Avg_Age
    FROM AbsenteeismData
    GROUP BY Education
)
SELECT 
    Education, 
    Total_Absenteeism, 
    Avg_Age, 
    AVG(Total_Absenteeism) OVER () AS Overall_Avg_Absenteeism
FROM Education_Absenteeism
ORDER BY Total_Absenteeism DESC;

-- Days Absenteeism
SELECT 
    Day_of_the_week, 
    COUNT(*) AS Absenteeism_Count
FROM AbsenteeismData
GROUP BY Day_of_the_week
ORDER BY Absenteeism_Count DESC;