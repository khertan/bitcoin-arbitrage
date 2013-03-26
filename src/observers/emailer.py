import logging
from observer import Observer
import config
import smtplib
import datetime

def send_email(subject, message):
    _to = config.smtp_to
    _from = config.smtp_from
    _date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
    mime_message = """From: Python Arbitrage Script <%(_from)s>
To: <%(_to)s>
Date: %(_date)s
Subject: %(subject)s

%(message)s
""" % locals()
    try:
        smtpObj = smtplib.SMTP_SSL(config.smtp_host, config.smtp_port)
        smtpObj.login(config.smtp_login, config.smtp_passwd)
        smtpObj.sendmail(_from, [_to], mime_message)
    except smtplib.SMTPException, err:
        logging.warn("Unable to send email")

class Emailer(Observer):
    def opportunity(self, profit, volume, buyprice, kask, sellprice, kbid, perc, weighted_buyprice, weighted_sellprice):
        if profit > config.profit_thresh and perc > config.perc_thresh:
            message = """profit: %f EUR with volume: %f BTC
buy at %.4f (%s) sell at %.4f (%s) ~%.2f%%
""" % (profit, volume, buyprice, kask, sellprice, kbid, perc)
            send_email("[Arbitrer] Operation", message)

if __name__ == "__main__":
    send_email("test", "hey!")

