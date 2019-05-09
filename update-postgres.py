#!/usr/bin/python

import re
import psycopg2
import config


def string_found(string1, string2):
    """Get matching whole words in string"""
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False


CON = None

try:
    CONNECTION = psycopg2.connect(config)
    CUR = CONNECTION.cursor()
    CUR.execute("SELECT pk_article_id,title,category,tag_ids \
                FROM learning.articles where category = 'Unread'")
    UNREAD = CUR.fetchall()
    CUR.execute("SELECT pk_tag_id,association FROM learning.tag")
    TAGS_RESULT = []
    for t in CUR.fetchall():
        if isinstance(t, int):
            continue
        else:
            TAGS_RESULT.append(t)

    for a in UNREAD:
        ARTICLE_ID = a[0]
        ARTICLE_TITLE = a[1]
        ARTICLE_CATEGORY = a[2]
        ARTICLE_TAG_IDS = a[3]

        for TAG_RESULT in TAGS_RESULT:
            for association in TAG_RESULT[1]:
                # print(tag_association.lower(),article_title.lower())
                # print(string_found(tag_association.lower(),article_title.lower()))
                if string_found(association.lower(), ARTICLE_TITLE.lower()):
                    if isinstance(ARTICLE_TAG_IDS, list) and ARTICLE_TAG_IDS:
                        TAGS = list(set(ARTICLE_TAG_IDS + [TAG_RESULT[0]]))
                    else:
                        TAGS = [TAG_RESULT[0]]

                    CUR.execute("UPDATE learning.articles \
                                SET tag_ids = %s \
                                where pk_article_id = %s", (TAGS, ARTICLE_ID))
                else:
                    tags = []


    CUR.execute("SELECT \
                COUNT(case when category = 'Unread' and tag_ids != '{}' \
                then 1 else null end) as tagged,\
                COUNT(case when category = 'Unread' and tag_ids = '{}' \
                then 1 else null end) as untagged\
                from learning.articles")

    print(CUR.fetchall())

    CONNECTION.commit()
finally:
    if CONNECTION:
        CONNECTION.close()
