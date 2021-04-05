CREATE VIEW view_users_status AS
SELECT `Year_Month`, User_ID, Active_From, User_Life_Cycle_Status,
SUM (Elapsed) OVER (PARTITION BY User_ID ORDER BY User_ID, Calendar_Date) AS Lapsed_Months
From (
  SELECT
  	c.year_month as `Year_Month`,
  	c.`date` as Calendar_Date,
  	p.user_id As User_ID,
  	c.month_number As Month_Number,
    CASE
        WHEN strftime("%m", c.`date`) = strftime("%m", p.policy_start_date) Then "-"
        WHEN c.`date` > (select MIN(policy_start_date) from policy WHERE policy.user_id=p.user_id)
        and c.`date` <= (select MAX(policy_end_date) from policy WHERE policy.user_id=p.user_id)
        THEN (Select strftime("%Y-%m", DATE(Min(policy_start_date), "+1 months")) from policy WHERE user_id=p.user_id)
        Else "-"
    END as  Active_From,
    CASE
        WHEN strftime("%m", c.`date`) = strftime("%m", p.policy_start_date) Then "NEW"
        WHEN c.`date` > (select MIN(policy_start_date) from policy WHERE policy.user_id=p.user_id)
        and c.`date` <= (select MAX(policy_end_date) from policy WHERE policy.user_id=p.user_id)  THEN "Active"
        WHEN c.`date` > (select MAX(policy_end_date) from policy WHERE policy.user_id=p.user_id)
        AND c.`date` <= DATE((select MAX(policy_end_date) from policy WHERE policy.user_id=p.user_id), "+1 months") THEN "Churned"
        Else "Lapsed"
    END as User_Life_Cycle_Status,
    CASE
        WHEN c.`date` < DATE((select MAX(policy_end_date) from policy WHERE policy.user_id=p.user_id), "+1 months") THEN 0
        Else 1
    END as Elapsed
    FROM calendar AS c
    JOIN policy AS p ON c.`date` >= p.policy_start_date
    GROUP By c.month_number, p.user_id
    ORDER By p.user_id, c.`date`)
AS SUB_CLAUSE
GROUP By Month_Number, User_ID
ORDER BY User_ID, Calendar_Date