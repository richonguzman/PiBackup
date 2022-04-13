#!/usr/bin/env python3

import os

current_folder = os.getcwd() + '/'

country_letters = ['AF','AX','AL','DZ','AS','AD','AO','AI','AQ','AG','AR','AM','AW','AU','AT','AZ',
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

answer_letters = ['y','n','Y','N']


def start_config():
    print('\n### PiBackup Country and Wifi configuration ###\n')
    country = input("-Country Code (just two letters) : ")
    country = country.upper()
    while not country in country_letters:
        country = input("-Input a valid Country Code (just two letters) : ")
        country = country.upper()
    print("\nThe default Wifi Hotspot Name is 'PiBackup'")
    answer_1 = input("-do you want to change it? (y/n) ")
    while not answer_1 in answer_letters:
        answer_1 = input("-do you want to change it? (y/n) ")
    if answer_1 == 'y' or answer_1 == 'Y':
        wifi_hotspot_name = input("-Name of NEW Wifi Hotspot Name : ")
    else:
        wifi_hotspot_name = 'PiBackup'
    print(wifi_hotspot_name)
    print("\nThe default Wifi Hotspot Password is '8Fotografia8'")
    answer_2 = input("-do you want to change it? (y/n) ")
    while not answer_2 in answer_letters:
        answer_2 = input("-do you want to change it? (y/n) ")
    if answer_2 == 'y' or answer_2 == 'Y':
        wifi_hotspot_password = input("-NEW Password (8 digits/letters or more): ")
        while len(wifi_hotspot_password) < 8:
            print("\nwifi Password must be 8 or more digits/letters")
            wifi_hotspot_password = input("-NEW Password : ")
    else:
        wifi_hotspot_password = '8Fotografia8'
    print(wifi_hotspot_password)
    
    with open(current_folder + 'conf/PBK_hostapd.conf','w') as output_file:
        output_file.write('interface=wlan0\n')
        output_file.write('ssid='+str(wifi_hotspot_name)+'\n')
        output_file.write('macaddr_acl=0\n')
        output_file.write('ignore_broadcast_ssid=0\n\n')
        
        output_file.write('## 5GHz\n')
        output_file.write('hw_mode=a\n')
        output_file.write('channel=36\n')
        output_file.write('country_code='+str(country)+'\n')
        output_file.write('ieee80211d=1\n')
        output_file.write('ieee80211n=1\n')
        output_file.write('ieee80211ac=1\n')
        output_file.write('wmm_enabled=1\n\n')
        output_file.write('## wpa auth\n')   
        output_file.write('auth_algs=1\n')
        output_file.write('wpa=2\n')
        output_file.write('wpa_passphrase='+str(wifi_hotspot_password)+'\n')
        output_file.write('wpa_key_mgmt=WPA-PSK\n')
        output_file.write('wpa_pairwise=TKIP\n')
        output_file.write('rsn_pairwise=CCMP\n')
    output_file.close()
    
    print("\n\nPiBackup configuration updated...")
    

############ CONFIGURATION ############
start_config()