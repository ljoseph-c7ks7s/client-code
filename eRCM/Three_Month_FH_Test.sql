SET @tn = '5700001419', @win = '2014-12';

SELECT avg(sub.Flying_Hours) as average FROM
	(SELECT Serial_Number, Mission_Number, Depart_Date, Land_Date, Flying_Hours,
		concat(year(DATE_SUB(Depart_Date, Interval 2 month)), '-', month(DATE_SUB(Depart_Date, Interval 2 month)))  as W1,
		concat(year(DATE_SUB(Depart_Date, Interval 1 month)), '-', month(DATE_SUB(Depart_Date, Interval 1 month))) as W2,
		concat(year(DATE_SUB(Depart_Date, Interval 0 month)), '-', month(DATE_SUB(Depart_Date, Interval 0 month))) as W3
		FROM ercm_kc135.compiled_sortie_history_data 
		WHERE Depart_Date >= '2014-04-09'
		) sub
    where (sub.W1 = @win OR sub.W2 = @win OR sub.W3 = @win);
    # and WHERE sub.Serial_Number = @tn

