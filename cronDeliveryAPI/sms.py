def send_sms(phone, key):
    print(phone)
    login = 'CronApp'
    password = 'croncron'
    message = "DeliveryAPPCode:"
    message += str(key) # DeliveryAPPCode:key
    link = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s" % (login, password, phone, message)
    print(link)

send_sms('+7(989) 461 - 32 - 51', 50676)