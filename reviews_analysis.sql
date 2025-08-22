-- Netflix SQL Queries for indepth analysis and insights generation

-- 1. Creating table for storing processed reviews (if not already created)
CREATE TABLE netflix_reviews (
    id INT IDENTITY(1,1) PRIMARY KEY,
    review NVARCHAR(MAX),
    review_cleaned NVARCHAR(MAX),
    rating INT
);

-- 2. Creating index to speed up rating queries
CREATE INDEX idx_rating ON netflix_reviews(rating);

-- 3. Creating table for storing viewing activity
CREATE TABLE netflix_views (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    content_id INT,
    genre NVARCHAR(50),
    view_date DATE,
    watch_time INT
);

-- 4. Query: Top genres by average rating
SELECT genre, AVG(rating) AS avg_rating
FROM netflix_views v
JOIN netflix_reviews r ON v.content_id = r.id
GROUP BY genre
ORDER BY avg_rating DESC;

-- 5. Query: Seasonal viewing trends
SELECT DATENAME(MONTH, view_date) AS month, COUNT(*) AS views
FROM netflix_views
GROUP BY DATENAME(MONTH, view_date), MONTH(view_date)
ORDER BY MONTH(view_date);

-- 6. Query: Sentiment-driven engagement 
SELECT sentiment_score, COUNT(*) AS review_count
FROM netflix_reviews
GROUP BY sentiment_score
ORDER BY review_count DESC;

-- 7. Query: Most engaged users (by watch_time)
SELECT TOP 10 user_id, SUM(watch_time) AS total_watch_time
FROM netflix_views
GROUP BY user_id
ORDER BY total_watch_time DESC;
