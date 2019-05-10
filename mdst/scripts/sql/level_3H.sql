-- level 3H 1
-- 613. AF41-3H-27. WUC BEGINS WITH "41" AND ENDS WITH 000 AND D/C CONTAINS "SME " THEN CHANGE WUC TO 41Y00
SELECT Equipment_Designator, Work_Unit_Code, Corrective_Narrative, Discrepancy_Narrative FROM mdst_c130.import_remis_data
	WHERE Work_Unit_Code LIKE '41%'
	AND Work_Unit_Code LIKE '%000'
    AND (Discrepancy_Narrative LIKE '%SME %'
    OR Corrective_Narrative LIKE '%SME %')
    ;

-- level 3H 2
-- 738. AF41-3H-152. WUC BEGINS WITH "41" AND ENDS WITH 99 AND MDS DOES NOT BEGIN WITH C130J AND DISCREPANCY CONTAINS " BOOT" AND " BLEED" AND DISCREPANCY DOES NOT CONTAIN (" 1C-130H-2-21JG-30-1" OR " 1C-130 H-2-21JG-30-1" OR " 1C-130H-2 -21JG-30-1" OR " 1C-130H -2-21JG-30-1") OR " 1C-130H-2-26GS-00-1" OR " 1C-130H-2-30JG-00-1OBSERVE" OR " 1C-130J-23" OR " 21-21-03" OR (" 517TAG" OR " 517 TAG") OR (" AC-130W" OR " AC 130W" OR " AC130W") OR (" AC130U25MM" OR " AC130U 25MM") OR (" AC130UELCTRO-ENVIRONMENTAL" OR " AC130U ELCTRO-ENVIRONMENTAL" OR " AC130UELCTRO ENVIRONMENTAL" OR " AC130U ELCTRO ENVIRONMENTAL" OR " AC130UELCTROENVIRONMENTAL" OR " AC130U ELCTROENVIRONMENTAL") OR (" ANALYZERTRIMMER" OR " ANALYZER TRIMMER") OR (" ANTI-ICING" OR " ANTI ICING" OR " ANTIICING") OR (" ANTI-ICINGSYSTEM.*IAW" OR " ANTI ICINGSYSTEM.*IAW" OR " ANTIICINGSYSTEM.*IAW") OR (" BASELEADING" OR " BASE LEADING") OR (" BLANKETSHALL" OR " BLANKET SHALL") OR (" BLOWERLIGHT" OR " BLOWER LIGHT") OR " C130J" OR " CARGO" OR " CHAMBER" OR (" COOLINGFAN" OR " COOLING FAN") OR " DECK" OR (" DETECTORTHERMOSTATAFTER" OR " DETECTOR THERMOSTATAFTER") OR (" DETECTORTHERMOSTATFOR" OR " DETECTOR THERMOSTATFOR") OR " DUCT" OR " EC130H" OR (" ELECTRO-ENVIRONMENTAL" OR " ELECTRO ENVIRONMENTAL" OR " ELECTROENVIRONMENTAL") OR " ENGINE" OR (" FLOORHANDLE" OR " FLOOR HANDLE") OR (" FLOWPUMP" OR " FLOW PUMP") OR " FREEDOM" OR (" GAPURGE" OR " GA PURGE") OR " H-2-21JG-21-1.OBSERVE" OR " H-2-21JG-80-1" OR " HEAT" OR " ICE" OR " L.THOMA" OR (" LCPUMP" OR " LC PUMP") OR (" MC130HMC-130H" OR " MC130H MC-130H" OR " MC130HMC 130H" OR " MC130H MC 130H" OR " MC130HMC130H" OR " MC130H MC130H") OR " NESA" OR " OBE" OR " OUTFLOW" OR (" PITOTSTATIC" OR " PITOT STATIC") OR " PRESS" OR (" PRESSURE" OR " PRESS URE") OR " PRESSURIZATION" OR " PROP" OR (" RADARCOOLANT" OR " RADAR COOLANT") OR " SAFETY" OR " SAMPLING" OR (" SEPARATOR" OR " SEP ARATOR") OR " SEPERATOR" OR " SHADOW" OR " SME" OR " SOCK" OR (" V-BAND" OR " V BAND" OR " VBAND") THEN CHANGE WUC TO 41400
SELECT Equipment_Designator, Work_Unit_Code, Corrective_Narrative, Discrepancy_Narrative FROM mdst_c130.import_remis_data
	WHERE Work_Unit_Code LIKE '41%'
	AND Work_Unit_Code LIKE '%99'
    AND Equipment_Designator NOT LIKE 'C130J%'
    AND (Discrepancy_Narrative LIKE "% BOOT%" AND Discrepancy_Narrative LIKE "% BLEED%" AND
    (
		(Discrepancy_Narrative NOT LIKE "% 1C-130H-2-21JG-30-1%%" OR Discrepancy_Narrative NOT LIKE "% 1C-130 H-2-21JG-30-1%%" OR Discrepancy_Narrative NOT LIKE "% 1C-130H-2 -21JG-30-1%%" OR Discrepancy_Narrative NOT LIKE "% 1C-130H -2-21JG-30-1%%")
        OR Discrepancy_Narrative NOT LIKE "% 1C-130H-2-26GS-00-1%"
        OR Discrepancy_Narrative NOT LIKE "% 1C-130H-2-30JG-00-1OBSERVE%"
        OR Discrepancy_Narrative NOT LIKE "% 21-21-03%" 
        OR Discrepancy_Narrative NOT LIKE "% 21-21-03%"
        OR (Discrepancy_Narrative NOT LIKE "% 517TAG%%" OR Discrepancy_Narrative NOT LIKE "% 517 TAG%%") 
        OR (Discrepancy_Narrative NOT LIKE "% AC-130W%%" OR Discrepancy_Narrative NOT LIKE "% AC 130W%%" OR Discrepancy_Narrative NOT LIKE "% AC130W%%") 
        OR (Discrepancy_Narrative NOT LIKE "% AC130U25MM%%" OR Discrepancy_Narrative NOT LIKE "% AC130U 25MM%")
        OR (Discrepancy_Narrative NOT LIKE "% AC130UELCTRO-ENVIRONMENTAL%" OR Discrepancy_Narrative NOT LIKE "% AC130U ELCTRO-ENVIRONMENTAL%" OR Discrepancy_Narrative NOT LIKE "% AC130UELCTRO ENVIRONMENTAL%" OR Discrepancy_Narrative NOT LIKE "% AC130U ELCTRO ENVIRONMENTAL%" OR Discrepancy_Narrative NOT LIKE "% AC130UELCTROENVIRONMENTAL%" OR Discrepancy_Narrative NOT LIKE "% AC130U ELCTROENVIRONMENTAL%")
        OR (Discrepancy_Narrative NOT LIKE "% ANALYZERTRIMMER%" OR Discrepancy_Narrative NOT LIKE "% ANALYZER TRIMMER%")
        OR (Discrepancy_Narrative NOT LIKE "% ANTI-ICING%" OR Discrepancy_Narrative NOT LIKE "% ANTI ICING%" OR Discrepancy_Narrative NOT LIKE "% ANTIICING%")
        OR (Discrepancy_Narrative NOT LIKE "% ANTI-ICINGSYSTEM.*IAW%" OR Discrepancy_Narrative NOT LIKE "% ANTI ICINGSYSTEM.*IAW%" OR Discrepancy_Narrative NOT LIKE "% ANTIICINGSYSTEM.*IAW%")
        OR (Discrepancy_Narrative NOT LIKE "% ANTI-ICING%" OR Discrepancy_Narrative NOT LIKE "% ANTI ICING%" OR Discrepancy_Narrative NOT LIKE "% ANTIICING%")
        OR (Discrepancy_Narrative NOT LIKE "% ANTI-ICINGSYSTEM.*IAW%" OR Discrepancy_Narrative NOT LIKE "% ANTI ICINGSYSTEM.*IAW%" OR Discrepancy_Narrative NOT LIKE "% ANTIICINGSYSTEM.*IAW%") 
		OR (Discrepancy_Narrative NOT LIKE "% BASELEADING%" OR Discrepancy_Narrative NOT LIKE "% BASE LEADING%")
        OR (Discrepancy_Narrative NOT LIKE "% BLANKETSHALL%" OR Discrepancy_Narrative NOT LIKE "% BLANKET SHALL%")
        OR (Discrepancy_Narrative NOT LIKE "% BLOWERLIGHT%" OR Discrepancy_Narrative NOT LIKE "% BLOWER LIGHT%") 
		OR Discrepancy_Narrative NOT LIKE "% C130J%" 
		OR Discrepancy_Narrative NOT LIKE "% CARGO%" 
        OR Discrepancy_Narrative NOT LIKE "% CHAMBER%" 
        OR (Discrepancy_Narrative NOT LIKE "% COOLINGFAN%" OR Discrepancy_Narrative NOT LIKE "% COOLING FAN%") 
        OR Discrepancy_Narrative NOT LIKE "% DECK%" 
        OR (Discrepancy_Narrative NOT LIKE "% DETECTORTHERMOSTATAFTER%" OR Discrepancy_Narrative NOT LIKE "% DETECTOR THERMOSTATAFTER%") 
		OR (Discrepancy_Narrative NOT LIKE "% DETECTORTHERMOSTATFOR%" OR Discrepancy_Narrative NOT LIKE "% DETECTOR THERMOSTATFOR%") 
        OR Discrepancy_Narrative NOT LIKE "% DUCT%" 
        OR Discrepancy_Narrative NOT LIKE "% EC130H%" 
        OR (Discrepancy_Narrative NOT LIKE "% ELECTRO-ENVIRONMENTAL%" OR Discrepancy_Narrative NOT LIKE "% ELECTRO ENVIRONMENTAL%" OR Discrepancy_Narrative NOT LIKE "% ELECTROENVIRONMENTAL%") 
        OR Discrepancy_Narrative NOT LIKE "% ENGINE%" 
        OR (Discrepancy_Narrative NOT LIKE "% FLOORHANDLE%" OR Discrepancy_Narrative NOT LIKE "% FLOOR HANDLE%") 
        OR (Discrepancy_Narrative NOT LIKE "% FLOWPUMP%" OR Discrepancy_Narrative NOT LIKE "% FLOW PUMP%") 
		OR Discrepancy_Narrative NOT LIKE "% FREEDOM" 
        OR (Discrepancy_Narrative NOT LIKE "% GAPURGE%" OR Discrepancy_Narrative NOT LIKE "% GA PURGE%") 
        OR Discrepancy_Narrative NOT LIKE "% H-2-21JG-21-1.OBSERVE%" 
        OR Discrepancy_Narrative NOT LIKE "% H-2-21JG-80-1%" 
        OR Discrepancy_Narrative NOT LIKE "% HEAT%" 
        OR Discrepancy_Narrative NOT LIKE "% ICE%" 
        OR Discrepancy_Narrative NOT LIKE "% L.THOMA%" 
		OR (Discrepancy_Narrative NOT LIKE "% LCPUMP%" OR Discrepancy_Narrative NOT LIKE "% LC PUMP%") 
        OR (Discrepancy_Narrative NOT LIKE "% MC130HMC-130H%" OR Discrepancy_Narrative NOT LIKE "% MC130H MC-130H%" OR Discrepancy_Narrative NOT LIKE "% MC130HMC 130H%" OR Discrepancy_Narrative NOT LIKE "% MC130H MC 130H%" OR Discrepancy_Narrative NOT LIKE "% MC130HMC130H%" OR Discrepancy_Narrative NOT LIKE "% MC130H MC130H%") 
        OR Discrepancy_Narrative NOT LIKE "% NESA%" 
        OR Discrepancy_Narrative NOT LIKE "% OBE%" 
        OR Discrepancy_Narrative NOT LIKE "% OUTFLOW%" 
        OR (Discrepancy_Narrative NOT LIKE "% PITOTSTATIC%" OR Discrepancy_Narrative NOT LIKE "% PITOT STATIC%") 
        OR Discrepancy_Narrative NOT LIKE "% PRESS%" 
		OR (Discrepancy_Narrative NOT LIKE "% PRESSURE%" OR Discrepancy_Narrative NOT LIKE "% PRESS URE%") 
        OR Discrepancy_Narrative NOT LIKE "% PRESSURIZATION%" 
        OR Discrepancy_Narrative NOT LIKE "% PROP%" 
        OR (Discrepancy_Narrative NOT LIKE "% RADARCOOLANT%" OR Discrepancy_Narrative NOT LIKE "% RADAR COOLANT%") 
		OR Discrepancy_Narrative NOT LIKE "% SAFETY%" 
        OR Discrepancy_Narrative NOT LIKE "% SAMPLING%" 
        OR (Discrepancy_Narrative NOT LIKE "% SEPARATOR%" OR Discrepancy_Narrative NOT LIKE "% SEP ARATOR%") 
        OR Discrepancy_Narrative NOT LIKE "% SEPERATOR%" 
        OR Discrepancy_Narrative NOT LIKE "% SHADOW%" 
        OR Discrepancy_Narrative NOT LIKE "% SME%" 
        OR Discrepancy_Narrative NOT LIKE "% SOCK%" 
    ))
	;

-- level 3H 3
-- 41. AF11-3H-41. WUC BEGINS WITH "11" AND ENDS WITH "000" AND D/C CONTAINS ("146-176.NOTE" OR "146176.NOTE") THEN CHANGE WUC TO 11L00
SELECT Equipment_Designator, Work_Unit_Code, Corrective_Narrative, Discrepancy_Narrative FROM mdst_c130.import_remis_data
	WHERE Work_Unit_Code LIKE '11%'
	AND Work_Unit_Code LIKE '%000'
    AND (
		(Discrepancy_Narrative LIKE '%146-176.NOTE%' OR Corrective_Narrative LIKE '%146-176.NOTE%') 
        OR (Discrepancy_Narrative LIKE '%146176.NOTE%' OR Corrective_Narrative LIKE '%146176.NOTE%')
        )
    ;