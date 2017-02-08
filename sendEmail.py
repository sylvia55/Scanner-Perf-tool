import smtplib
from os.path import join
from email.mime.text import MIMEText


class sendEmail():
    def send_email(self, user, host, receiverlist, content):
        server = smtplib.SMTP()
        server.connect(host=host, port=25)
        server.ehlo()
        # server.starttls()
        # server.login(user, password)
        server.sendmail(user, receiverlist, content)
        server.close()

    def initial_send_mail(self, subject, content):
        # content = content.split(":")
        a = ''
        for c in content.split(':'):
            temp = join('<p>', c, '</p>')
            a = join(a, temp)
        host = "cdcrelay.tw.trendnet.org"
        user = "sylvia@test.com"
        # password = "Evita0!234"
        receiverlist =["sylvia_wu@trendmicro.com.cn", "wuwuyunhu@126.com"]
        body = "\r\n".join([
            "From: %s"%user,
            "To: %s"%",".join(receiverlist),
            "Subject: %s"%subject,
            "",
            str(a)
        ])
        # body = content
        self.send_email(user, host, receiverlist, body)


def main():
    email = sendEmail()
    # content =
    email.initial_send_mail("subject is sylvia", "content is sylvia hello")


if __name__ == '__main__':
    main()