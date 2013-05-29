#!/usr/bin/env python
# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import os.path
import re
import simplejson
import smtplib
import sys
import traceback
import urllib

try:
    ngs = BeautifulSoup(urllib.urlopen("http://pogoda.ngs.ru").read())

    temperature_div = ngs.find("div", "today-panel__temperature")
    weather = {
        "temperature"       : temperature_div.find("span", "value__main").get_text().encode("utf-8").strip().replace(" ", "") + "°C",
        "temperature_trend" : "+" if temperature_div.find("i", "icon-temp_status-up") else "-",

        "description"       : temperature_div.find("span", "description").get_text().strip().lower(),
        "romance"           : "Восход: %s, закат: %s" % tuple(ngs.find_all("div", "today-panel__info__main__item")[1].find_all("dt")[0].get_text().encode("utf-8").strip().split(" − "))
    }

    open(os.path.join(os.path.dirname(__file__), "index.json"), "w").write(simplejson.dumps(weather))
except:
    msg = MIMEText("Ошибка обновления погоды: %s\n%s" % (repr(sys.exc_info()[1]), traceback.format_tb(sys.exc_info()[2])[0]))
    msg["Subject"] = "Ошибка обновления погоды"
    msg["From"] = "themylogin@gmail.com"
    msg["To"] = "themylogin@gmail.com"

    s = smtplib.SMTP("localhost")
    s.sendmail(msg["From"], [msg["To"]], msg.as_string())
    s.quit()
