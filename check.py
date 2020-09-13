import pyqrcode
import png
from pyqrcode import QRCode
import xlrd
from send import send
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image, ImageDraw, ImageFilter

"""
For insert image to another image:
    https://note.nkmk.me/en/python-pillow-paste/
    https://www.geeksforgeeks.org/working-images-python/

For check installed packages, remove installed packages:
    https://note.nkmk.me/en/python-pillow-basic/
        pip show Pillow

For PIL to work:
    easy_install PILLOW

Insert text into image
    https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil

"""
# define constant 

DEFAULT_PATH = './images/'
FULL_PATH_TICKET_FILE = DEFAULT_PATH + 'e_ticket.png'   # template of ticket

def read_gsheet_to_sent_ticket(): # list user to send - pail = YES and send_ticket = NO
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
        ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheetRegisteredUser = client.open("List of registered user").sheet1


    lst = []
    # for i in range(1,10) : 
    n=2
    while n < 10 : 
        # user_info = sheetRegisteredUser.row_values(n)
        # RegisteredUsers_Paid = user_info[8]
        # RegisteredUsers_SentTicket = user_info[9] 
        # # print(RegisteredUsers_Paid, RegisteredUsers_SentTicket)
        # if RegisteredUsers_Paid == "Y" and  RegisteredUsers_SentTicket == "N" and len(user_info) == 10 : 
        #     RegisteredUsers_FullNames = user_info[1]
        #     RegisteredUsers_Emails = user_info[4]
        #     RegisteredUsers_Codes = user_info[5]  
        #     RegisteredUsers_Full_Codes = user_info[6]
        #     lst.append([RegisteredUsers_Codes, RegisteredUsers_Emails, RegisteredUsers_FullNames, RegisteredUsers_Full_Codes])
        # n +=1 
        user_info = sheetRegisteredUser.row_values(n)
        RegisteredUsers_Paid = user_info[8]
        RegisteredUsers_SentTicket = user_info[9] 
        # print(RegisteredUsers_Paid, RegisteredUsers_SentTicket)
        if RegisteredUsers_Paid == "Y" and  RegisteredUsers_SentTicket == "N" and len(user_info) == 10 : 
            RegisteredUsers_FullNames = user_info[1]
            RegisteredUsers_Emails = user_info[4]
            RegisteredUsers_Codes = user_info[5]  
            RegisteredUsers_Full_Codes = user_info[6]
            # print(RegisteredUsers_Codes + " --- " + RegisteredUsers_Emails + " --- " + RegisteredUsers_FullNames + " --- " + RegisteredUsers_Full_Codes)
            lst.append([RegisteredUsers_Codes, RegisteredUsers_Emails, RegisteredUsers_FullNames, RegisteredUsers_Full_Codes])
        n +=1 
    return lst 

def make_qr_code(sShortCode, sFullCode) :
    #sShortCode is utilized to create file name
    #sFullCode is utilized to create QRCode

    sQRCodeFile = DEFAULT_PATH + 'QRCode_' + sShortCode + '.png'
    url = pyqrcode.create(sFullCode, encoding = 'utf-8')
    url.png(sQRCodeFile, scale=10)

def add_image(sFullPathTicket, sFullPathQRCode, sFinalImageName) : # insert QRcode image to the ticket
    imgTicket = Image.open(sFullPathTicket)
    imgQR_code = Image.open(sFullPathQRCode).resize((518,518))  # need to resize because size of QR Code image depend on length of Code.

    back_im = imgTicket.copy()
    back_im.paste(imgQR_code, (102, 102))

    sFullPathFinalImageFile = DEFAULT_PATH + sFinalImageName

    back_im.save(sFullPathFinalImageFile, quality=95)

def add_text(sFullPathTicketFile, sText, sFinalImageName) :
    from PIL import Image, ImageDraw, ImageFont

    imgTicket = Image.open(sFullPathTicketFile)
    draw = ImageDraw.Draw(imgTicket)
    font = ImageFont.truetype("JetBrainsMono-Bold.ttf", 35)
    sName = sText

    # Get Left Align for sName: supposed that 32 characters/letters fit the width of the ticket.
    if len(sName) > 27:     # supposed that 27 words fit to the box
        arrNames = sName.split(" ")
        sName = arrNames[len(arrNames)-2] + ' ' + arrNames[len(arrNames)-1]
    nLeftAlign = (32 - len(sName))/2

    draw.text((nLeftAlign*22, 675), sName,(255,255,255),font=font)
    imgTicket.save(DEFAULT_PATH + sFinalImageName)

def generate_ticket(sShortCode, sFullCode, sFullName) :
    #Review Gsheet "List of registered user":
        # ShortCode is utilized to create file name of QRCode_image, name of specific user's ticket
        # FullCode i sutilized to generate QRCode.
    make_qr_code(sShortCode, sFullCode) # generate <sShortCode>.png in DEFAULT_PATH

    sTempFileName = 'temp.png'
    sQRCodeFile = DEFAULT_PATH + 'QRCode_' + sShortCode + '.png'
    add_image(FULL_PATH_TICKET_FILE, sQRCodeFile, sTempFileName) # add QRCode image to ticket image -> final image temp.png in DEFAULT_PATH

    sTicket_with_QRCodeFile = DEFAULT_PATH + sTempFileName
    sFinalImageName = sShortCode + '.png'
    add_text(sTicket_with_QRCodeFile, sFullName, sFinalImageName)  # add <sFullName> to image of Ticket_with_QRCode


def main() :
    users_info = read_gsheet_to_sent_ticket()
    for user in users_info :
        qr_code = user[0]
        email = user[1]
        full_name = user[2]
        full_code = user[3]
        name_image = qr_code + '.png'
        # sendemail function
        # make_qr_code(qr_code, "/home/khoa/working/sendmail/images/{}.png".format(name_image))
        generate_ticket(qr_code, full_code, full_name)
        send(email, name_image,full_name,qr_code)
        # print("Sent mail with user {} with qr code {}".format(name_image, qr_code))

if __name__ == '__main__':
    main()
