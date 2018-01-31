crontab -e  
# * * * * 1 ./python3 mail.py
nohup python3 wechat_record.py >/dev/null 2>&1 &
