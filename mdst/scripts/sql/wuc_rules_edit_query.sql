SELECT left(sub.work_unit_code,3) as WUC,
	count(*) as WUC_Count, 
	round((count(*) /(select count(*) FROM mdst_c130.edit_wuc_level_5 where wuc_rule is not null)), 4) as WUC_Percentile
FROM (SELECT * FROM mdst_c130.edit_wuc_level_5 where wuc_rule is not null) sub 
group by left(sub.work_unit_code,3)
order by count(*) desc;