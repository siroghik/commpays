import json

gas = 'gas'
water = 'water'
el_ty = 'el_ty'

def enter_readings(r):
	while True:
		try:
			v = float(input(r + ': '))
			return v
		except:
			print 'invalid format!'

def print_readings(r):
	print '-' * 8
	print '{0}: {1} {2}'.format(gas, r[gas], 'm3')
	print '{0}: {1} {2}'.format(water, r[water], 'm3')
	print '{0}: {1} {2}'.format(el_ty, r[el_ty], 'kWh')
	print '-' * 8 + '\n'

def print_amount():
	print 'amount:\n' + '-' * 8
	print '{0}: {1} {2}'.format(gas, amount[gas], 'm3')
	print '{0}: {1} {2}'.format(water, amount[water], 'm3')
	print '{0}: {1} {2}'.format(el_ty, amount[el_ty], 'kWh')
	print '-' * 8 + '\n'

def calculate():
	print 'pay:\n' + '-' * 8
	pay_for_gas = amount[gas] * tariff[gas]
	pay_for_gas = round(pay_for_gas, 2)
	print '{0}: {1} {2}'.format(gas, pay_for_gas, 'UAH')
	pay_for_water = amount[water] * tariff[water]
	pay_for_water = round(pay_for_water, 2)
	print '{0}: {1} {2}'.format(water, pay_for_water, 'UAH')
	pay_for_elty = 0
	if(amount[el_ty] <= 100):
		pay_for_elty = amount[el_ty] * tariff[el_ty][0]
	else:
		under_100 = 100 * tariff[el_ty][0]
		over_100 = (amount[el_ty] - 100) * tariff[el_ty][1]
		pay_for_elty = under_100 + over_100
	pay_for_elty = round(pay_for_elty, 2)
	print '{0}: {1} {2}'.format(el_ty, pay_for_elty, 'UAH')
	print '\nsum: ' + str(pay_for_gas + pay_for_water + pay_for_elty) + 'UAH'
	print '-' * 8 + '\n'

print '\n' + '-' * 8
print 'commpays'
print '-' * 8

# load old records
with open('readings.json', 'r') as f:
	readings = json.load(f)

# count old records
quantity = len(readings)
if(quantity != 0):
	print '\nYou have ' + str(quantity) + ' records\n'
	prev_readings = readings[quantity-1]
	print 'last record:'
	print_readings(prev_readings)
else:
	print '\nyou have no records\n'
	prev_readings ={
		gas: 0.0,
		water: 0.0,
		el_ty: 0.0
	}

# enter new readings
print 'please enter current readings'
curr_readings = {
	gas: enter_readings(gas),
	water: enter_readings(water),
	el_ty: enter_readings(el_ty)
}
print '\n'

# calculate amount
amount = {
	gas: curr_readings[gas] - prev_readings[gas],
	water: curr_readings[water] - prev_readings[water],
	el_ty: curr_readings[el_ty] - prev_readings[el_ty]
}

# load tariff
with open('tariff.json', 'r') as f:
	tariff = json.load(f)

# print info
print_amount()
calculate()

# save current readings?
if 'y' == raw_input('wanna save current record? "y/n" '):
	readings.append(curr_readings)
	with open('readings.json', 'w') as f:
		json.dump(readings, f)

print '\n' + '-' * 8
print 'good bye!'
print '-' * 8 + '\n'