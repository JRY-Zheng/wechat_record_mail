#!/usr/bin/python\
from email import encoders
from email.header import Header
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib, time, os, random, re
import datetime, codecs
import matplotlib.pyplot as plt
  
s = os.sep

template = [
    '指定一个邮件的模板，示例：这是一个打卡记录邮件。'
    ]
hd = '*************打卡记录*************\n'
tl = '*************继续加油*************\n'

last_week = datetime.date.today() - datetime.timedelta(days=7)
iso = last_week.isocalendar()
week_index = '%s-%s' % (iso[0], iso[1])
with codecs.open('.' + s + 'daka_chat' + s + week_index + '.cht', 'r', 'utf-8') as f:
    # content = f.read()
    lines = f.readlines()
content = ''.join(lines)

times_in_week_of_fr = [0, 0, 0, 0, 0, 0, 0]
times_in_week_of_me = [0, 0, 0, 0, 0, 0, 0]
for line in lines:
    matchs = re.match(r'(\d+)-(\d+)-(\d+)@(.+?):(.+)', line)
    # print(line, matchs)
    if matchs:
        # w, y, m, d, p, s = matchs
        y = int(matchs.group(1))
        m = int(matchs.group(2))
        d = int(matchs.group(3))
        p = matchs.group(4)
        dow = datetime.datetime(y, m, d).weekday()
        if p == '微信名':  # 如果希望使用备注名，可以在wechat_record里修改
            times_in_week_of_fr[dow] += 1
        else:
            times_in_week_of_me[dow] += 1

name_of_week = ['一', '二', '三', '四', '五', '六', '日']
label = ['Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.', 'Sun.']
legend = ['Your freind', 'You']
fr_plot = plt.plot(range(7), times_in_week_of_fr, '*-')
me_plot = plt.plot(range(7), times_in_week_of_me, '*-')
plt.xticks(range(7), label, rotation=0)
plt.ylabel('Frequency')  
plt.title('Weekly Record')
plt.legend(legend, loc = 1, ncol = 1)
plt.savefig('.' + s + 'wechat'+ s + 'graphic-daka' + s + 'frequency' + str(last_week) + '.png')

compliment = ''
for table in (times_in_week_of_fr, times_in_week_of_me):
    day_with_max_times = [0]
    day_with_zero_time = []
    for day in range(7):
        if table[day] == 0:
            day_with_zero_time.append(day)
        if day == 0:continue
        if table[day_with_max_times[0]] < table[day]:
            day_with_max_times.clear()
            day_with_max_times.append(day)
        elif table[day_with_max_times[0]] == table[day]:
            day_with_max_times.append(day)
    success = '、'.join(['星期' + name_of_week[num] for num in day_with_max_times])
    fail = '、'.join(['星期' + name_of_week[num] for num in day_with_zero_time])
    praise = ('朋友，你在' if compliment == '' else '而我在') + success + '打卡次数最多，足足打卡了' + str(table[day_with_max_times[0]]) + '次！'
    critise = ('但是在' + fail + '没有完成打卡任务哦！\n') if fail else ('并且每天都完成了任务！\n' if compliment == '' else '每天也都完成了任务！\n')
    compliment += praise + critise

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

msgct = template[random.randint(0, len(template) - 1)] + compliment + hd + content + tl
with open('.' + s + 'mail_record.ml', 'a') as f:
    f.write(msgct + '\n')
msg = MIMEMultipart()

from_addr = 'example@123.com'
pafrword = 'pafrword'
to_addr = ['example@123.com', 'example@123.com']
smtp_server = 'smtp.123.com'

# msg = MIMEText(msgct, 'plain', 'utf-8')
msg['From'] = _format_addr('Your name <%s>' % from_addr)
msg['To'] = _format_addr("Your friend's name <%s>, Your name<%s>" % (to_addr1, to_addr2))
msg['Subject'] = Header(time.strftime('%Y年第%W周的打卡记录',time.localtime(time.time())), 'utf-8').encode()
# msg.attach(MIMEText(msgct, 'plain', 'utf-8'))
with open('.' + s + 'wechat'+ s + 'graphic-daka' + s + 'frequency' + str(last_week) + '.png', 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'png', filename='frequency' + str(last_week) + '.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='frequency' + str(last_week) + '.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)
msg.attach(MIMEText('<p>' + msgct.replace('\n', '<br/>') + '</p>' + '<p><img src="cid:0"></p>' + '</body></html>', 'html', 'utf-8'))

import smtplib
server = smtplib.SMTP(smtp_server, 587) # SMTP协议默认端口是25
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, pafrword)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()
