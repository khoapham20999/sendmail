import gspread


gc = gspread.service_account(filename='/home/khoa/working/sendmail/labs/abc.json')
sh = gc.open_by_key('1gnr2RJKMyFBof6cDmXJ_7T_ziq628Rg2RcXn9IdVJR0')

worksheet = sh.sheet1

res = worksheet.get_all_records()
print(res)
