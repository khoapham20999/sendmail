import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import conf

def send(toaddr, name_image, full_name) :
    body = "Vé của bạn: "
    from_mail = conf.username
    msg = MIMEMultipart()
    msg['From'] = from_mail
    msg['To'] = toaddr
    msg['Subject'] = "Welcome to the festival"
    msg.attach(MIMEText(body, 'plain'))

    img_data = open("/home/khoa/working/sendmail/images/{}.png".format(name_image), 'rb').read()
    html_part = MIMEMultipart(_subtype='related')
    body = MIMEText('''<p>Hello <strong> {} </strong> </p>
    <img src="cid:myimage" alt="Logo" style="width:200px;height:200px;"/>'''.format(full_name), _subtype='html')
    html_part.attach(body)

    img = MIMEImage(img_data, 'jpg')
    img.add_header('Content-Id', '<myimage>')  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="myimage")
    html_part.attach(img)
    msg.attach(html_part)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_mail, conf.password)
    text = msg.as_string()

    s.sendmail(from_mail, toaddr, text)
    s.quit()









#
