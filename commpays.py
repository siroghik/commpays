import json
import datetime

gas = 'gas'
water = 'water'
el_ty = 'el_ty'
summ = 0


# FUNCTIONS

def enter_readings(r):
    if r == 'el_tariff':
        under_100 = enter_readings('el-ty under 100 kWh')
        over_100 = enter_readings('el-ty over 100 kWh')
        return [under_100, over_100]
    while True:
        try:
            v = float(input(r + ': '))
            return v
        except:
            print ('invalid format!')

def print_tariff():
    print ('-' * 8)
    print ('{0}: {1} for {2}'.format(gas, tariff[gas], 'm3'))
    print ('{0}: {1} for {2}'.format(water, tariff[water], 'm3'))
    print ('{0} under 100 kWh: {1} for {2}'.format(el_ty, tariff[el_ty][0], 'kWh'))
    print ('{0} over 100 kWh: {1} for {2}'.format(el_ty, tariff[el_ty][1], 'kWh'))
    print ('-' * 8 + '\n')

def print_readings(r):
    print ('-' * 8)
    print ('{0}: {1} {2}'.format(gas, r[gas], 'm3'))
    print ('{0}: {1} {2}'.format(water, r[water], 'm3'))
    print ('{0}: {1} {2}'.format(el_ty, r[el_ty], 'kWh'))
    print ('-' * 8 + '\n')

def print_amount():
    print ('amount:\n' + '-' * 8)
    print ('{0}: {1} {2}'.format(gas, amount[gas], 'm3'))
    print ('{0}: {1} {2}'.format(water, amount[water], 'm3'))
    print ('{0}: {1} {2}'.format(el_ty, amount[el_ty], 'kWh'))
    print ('-' * 8 + '\n')

def calculate():
    print ('pay:\n' + '-' * 8)
    pay_for_gas = amount[gas] * tariff[gas]
    pay_for_gas = round(pay_for_gas, 2)
    print ('{0}: {1} {2}'.format(gas, pay_for_gas, 'UAH'))
    pay_for_water = amount[water] * tariff[water]
    pay_for_water = round(pay_for_water, 2)
    print ('{0}: {1} {2}'.format(water, pay_for_water, 'UAH'))
    pay_for_elty = 0
    if(amount[el_ty] <= 100):
        pay_for_elty = amount[el_ty] * tariff[el_ty][0]
    else:
        under_100 = 100 * tariff[el_ty][0]
        over_100 = (amount[el_ty] - 100) * tariff[el_ty][1]
        pay_for_elty = under_100 + over_100
    pay_for_elty = round(pay_for_elty, 2)
    print ('{0}: {1} {2}'.format(el_ty, pay_for_elty, 'UAH'))
    global summ
    summ = pay_for_gas + pay_for_water + pay_for_elty
    print ('\nsum: ' + str(summ) + 'UAH')
    print ('-' * 8 + '\n')


print ('\n' + '-' * 8)
print ('commpays')
print ('-' * 8)

# load tariff
with open('tariff.json', 'r') as f:
    tariff = json.load(f)

# load old records
with open('readings.json', 'r') as f:
    readings = json.load(f)

# count old records
quantity = len(readings)
if(quantity != 0):
    print ('\nYou have ' + str(quantity) + ' records')
    prev_readings = readings[quantity-1]
    print ('last record:')
    print_readings(prev_readings)
else:
    print ('\nyou have no records')
    prev_readings ={
        gas: 0.0,
        water: 0.0,
        el_ty: 0.0
    }

# main menu
while True:
    menu_text = """
what do you want to do?
n - new readings
t - change tariff
s - show tariff
q - quit
"""
    choise = input(menu_text)
    # creat new readings
    if choise == 'n':
        print ('please enter current readings')
        curr_readings = {
            gas: enter_readings(gas),
            water: enter_readings(water),
            el_ty: enter_readings(el_ty)
        }
        print ('\n')
        # calculate amount
        amount = {
            gas: curr_readings[gas] - prev_readings[gas],
            water: curr_readings[water] - prev_readings[water],
            el_ty: curr_readings[el_ty] - prev_readings[el_ty]
        }
        # print info
        print_amount()
        calculate()
        # save current readings?
        if 'y' == input('wanna save current record? "y/n" '):
            readings.append(curr_readings)
            with open('readings.json', 'w') as f:
                json.dump(readings, f)
            print ('record saved')
        # prediction
        if 'y' == input('wanna prediction? "y/n" '):
            while True:
                payday = input('enter payday: ')
                if 0 < int(payday) < 31:
                    today = datetime.datetime.today().day
                    diff = payday - today
                    if diff <= 0:
                        diff = 30 - today + payday
                    k = 30.0 / (30 - diff)
                    pred = round(k * summ, 2)
                    print ('\n' + '-' * 8)
                    print ('{0}: {1} {2}'.format('prediction pay', pred, 'UAH'))
                    print ('-' * 8 + '\n')
                    break
                else:
                  print ('invalid payday')
    # show tariff
    elif choise == 's':
        print_tariff()
    # change tariff
    elif choise == 't':
        tariff = {
            gas: enter_readings(gas),
            water: enter_readings(water),
            el_ty: enter_readings('el_tariff')
        }
        with open('tariff.json', 'w') as f:
            json.dump(tariff, f)
        print ('tariff changed')
    # end
    elif choise == 'q':
        break

print ('\n' + '-' * 8)
print ('good bye!')
print ('-' * 8 + '\n')
