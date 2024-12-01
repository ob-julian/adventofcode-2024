# Advent of Code 2024 - Day 1  
## Language Used: PostgreSQL

### Setup  
To begin, create a new database and set up the required tables and indexes:  

```sql
CREATE DATABASE aoc_2024_day_1;
```

```sql
CREATE TABLE test (
    group_1 INT,
    group_2 INT
);
CREATE INDEX test_group_1_idx ON test (group_1);
CREATE INDEX test_group_2_idx ON test (group_2);
```

```sql
CREATE TABLE input (
    group_1 INT,
    group_2 INT
);
CREATE INDEX input_group_1_idx ON input (group_1);
CREATE INDEX input_group_2_idx ON input (group_2);
```

**Note:** Ensure the numbers in the `.txt` files are separated by commas (`,`) instead of spaces. This allows the data to be imported correctly (e.g., when using Adminer).

---

### Part 1  
```sql
WITH sorted_group_1 AS (
    SELECT group_1, ROW_NUMBER() OVER (ORDER BY group_1) AS rn
    FROM input
),
sorted_group_2 AS (
    SELECT group_2, ROW_NUMBER() OVER (ORDER BY group_2) AS rn
    FROM input
)
SELECT 
    SUM(ABS(g1.group_1 - g2.group_2)) AS result
FROM sorted_group_1 g1
JOIN sorted_group_2 g2 ON g1.rn = g2.rn;
```

**Solution:**  
The result for Part 1 in my case was `2344935`.  

**Explanation:**  
1. I sorted the values in `group_1` and `group_2` and assigned a row number to each entry using `ROW_NUMBER()`.
2. I joined the two sorted groups on their row numbers.
3. Finally, I calculated the sum of the absolute differences between the paired values.

> I used AI to get the Idea of using `ROW_NUMBER()` and its correct implementation.
---

### Part 2  
```sql
SELECT SUM(t1.group_1)
FROM input AS t1
JOIN input ON t1.group_1 = input.group_2;
```

**Solution:**  
The result for Part 2 in my case was `27647262`.  

**Explanation:**  
1. The `input` table is joined with itself. For every value in `group_1`, all matching occurrences in `group_2` are considered.
2. This means each value in `group_1` is effectively multiplied by the number of times it appears in `group_2`.
3. The final sum is calculated from this adjusted dataset.