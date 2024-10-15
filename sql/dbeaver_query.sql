select
	sum("Yards Boyd") "Boyd Yards",
	sum("Yards Higgins") "Higgins Yards",
	sum("Yards Chase") "Chase Yards",
	concat(
		sum(case when "Result" = 'Win' then 1 else 0 end),
		'-',
		sum(case when "Result" = 'Loss' then 1 else 0 end) 
	) "Win/Loss"
from
	public.drew_ringo