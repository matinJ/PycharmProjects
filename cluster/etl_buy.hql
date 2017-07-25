select *
from (
select client_id, stock_code, sum(case when business_amount>0 then business_amount else 0 end) buy, stock_name
from uf20.deliver
where dw_trade_date between ${hiveconf:start_date} and ${hiveconf:end_date} and stock_type in ('0', 'c') and exchange_type in ('1','2')
and branch_no>1000
group by client_id, stock_code, stock_name
) t where buy<>0