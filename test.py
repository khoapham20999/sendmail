import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders

# fromaddr = "EMAIL address of the sender"
# toaddr = "EMAIL address of the receiver"

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg['From'] = "chanphuoc.carloauticus@gmail.com"

# storing the receivers email address
msg['To'] = "khoapham20999@gmail.com"

# storing the subject
msg['Subject'] = "Welcome to the world"

# string to store the body of the mail
body = "Body_of_the_mail"

# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

# open the file to be sent
# filename = "qr.jpg"
# attachment = open("/home/khoa/working/sendmail/images/a.jpg", "rb")
#
# # instance of MIMEBase and named as p
# p = MIMEBase('application', 'octet-stream')
#
# # To change the payload into encoded form
# p.set_payload((attachment).read())
#
# encoders.encode_base64(p)
#
# p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
#
# msg.attach(p)

# html = """\
# <html>
#   <head></head>
#     <body>
#       <img src="cid:image1" alt="Logo" style="width:250px;height:50px;"><br>
#        <p><h4 style="font-size:15px;">Some Text.</h4></p>
#     </body>
# </html>
# """
# # Record the MIME types of text/html.
# part2 = MIMEText(html, 'html')
#
# # Attach parts into message container.
# msg.attach(part2)
#
# fp = open('/home/khoa/working/sendmail/images/a.jpg', 'rb')
# msgImage = MIMEImage(fp.read())
# fp.close()
#
# # Define the image's ID as referenced above
# msgImage.add_header('Content-ID', '<image1>')
# msg.attach(msgImage)
img_data = open('/home/khoa/working/sendmail/images/a.jpg', 'rb').read()
html_part = MIMEMultipart(_subtype='related')
body = MIMEText('''<p>Hello</p>
<img src="cid:myimage" alt="Logo" style="width:200px;height:200px;"/>''', _subtype='html')
html_part.attach(body)


img = MIMEImage(img_data, 'jpg')
img.add_header('Content-Id', '<myimage>')  # angle brackets are important
img.add_header("Content-Disposition", "inline", filename="myimage")
html_part.attach(img)
msg.attach(html_part)

# fp = open("/home/khoa/working/sendmail/images/a.jpg", 'rb')
# img = MIMEImage(fp.read())
# fp.close()
#
# msg.attach(img)

s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

s.login("chanphuoc.carloauticus@gmail.com", "mypassword")

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail("chanphuoc.carloauticus@gmail.com", "khoapham20999@gmail.com", text)

# terminating the session
s.quit()
