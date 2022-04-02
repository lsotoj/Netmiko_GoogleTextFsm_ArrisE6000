import textfsm
import os
import csv
#+++++ parsing the data ++++++++
#function for split the downstream and upstream slot x/x/x interface from de SHOW PHY command
def split_interfaz(modem):
    interfaz = modem[1]
    indice =  interfaz.index('-')
    downstream = interfaz[:indice]
    upstream = interfaz[indice + 1:]
    modem.append(downstream)
    modem.append(upstream)
    return modem

#function for split the downstream and upstream bonding dwXup from SHOW CABLE MODEM comand.
def split_bonded(modem):
    bonded = modem[3]
    if bonded != '-':
        indice_x = bonded.index('x')
        bonded_downstream = bonded[:indice_x]
        bonded_upstream = bonded[indice_x + 1:]
        modem.append(bonded_downstream)
        modem.append(bonded_upstream)
    else:
        modem.append(bonded)
        modem.append(bonded)
    
    return  modem



#opening the text plain files with the data extracted by commands with Netmiko
file_result_path = os.getcwd() + "/txt/show_phy.txt"
with open(file_result_path, 'r') as data_file:
    file_output_phy = data_file.read()

file_result_path = os.getcwd() + "/txt/show_cm.txt"
with open(file_result_path, 'r') as data_file:
    file_output_cm = data_file.read()

file_result_path = os.getcwd() + "/txt/show_slots.txt"
with open(file_result_path, 'r') as data_file:
    file_output_slots = data_file.read()



#Opening the templates used by TextFSM to match only the useful data.
template_path =os.getcwd() + "/txt/show_phy_template"
with open(template_path, 'r') as template:
    template_object_phy = textfsm.TextFSM(template)

template_path =os.getcwd() + "/txt/show_cm_template"
with open(template_path, 'r') as template:
    template_object_cm = textfsm.TextFSM(template)

template_path =os.getcwd() + "/txt/show_slots_template"
with open(template_path, 'r') as template:
    template_object_slots = textfsm.TextFSM(template)


#Here's where TextFSM makes his work and extracts only useful data for each file. It's going stored in a list. 
output_parse_phy = template_object_phy.ParseText(file_output_phy)
output_parse_cm = template_object_cm.ParseText(file_output_cm)
slots = template_object_slots.ParseText(file_output_slots)
print("nomas sale")
for cm in range(0, 10):
    print(slots[cm])

listOfDict = {};
for cm in range(0, 10):
    cmts = slots[cm][0]
    slot = slots[cm][1]
    nodo = slots[cm][2]
    listOfDict[cmts] = {slot:nodo}
print(listOfDict)

output_float_phy = []
output_bonded_cm = []

#Appling a garbage collector to the principal array
for modem in output_parse_phy:
    del modem[4]
    del modem[4]
    del modem[7]
    del modem[7]
    del modem[7]



#Here I'm splitting the slot interface and converting to float point the power level measurements
for modem in output_parse_phy:
    temporary_array = []
    temporaty_data = 0
    
    #calling the function to extract the downstream and upstream interfaz slot
    modem = split_interfaz(modem)
    
    for j in range(0, len(modem), 1):
        #Converting to float point the measurements
        if (j == 3 or j == 4 or j == 5 or j == 6) and (modem[j] != "-"):
            temporaty_data = float(modem[j])
        else:
            temporaty_data = modem[j]

        temporary_array.append(temporaty_data)
    
    output_float_phy.append(temporary_array)




#split the bonded
for modem in output_parse_cm:
    modem = split_bonded(modem)
    output_bonded_cm.append(modem)



for principal_modem in output_float_phy:
    buscado = principal_modem[7]
    indicador = 0

    for bonded_modem in output_bonded_cm:
        if buscado in bonded_modem:
            indicador = 1
            bonding_dw = bonded_modem[9]
            bonding_up = bonded_modem[10]
            if (bonding_dw != '-') and (bonding_up != '-'):
                bonding_dw = int(bonding_dw)
                principal_modem.append(bonding_dw)
                bonding_up = int(bonding_up)
                principal_modem.append(bonding_up)
                break
            else:
                principal_modem.append('-')
                principal_modem.append('-')
                break
    if indicador == 0:
        principal_modem.append('-')
        principal_modem.append('-')
            

print('BONDED DONDE')

#semaphore
for modem in output_float_phy:
    status = 'WITHOUT STATUS'
    us_snr = modem[3]
    us_pwr = modem[4]
    ds_pwr = modem[5]
    ds_snr = modem[6]
    portadoras_up = modem[11]

    
    if us_snr == '-'or us_pwr == '-' or ds_pwr == '-' or ds_snr == '-':
        modem.append(status)
        continue

    if portadoras_up == '-':
        status = 'NON BONDING'
        modem.append(status)
        continue
    elif portadoras_up <= 2:
        #valuating the green flag
        if (us_snr >= 27) and ((us_pwr > 40)and(us_pwr <= 53)) and ((ds_pwr > -9)and(ds_pwr <= 10)) and (ds_snr >= 33):
            status = 'GOOD'
            modem.append(status)
            continue

        #valuating the yellow flag
        if ((us_pwr >= 39)and(us_pwr <= 40)) or ((us_pwr > 53)and( us_pwr < 54)):
            status = 'POOR'
        elif ((ds_pwr >= -10)and(ds_pwr <= -9)) or ((ds_pwr > 10)and( ds_pwr <= 11)):
            status = 'POOR'


        #valuating red flag
        if us_snr < 27 :
            status = 'BAD'
            modem.append(status)
            continue
        elif (us_pwr < 39) or (us_pwr >= 54):
            status = 'BAD'
            modem.append(status)
            continue
        elif (ds_pwr < -10) or (ds_pwr > 11):
            status = 'BAD'
            modem.append(status)
            continue
        elif (ds_snr < 33):
            status = 'BAD'
            modem.append(status)
            continue

    # 3 or more carrier
    elif portadoras_up >= 3:
        #valuating the green flag
        if (us_snr >= 27) and ((us_pwr > 40)and(us_pwr <= 50)) and ((ds_pwr > -9)and(ds_pwr <= 10)) and (ds_snr >= 33):
            status = 'GOOD'
            modem.append(status)
            continue

        #valuating the yellow flag
        if ((us_pwr >= 39)and(us_pwr <= 40)) or ((us_pwr > 50)and( us_pwr < 51)):
            status = 'POOR'
        elif ((ds_pwr >= -10)and(ds_pwr <= -9)) or ((ds_pwr > 10)and( ds_pwr <= 11)):
            status = 'POOR'


        #valuating red flag
        if us_snr < 27 :
            status = 'BAD'
            modem.append(status)
            continue
        elif (us_pwr < 39) or (us_pwr >= 51):
            status = 'BAD'
            modem.append(status)
            continue
        elif (ds_pwr < -10) or (ds_pwr > 11):
            status = 'BAD'
            modem.append(status)
            continue
        elif (ds_snr < 33):
            status = 'BAD'
            modem.append(status)
            continue
    
    modem.append(status)


with open('GFG', 'w') as fcsv:
    # using csv.writer method from CSV package
    write = csv.writer(fcsv)
    for dato in output_float_phy:
        write.writerow(dato)
print("TO CSV DONE")