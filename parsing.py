import textfsm
import os
import csv
#+++++ parsing the data ++++++++
#function for split the downstream and upstream interface
def split_interfaz(modem):
    interfaz = modem[1]
    indice =  interfaz.index('-')
    downstream = interfaz[:indice]
    upstream = interfaz[indice + 1:]
    modem.append(downstream)
    modem.append(upstream)
    return modem

#function for split the downstream and upstream bonding 
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



#opening the text plain files
file_result_path = os.getcwd() + "/txt/show_phy.txt"
with open(file_result_path, 'r') as data_file:
    file_output_phy = data_file.read()

file_result_path = os.getcwd() + "/txt/show_cm.txt"
with open(file_result_path, 'r') as data_file:
    file_output_cm = data_file.read()

file_result_path = os.getcwd() + "/txt/show_slots.txt"
with open(file_result_path, 'r') as data_file:
    file_output_slots = data_file.read()



#opening the templates
template_path =os.getcwd() + "/txt/show_phy_template"
with open(template_path, 'r') as template:
    template_object_phy = textfsm.TextFSM(template)

template_path =os.getcwd() + "/txt/show_cm_template"
with open(template_path, 'r') as template:
    template_object_cm = textfsm.TextFSM(template)

template_path =os.getcwd() + "/txt/show_slots_template"
with open(template_path, 'r') as template:
    template_object_slots = textfsm.TextFSM(template)

#parsed data 
output_parse_phy = template_object_phy.ParseText(file_output_phy)
output_parse_cm = template_object_cm.ParseText(file_output_cm)
output_parse_slots = template_object_slots.ParseText(file_output_slots)

output_float_phy = []
output_bonded_cm = []



for modem in output_parse_phy:
    temporary_array = []
    temporaty_data = 0
    
    #calling the function to extract the downstream and upstream IF
    modem = split_interfaz(modem)
    
    for j in range(0, len(modem), 1):
        #Converting to float point the measurements
        if (j == 3 or j == 6 or j == 7 or j == 8) and (modem[j] != "-"):
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
    buscado = principal_modem[12]
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
    us_pwr = modem[6]
    ds_pwr = modem[7]
    ds_snr = modem[8]
    portadoras_up = modem[16]

    
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