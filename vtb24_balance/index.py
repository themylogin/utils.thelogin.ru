#!/home/themylogin/www/apps/virtualenv/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "apps", "thelogin62a"))
from db import db
from controller.content.model import ContentItem
sys.path.pop()

print "Content-type: text/plain; charset=utf-8\n"
print re.search(u"Доступно к использованию: ([A-Z0-9. ]+[A-Z])", db.query(ContentItem).filter(ContentItem.type == "vtb24_transaction").order_by(ContentItem.created_at.desc())[0].data["notification"]).group(1)
