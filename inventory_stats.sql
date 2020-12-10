with inventory_left (product_id, fyear, product_name, inventory_remaining,year_rank) as 
(select fr.pid,fr.pyear,fr.product_name,id.quantity-fr.qty_total as inventory_remaining,1 as year_rank
from final_report fr
inner join inventory_data id
on fr.pid=id.product_id and
fr.pyear=id.year
union all
select fr.pid,fr.pyear,fr.product_name,ir.inventory_remaining-fr.qty_total,fr.year_rank
from (select pid,product_name, pyear,qty_total, rank() over (partition by pid order by pyear asc) as year_rank
from final_report) fr inner join inventory_left ir
on fr.pid=ir.product_id and
fr.year_rank = ir.year_rank+1)
select *
from inventory_left;