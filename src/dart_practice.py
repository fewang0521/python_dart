# -*- coding: utf-8 -*-
import dart_fss as dart
api_key='fcb0b5b6663759936ad3c7dbf488b1ead9459fd0'
dart.dart_set_api_key(api_key)
crp_list=dart.get_crp_list()
samsung_electronics=crp_list.find_by_name('삼성전자')[0]
fs_annual = samsung_electronics.get_financial_statement(start_dt='20180101', report_tp='quarter')
print(fs_annual)
