from quickstart import GoogleSheet
from verify_pass import no_ssl_verification
import click_house_query as chq
import json
from decimal import Decimal



def main():
    item = chq.ch_query("""select
                        toYYYYMM(ch.close_date) as ch_date,
                        --ch.form_id as form_id,
                        --max(ch.form_name) as form_name,
                        sum(if((ch.card_id > 0) and (ch.ch_type = 1), 1, 0)) as ch_cnt_kopilka,
                        sum(if(ch.ch_type = 1, 1, 0)) as ch_cnt,
                        sum(if(ch.ch_type = 1, ch.ch_str_cnt, 0)) as ch_str_cnt,
                        sum(if(ch.ch_type = 1, ch_str_cnt_kopilka, 0)) as ch_str_cnt_kopilka,
                        sum(if(ch.card_id > 0, ch.ch_sum, 0)) as ch_sum_kopilka,
                        sum(ch.ch_sum) as ch_sum,
                        sum(ch.ch_sum_wo_nds) as ch_sum_wo_nds,
                        sum(if(ch.card_id > 0, ch.ch_sum, 0)) / sum(if((ch.card_id > 0) and (ch.ch_type = 1), 1, 0)) as ch_sum_mid_kopilka,
                        sum(ch.ch_sum) / sum(if(ch.ch_type = 1, 1, 0)) as ch_sum_mid
                    from (
                        select
                            chl.shift_id,
                            chl.check_id,
                            chl.close_date,
                            max(chl.check_type) as ch_type,
                            max(chl.kopilka_card_id) as card_id,
                            max(chl.format_id) as form_id,
                            --max(csf.format_name) as form_name,
                            count(1) as ch_str_cnt,
                            sum(if(chl.kopilka_card_id > 0, 1, 0)) as ch_str_cnt_kopilka,
                            sum(chl.base_sum) as ch_sum,
                            sum(chl.base_sum - chl.base_sum_vat) as ch_sum_wo_nds
                        from bi.dm_checkline chl
                        inner join bi.cat_store csf on csf.store_id = chl.store_id
                        where chl.close_date BETWEEN '2022-04-01 00:00:00' AND '2022-04-30 23:59:59'
                        /*and csf.region in (
                                    --'Красноярский край'
                                    --'Республика Хакасия'
                                    --'Республика Тыва'
                                    --'Иркутская область'
                                    --'Кемеровская область'	
                            )*/
                        group by chl.shift_id, chl.check_id, chl.close_date
                    ) ch
                    group by toYYYYMM(ch.close_date)--, ch.form_id
                    order by ch_date--, form_id
                    """)
    print(item[0])
    sheet = GoogleSheet()
    json_data = []
    for i in item[0]:
        json_data.append(json.dumps(i, ensure_ascii=False, default=float))
    
    sheet.sendData(json_data)


with no_ssl_verification():
    if __name__ == "__main__":
        main()