import pyqrcode
import png
from pyqrcode import QRCode
import xlrd
from send import send

def read_file() :
    loc = ("/home/khoa/working/sendmail/list.xls")
    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    lst = []
    for row in range(1, sheet.nrows) :
        qr_code = sheet.cell_value(row, 5)
        email = sheet.cell_value(row,4)
        lst.append([qr_code, email])
    return lst

def make_qr_code(qr_code, image_path) :
    url = pyqrcode.create(qr_code)
    url.png(image_path, scale = 6)

def check() :
    users_info = read_file()
    for user in users_info :
        qr_code = user[0]
        email = user[1]
        name_image = email.split("@")[0]
        # sendemail function
        make_qr_code(qr_code, "/home/khoa/working/sendmail/images/{}.png".format(name_image))
        send(email, name_image)
        # print("Sent mail with user {} with qr code {}".format(name_image, qr_code))

if __name__ == '__main__':
    check()















# print
