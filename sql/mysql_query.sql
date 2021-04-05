CREATE VIEW view_users_status AS
SELECT `Year_Month`, User_ID, Active_From, User_Life_Cycle_Status,
SUM (Elapsed) OVER (PARTITION BY User_ID ORDER BY User_ID, Calendar_Date) AS Lapsed_Months
FROM
(SELECT
  	c.year_month as `Year_Month`,
  	c.`date` as Calendar_Date,
  	p.user_id As User_ID,
  	c.month_number As Month_Number,
    CASE
        WHEN DATE_FORMAT(c.`date`, "%m") = DATE_FORMAT(p.policy_start_date, "%m") Then "-"
        WHEN c.`date` > (select MIN(policy_start_date) from policy WHERE policy.user_id=p.user_id)
        and c.`date` <= (select MAX(policy_end_date) from policy WHERE policy.user_id=p.user_id)
        THEN (Select DATE_FORMAT(DATE_ADD(Min(policy_start_date), INTERVAL 1 MONTH), "%Y-%m") from policy WHERE user_id=p.user_id)
        Else "-"
    END as  Active_From,
    CASE
        WHEN DATE_FORMAT(c.`date`, "%m") = DATE_FORMAT(p.policy_start_date, "%m") Then "NEW"
        WHEN c.`date` > (select MIN(policy_start_date) from policy WHERE policy.user_id=p.user_id)
        and c.`date` <= (select MAX(policy_end_date) from policy WHERE policy.user_id=p.user_id)  THEN "Active"
        WHEN c.`date` > (select MAX(policy_end_date) from policy WHERE policy.user_id=p.user_id)
        AND c.`date` <= DATE_ADD((select MAX(policy_end_date) from policy WHERE policy.user_id=p.user_id), INTERVAL 1 MONTH) THEN "Churned"
        Else "Lapsed"
    END as User_Life_Cycle_Status,
    CASE
        WHEN c.`date` < DATE_ADD((select MAX(policy_end_date) from policy WHERE policy.user_id=p.user_id), INTERVAL 1 MONTH) THEN 0
        Else 1
    END as Elapsed
    FROM calendar AS c
    JOIN policy AS p ON c.`date` >= p.policy_start_date
    GROUP By c.month_number, p.user_id
    ORDER By p.user_id, c.`date`)
AS MAIN
GROUP By Month_Number, User_ID
ORDER BY User_ID, Calendar_Date