-- Пройдено км за все время
select recorded_at,
    SUM(kilocalories) OVER (
        ORDER BY recorded_at
    ) AS total_kilocalories
from fitness_data
ORDER BY recorded_at;
-- 
-- Трата килокалорий по часам
SELECT date_trunc('hour', recorded_at) AS hour_start,
    SUM(kilocalories) AS total_kilocalorie
FROM fitness_data
GROUP BY date_trunc('hour', recorded_at)
ORDER BY hour_start;
-- 
-- Количество разной активности
select type_name,
    count(*)
from fitness_data
    join activity_types on activity_types.id = fitness_data.activity_type_id
group by type_name;