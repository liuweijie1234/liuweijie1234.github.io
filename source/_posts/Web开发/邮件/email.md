


```python
import smtplib
from email.mime.text import MIMEText
from email.header import Header

MAIL_TO_ADDRS = ["2496234829@qq.com", "liuweijie@kaadas.com"]
MAIL_HOST = "smtp.qiye.163.com"  # 设置服务器
MAIL_PORT_1 = 587
MAIL_PORT_2 = 465
MAIL_ADDRS = "odoo@kaadas.com"  # 用户名
MAIL_PWD = "xxxx"  # 口令

class EmailSender:
    def __init__(self):
        self.host = MAIL_HOST
        self.port_1 = MAIL_PORT_1
        self.port_2 = MAIL_PORT_2
        self.user = MAIL_ADDRS
        self.password = MAIL_PWD

    def _send_email(self, to_addr_list, subject, content, content_type):
        message = MIMEText(content, content_type, 'utf-8')
        message['From'] = email.utils.formataddr(('ATE系统', self.user))
        message['To'] = Header(", ".join(to_addr_list))
        message['Subject'] = Header(subject, 'utf-8')

        with smtplib.SMTP(host=self.host, port=self.port_1) as smtpObj:
            smtpObj.starttls()
            try:
                smtpObj.login(user=self.user, password=self.password)
            except smtplib.SMTPAuthenticationError as err:
                logging.error("SMTP authentication failed for user %s: %s" % (self.user, str(err)))
                raise err

            try:
                smtpObj.sendmail(from_addr=self.user, to_addrs=to_addr_list, msg=message.as_string())
            except smtplib.SMTPServerDisconnected as e:
                logging.error("SMTP server unexpectedly closed the connection: %s" % str(e))
                smtpObj = smtplib.SMTP_SSL(host=self.host, port=self.port_2)
                smtpObj.login(user=self.user, password=self.password)
                smtpObj.sendmail(from_addr=self.user, to_addrs=to_addr_list, msg=message.as_string())
            except Exception as err:
                logging.error("Failed to send email from %s to %s: %s" % (self.user, to_addr_list, str(err)))
                raise err

    def send_plain_email(self, to_addrs, subject, content):
        self._send_email(to_addrs, subject, content, 'plain')

    def send_html_email(self, to_addrs, subject, content):
        self._send_email(to_addrs, subject, content, 'html')

def check_onmicro_mac():
    total_remain_num = MACSubsection.objects.exclude(status=2).aggregate(total_remain=Sum('remain_num'))
    remain_num = int(total_remain_num['total_remain'])
    if remain_num <= Onmicro_NUM:
        subject_variable = "昂瑞微Mac不足"
        PLANT_NAME = PLANT_CONTRAST[PLANT]
        subject = f"{PLANT_NAME} ATECenter 告警: {subject_variable}"
        content = f"<html><body><h1>当前昂瑞微剩余MAC数量：{remain_num}</h1>" \
                  f"<p>{PLANT_NAME} 工厂 昂瑞微MAC 余量不足{Onmicro_NUM}, 请马上补充</p></body></html>"
        try:
            sender = EmailSender()
            sender.send_html_email(to_addrs=MAIL_TO_ADDRS, subject=subject, content=content)
            logger_run.warning("ESN监控发送邮箱成功！")
        except Exception as e:
            logger_run.error("ESN监控发送邮箱失败，错误原因：{}".format(e))

``` 