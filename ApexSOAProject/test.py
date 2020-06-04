import email.parser

parser = email.parser.FeedParser()
print(parser, '222222222222222222222222222222222222222222222222223333333333333333333333333333333333322222222222222222')
email = '''Delivered-To: apex.mailer@cselectric.co.in
Received: by 2002:a7b:cc16:0:0:0:0:0 with SMTP id f22csp3086373wmh;
        Mon, 11 May 2020 20:14:07 -0700 (PDT)
X-Received: by 2002:ac2:4213:: with SMTP id y19mr12272212lfh.99.1589253247341;
        Mon, 11 May 2020 20:14:07 -0700 (PDT)
ARC-Seal: i=1; a=rsa-sha256; t=1589253247; cv=none;
        d=google.com; s=arc-20160816;
        b=Vu+IA8+leMHdSIKhx22E+Yckc7WqaxZ9mKvkFHYF/GNPZke1XjgjR2fYmPZughJmkU
         CpvRJ/BvbN63iiXvzMMbs9URdQNPwsmrqPrJ+uoe6YOYxJ5h6yuHtB3NfXPgtqRZJHow
         5jxM5MvbE/SN6kUJwjeBI6wGx6aQ2zgF+E6kStoslLe7GZWRLNn1+corX8wtbgy0Mo46
         1Wg10rUFAJm+puWbsuHsJHjO5zr2UvRtV3vScz+Q33MyC1sc2OGKAxRJUb/3P+ezKQ4V
         J6oamo5cATPj+PnzxNcc5qm9KkW2vK1+ciWqF8LURZ+n5A5bLnFVILrS+qxjctBttP46
         tK2g==
ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;
        h=to:subject:message-id:date:from:mime-version:dkim-signature;
        bh=009BqNRlPlm0pPB3nOb2OVxpf6xTMjrnxHpSjGVK7HU=;
        b=B37NRw2d5wr/Ep+m5a9zHiu/FwOJcHp2uyuP1hXySk1nY6abbBH5DszpQ3teFthwjQ
         Or4em3bUB1dwY9Pt5IliorL6ugUl6CikQmrgIDgOXWoAywDeZpoiVQrHYL515JA1aLOk
         j4GOe4gezQh76WOGUTU3RlXRLvJoBD9eAwlL8UVAPo10dduOEVtYDx8MQIP7EQ+M7I+n
         nmDLPdq+QVlnKOd0xA11tOEmu7z+SzQHP8UO9rr839WpElgmY5JWPofS2IWZ7AsObZy1
         gC0W24Hexs/MF8aPbh403L/zMC/9/+g2VVxysVD6knY3WYSL84k4Tys1+Sj4mI+UIt8C
         4JEA==
ARC-Authentication-Results: i=1; mx.google.com;
       dkim=pass header.i=@cselectric.co.in header.s=google header.b=jO9oXb1S;
       spf=pass (google.com: domain of harshita.agarwal@cselectric.co.in designates 209.85.220.41 as permitted sender) smtp.mailfrom=harshita.agarwal@cselectric.co.in;
       dmarc=pass (p=QUARANTINE sp=QUARANTINE dis=NONE) header.from=cselectric.co.in
Return-Path: <harshita.agarwal@cselectric.co.in>
Received: from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])
        by mx.google.com with SMTPS id d15sor7383725lji.31.2020.05.11.20.14.07
        for <apex.mailer@cselectric.co.in>
        (Google Transport Security);
        Mon, 11 May 2020 20:14:07 -0700 (PDT)
Received-SPF: pass (google.com: domain of harshita.agarwal@cselectric.co.in designates 209.85.220.41 as permitted sender) client-ip=209.85.220.41;
Authentication-Results: mx.google.com;
       dkim=pass header.i=@cselectric.co.in header.s=google header.b=jO9oXb1S;
       spf=pass (google.com: domain of harshita.agarwal@cselectric.co.in designates 209.85.220.41 as permitted sender) smtp.mailfrom=harshita.agarwal@cselectric.co.in;
       dmarc=pass (p=QUARANTINE sp=QUARANTINE dis=NONE) header.from=cselectric.co.in
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=cselectric.co.in; s=google;
        h=mime-version:from:date:message-id:subject:to;
        bh=009BqNRlPlm0pPB3nOb2OVxpf6xTMjrnxHpSjGVK7HU=;
        b=jO9oXb1SGHchw5SALMbKOK0D2/bo11P12oh+XD0RpKU4k54KUECQ5OzQpu6KQPq/Uz
         3jRG9WKs3SkOe7vjR1FSrRwKn9goOdGLLVyHfqco/uZNL017PwfwtrmZ9XR1ZIS266cK
         iXv77niVsWYVlKy+t/6mNZK6ekv5pKg6Cov2c=
X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20161025;
        h=x-gm-message-state:mime-version:from:date:message-id:subject:to;
        bh=009BqNRlPlm0pPB3nOb2OVxpf6xTMjrnxHpSjGVK7HU=;
        b=UZaTUxfF7Q5OxSlbTjOKbxNoLvqc08oWDFHTdIRQ6LC38a7u8tIpyc2ncWlPDUpg0s
         yjMTJPihBT7Aof3RCMp8LN+q/DW6JNUyA6fH7Csk6eR9WcwtkwA1VLALeJV5nEw4EBeU
         G0OdMNP4WkOC7fhjbriGrs9eq6oNZcYHHI0CrWpqLuqBfpAJOfbGKduWS0mVvjVKkxPU
         gKWGSy2Fy0/GRyd/HE1h7xW2NHhRgLG0aGq/gAwLgQ7bFYhKFf7IUKAVrgyCHU0BNAIH
         0F+btVWbKh+VjwH6t8GgH0QXy/EjlIK3WxNQhdwp8xdFEXDe10Y9qt8zhE3N5iJQnK/s
         xBXQ==
X-Gm-Message-State: AOAM533NHSpxLpQMNme0bY6tWVNNtghT3AIkjlaJoGrSPffD2zJUvjRD
	OxK7GvLwDdDmZJclry1FOvc6zlSZxc6PvFbABpXej6/TJH8=
X-Google-Smtp-Source: ABdhPJyV5UiHmZ03hoPgZm9+DdC18teCee7H+JwwW+/nKRl9tQjI+vpfp/GoKfo+GQ7OxEBEZPr9jXFY8vScegKnW/Q=
X-Received: by 2002:a2e:3009:: with SMTP id w9mr12485328ljw.71.1589253246711;
 Mon, 11 May 2020 20:14:06 -0700 (PDT)
MIME-Version: 1.0
From: Harshita Agarwal <harshita.agarwal@cselectric.co.in>
Date: Tue, 12 May 2020 08:43:40 +0530
Message-ID: <CAMbLPgBk+Aeqn0_Z0t3+32FnRTEJ4YUym4OrYbzc6i5hdHN-yg@mail.gmail.com>
Subject: Approve Apex Item ID (264828)
To: apex.mailer@cselectric.co.in
Content-Type: multipart/alternative; boundary="0000000000003ab97605a56adb18"

--0000000000003ab97605a56adb18
Content-Type: text/plain; charset="UTF-8"

Approval_Data_template"TRX Level":"2",
"Forwarded By":"5",
"Forwarded To":"3",
"Item Template":"@Asset Group Item"
End.
This is an automatically generated email. PLEASE DO NOT MODIFY ITS CONTENT
OR STRUCTURE!

--0000000000003ab97605a56adb18
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: quoted-printable

<div dir=3D"ltr">Approval_Data_template&quot;TRX Level&quot;:&quot;2&quot;,=
<br>&quot;Forwarded By&quot;:&quot;5&quot;,<br>&quot;Forwarded To&quot;:&qu=
ot;3&quot;,<br>&quot;Item Template&quot;:&quot;@Asset Group Item&quot;<br>E=
nd.<br>This is an automatically generated email. PLEASE DO NOT MODIFY ITS C=
ONTENT OR STRUCTURE! </div>

--0000000000003ab97605a56adb18--
'''
import json
import re
# data = "\@9895"
# email1 = ''.join([data,email]).splitlines()
# # print(email1)
# dd= ''.join([item.rstrip("', '") for item in email1])
# # print(dd)
# sd = dd.replace('@9895','')
# print(sd,'------------------------------------------------------------------333333333333333333333333333333333333333333----------------')

# parser.feed(sd)
parser.feed(email)
print(parser,'dddddddddddddddddddddddddddddddd')
msg = parser.close()
print("Subject:", msg['subject'])
for payload in msg.get_payload():
    body = payload.get_payload()
    #     print(body)
    aa = re.findall(r'Approval_Data_template(.*?)End.', str(body), re.DOTALL)

    #     data =str({body})
    s = str(aa).replace('\\n', ' ')
    q = str(s).replace("['", '{')
    final_body_rplc = str(q).replace("']", '}')
    #     print(final_body_rplc,'sssssssssssssssssssssssssssssssss')
    body_dict = json.loads(final_body_rplc)
    print(body_dict, 'xxxxxxx')
    try:
        trx_level = body_dict['TRX Level']
        forwarded_by = body_dict['Forwarded By']
        forwarded_to = body_dict['Forwarded To']
        item_template = body_dict['Item Template']
        print(item_template, trx_level, 'dddddddddddddddddddddddddddddd444444444444444444444444444')
    except:
        print('cd')
#
