#!/usr/bin/python

import sys
import psycopg2
import config

CONNECTION = None

try:
    CONNECTION = psycopg2.connect(config)
    CUR = CONNECTION.cursor()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'assigned':
            WHERE = "and tag_ids != '{}'"
        elif sys.argv[1] == 'unassigned':
            WHERE = "and tag_ids = '{}'"
        else:
            sys.exit()

        print(WHERE)

        CUR.execute("SELECT pk_article_id, title FROM learning.articles \
                where category = 'Unread' %s" % WHERE)

        for result in CUR.fetchall():
            print(result)

    CONNECTION.commit()
finally:
    if CONNECTION:
        CONNECTION.close()
