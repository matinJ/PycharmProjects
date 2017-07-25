select *
from (
select client_id, stock_code, sum(case when business_flag='4001' then business_amount else 0 end) s, sum(case when business_flag='4002' then business_amount else 0 end) b
from uf20.deliver
where dw_trade_date between ${hiveconf:start_date} and ${hiveconf:end_date} and stock_type in ('0', 'c') and exchange_type in ('1','2')
and branch_no>1000
group by client_id, stock_code
) t where b<>0 or s<>0