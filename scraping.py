from netmiko import ConnectHandler
import getpass
import traceback
import os
import textfsm


username = os.environ['VPN_USER']
password = getpass.getpass(prompt='Password: ', stream=None)
path_files = os.getcwd()

#opening the devices file with the cmts IP's
devices_path = os.getcwd()+"/txt/devices.txt"
with open(devices_path, 'r') as devices:
    result = devices.read()    
    list_of_cmts = result.strip().splitlines()

#creation of the files with the extracted data
f_phy = open(path_files + '/txt/show_phy.txt', 'w', encoding='utf-8')
f_cm = open(path_files + '/txt/show_cm.txt', 'w', encoding='utf-8')
f_slots = open(path_files + '/txt/show_slots.txt', 'w', encoding='utf-8')

#functions to write the data
def write_file_phy(data):
    f_phy.write(data)
    f_phy.write('\n')

def write_file_cm(data):
    f_cm.write(data)
    f_cm.write('\n')

def write_file_slots(data):
    f_slots.write(data)
    f_slots.write('\n')


#iterating all file with the cmts IP's
#show cm phy
for ip_cmts in list_of_cmts:
    try:
        with ConnectHandler(ip=ip_cmts, device_type='linux', username=username, password=password) as net_connect:
            print('SSH Connection to: ' + ip_cmts)
            
            #recording the CMTS name
            nombre_cmts = net_connect.find_prompt()
            write_file_phy(nombre_cmts)
      
            #show cm phy
            net_connect.send_command('terminal length 0', expect_string = '[#\?$]')
            outputPhy = net_connect.send_command('show cable modem phy', expect_string = '[#\?$]')
            write_file_phy(outputPhy)
            print("PHY Done")
    except Exception as error:
        print(error.__doc__)
        print(traceback.format_exc())

#show CM
for ip_cmts in list_of_cmts:
    try:
        with ConnectHandler(ip=ip_cmts, device_type='linux', username=username, password=password) as net_connect:
            print('SSH Connection Again ' + ip_cmts)
            
            #recording the CMTS name
            nombre_cmts = net_connect.find_prompt()
            write_file_cm(nombre_cmts)
 
            #show cm
            net_connect.send_command('terminal length 0', expect_string = '[#\?$]')
            outputCM = net_connect.send_command('show cable modem', expect_string = '[#\?$]')
            write_file_cm(outputCM)
            print("SH CM Done")
    except Exception as error:
        print(error.__doc__)
        print(traceback.format_exc())


#show cm port slot ...
for ip_cmts in list_of_cmts:
    try:
        with ConnectHandler(ip=ip_cmts, device_type='linux', username=username, password=password) as net_connect:
            print('Connected to ' + ip_cmts + ' for SLOT 1')

            #recording the CMTS name
            nombre_cmts = net_connect.find_prompt()
            write_file_slots(nombre_cmts)

            net_connect.send_command('terminal length 0', expect_string = '[#\?$]')
            outputSlot1 = net_connect.send_command('show cable modem summary port slot 1', expect_string = '[#\?$]')
            write_file_slots(outputSlot1)
    except Exception as error:
        print(error.__doc__)
        print(traceback.format_exc())

    #SLOT 2
    try:
        with ConnectHandler(ip=ip_cmts, device_type='linux', username=username, password=password) as net_connect:
            print('Connected to ' + ip_cmts + ' for SLOT 2')

            #recording the CMTS name
            nombre_cmts = net_connect.find_prompt()
            write_file_slots(nombre_cmts)

            net_connect.send_command('terminal length 0', expect_string = '[#\?$]')
            outputSlot2 = net_connect.send_command('show cable modem summary port slot 2', expect_string = '[#\?$]')
            write_file_slots(outputSlot2)
    except Exception as error:
        print(error.__doc__)
        print(traceback.format_exc())

    #SLOT 3
    try:
        with ConnectHandler(ip=ip_cmts, device_type='linux', username=username, password=password) as net_connect:
            print('Connected to ' + ip_cmts + ' for SLOT 3')

            #recording the CMTS name
            nombre_cmts = net_connect.find_prompt()
            write_file_slots(nombre_cmts)

            net_connect.send_command('terminal length 0', expect_string = '[#\?$]')
            outputSlot3 = net_connect.send_command('show cable modem summary port slot 3', expect_string = '[#\?$]')
            write_file_slots(outputSlot3)
    except Exception as error:
        print(error.__doc__)
        print(traceback.format_exc())

    #SLOT 4
    try:
        with ConnectHandler(ip=ip_cmts, device_type='linux', username=username, password=password) as net_connect:
            print('Connected to ' + ip_cmts + ' for SLOT 4')

            #recording the CMTS name
            nombre_cmts = net_connect.find_prompt()
            write_file_slots(nombre_cmts)

            net_connect.send_command('terminal length 0', expect_string = '[#\?$]')
            outputSlot4 = net_connect.send_command('show cable modem summary port slot 4', expect_string = '[#\?$]')
            write_file_slots(outputSlot4)
    except Exception as error:
        print(error.__doc__)
        print(traceback.format_exc())
    #SLOT 5
    try:
        with ConnectHandler(ip=ip_cmts, device_type='linux', username=username, password=password) as net_connect:
            print('Connected to ' + ip_cmts + ' for SLOT 5')

            #recording the CMTS name
            nombre_cmts = net_connect.find_prompt()
            write_file_slots(nombre_cmts)

            net_connect.send_command('terminal length 0', expect_string = '[#\?$]')
            outputSlot5 = net_connect.send_command('show cable modem summary port slot 5', expect_string = '[#\?$]') 
            write_file_slots(outputSlot5)
            print("SLOT Done")
    except Exception as error:
        print(error.__doc__)
        print(traceback.format_exc())

f_phy.close()
f_cm.close()
f_slots.close()