'''
Regulator Feedback Optimizer
RG 2022
'''

from eseries import *
from math import inf

vout_target = 4.35
r_tolerance_rel = 0.01
R1 = 10000
R2 = 1600

VREF_LOW  = 0.597
VREF_NOM  = 0.6
VREF_HIGH = 0.603

delta_T = 100 # temp rise
TCR = 200e-6 # 1 / K

use_temperature = True



def r_temperature(temp_rise):
	'''
	returns resistance deviation from reference
	temperature given temperature rise
	return 0 to ignore
	'''
	if not use_temperature:
		return 0

	alpha = 400e-6
	beta  = 0

	return alpha * temp_rise + beta * temp_rise * temp_rise

def v_out (R1, R2, VREF):
	return VREF + VREF * R1 / R2

def get_error(R1, R2):
	pass

def get_error_brute_force():
	lowest_vout = inf
	highest_vout = -inf
	for i in [-1, 1]:
		for k in [-1, 1]:
			for p in [0, 1, 2]:
				print(r_temperature(delta_T))
				r1_t = R1 * (1 + i * r_tolerance_rel) * (1 + r_temperature(delta_T)) # assuming PTC at this point
				r2_t = R2 * (1 + k * r_tolerance_rel) * (1 + r_temperature(delta_T))
				vref_t = (VREF_LOW, VREF_NOM, VREF_HIGH)[p]
				o = v_out(r1_t, r2_t, vref_t)
				if o < lowest_vout:
					lowest_vout = o
				if o > highest_vout:
					highest_vout = o
	return (lowest_vout, highest_vout)

def print_deviation(nom, val, label):
	e_abs = nom - val
	e_rel = e_abs / nom
	print('%s: %.3f (%.3f / %.3f)' % (label, val, e_abs, e_rel))

def main():
	nom = v_out(R1, R2, VREF_NOM)
	(low, high) = get_error_brute_force()

	print('nom: %.3f' % nom)
	print_deviation(nom, low, 'low')
	print_deviation(nom, high, 'high')

if __name__ == "__main__":
	main()
