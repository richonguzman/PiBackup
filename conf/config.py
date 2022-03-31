#!/usr/bin/env python3

import os

current_folder = os.getcwd() + '/'

country = ['AF','AX','AL','DZ','AS','AD','AO','AI','AQ','AG','AR','AM','AW','AU','AT','AZ',
           'BH','BS','BD','BB','BY','BE','BZ','BJ','BM','BT','BO','BQ','BA','BW','BV','BR',
           'IO','BN','BG','BF','BI','KH','CM','CA','CV','KY','CF','TD','CL','CN','CX','CC',
           'CO','KM','CG','CD','CK','CR','CI','HR','CU','CW','CY','CZ','DK','DJ','DM','DO',
           'EC','EG','SV','GQ','ER','EE','ET','FK','FO','FJ','FI','FR','GF','PF','TF','GA',
           'GM','GE','DE','GH','GI','GR','GL','GD','GP','GU','GT','GG','GN','GW','GY','HT',
           'HM','VA','HN','HK','HU','IS','IN','ID','IR','IQ','IE','IM','IL','IT','JM','JP',
           'JE','JO','KZ','KE','KI','KP','KR','KW','KG','LA','LV','LB','LS','LR','LY','LI',
           'LT','LU','MO','MK','MG','MW','MY','MV','ML','MT','MH','MQ','MR','MU','YT','MX',
           'FM','MD','MC','MN','ME','MS','MA','MZ','MM','NA','NR','NP','NL','NC','NZ','NI',
           'NE','NG','NU','NF','MP','NO','OM','PK','PW','PS','PA','PG','PY','PE','PH','PN',
           'PL','PT','PR','QA','RE','RO','RU','RW','BL','SH','KN','LC','MF','PM','VC','WS',
           'SM','ST','SA','SN','RS','SC','SL','SG','SX','SK','SI','SB','SO','ZA','GS','SS',
           'ES','LK','SD','SR','SJ','SZ','SE','CH','SY','TW','TJ','TZ','TH','TL','TG','TK',
           'TO','TT','TN','TR','TM','TC','TV','UG','UA','AE','GB','US','UM','UY','UZ','VU',
           'VE','VN','VG','VI','WF','EH','YE','ZM','ZW']

answer = ['y','n','Y','N']


def start_config():
    print('\n### PiBackup Country and Wifi configuration ###\n')
    pais = input("-Country Code (just two letters) : ")
    pais = pais.upper()
    while not pais in country:
        pais = input("-Input a valid Country Code (just two letters) : ")
        pais = pais.upper()
    print("\nThe default Wifi Hotspot Name is 'PiBackup'")
    respuesta = input("-do you want to change it? (y/n) ")
    while not respuesta in answer:
        respuesta = input("-do you want to change it? (y/n) ")
    if respuesta == 'y' or respuesta == 'Y':
        nombre_wifi = input("-Name of NEW Wifi Hotspot Name : ")
    else:
        nombre_wifi = 'PiBackup'
    print(nombre_wifi)
    print("\nThe default Wifi Hotspot Password is '8Fotografia8'")
    respuesta2 = input("-do you want to change it? (y/n) ")
    while not respuesta2 in answer:
        respuesta2 = input("-do you want to change it? (y/n) ")
    if respuesta2 == 'y' or respuesta2 == 'Y':
        password_wifi = input("-NEW Password (8 digits/letters or more): ")
        while len(password_wifi) < 8:
            print("\nwifi Password must be 8 or more digits/letters")
            password_wifi = input("-NEW Password : ")
    else:
        password_wifi = '8Fotografia8'
    print(password_wifi)
    print("\n\nPiBackup configuration updated...")
    
    with open(current_folder + 'PBK_hostapd.conf','w') as salida:
        salida.write('interface=wlan0\n')
        salida.write('ssid='+str(nombre_wifi)+'\n')
        salida.write('macaddr_acl=0\n')
        salida.write('ignore_broadcast_ssid=0\n\n')
        
        salida.write('## 5GHz\n')
        salida.write('hw_mode=a\n')
        salida.write('channel=36\n')
        salida.write('country_code='+str(pais)+'\n')
        salida.write('ieee80211d=1\n')
        salida.write('ieee80211n=1\n')
        salida.write('ieee80211ac=1\n')
        salida.write('wmm_enabled=1\n\n')
        
        salida.write('## wpa auth\n')   
        salida.write('auth_algs=1\n')
        salida.write('wpa=2\n')
        salida.write('wpa_passphrase='+str(password_wifi)+'\n')
        salida.write('wpa_key_mgmt=WPA-PSK\n')
        salida.write('wpa_pairwise=TKIP\n')
        salida.write('rsn_pairwise=CCMP\n')
    salida.close()


############ CONFIGURATION ############
start_config()