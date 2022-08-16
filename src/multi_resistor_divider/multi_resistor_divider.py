'''
3 resistor divider (actually any number resistor divider)
RG 2022
specify output voltages (ref. to GND) and get the dividing resistances

dependencies:
	eseries
to install, run:
	python -m pip install eseries

TODO:
- [ ] error calculation / optimization
- [DONE] include multiple decades
'''

from eseries import *
from math import inf
import itertools

v_in = 5.0
v_divided = [3.3, 1.5, 1.1] # input any number of voltages from high to low, e.g. [4.2, 2.8]
N = len(v_divided) + 1

# min max values for resistors
R_LOW  = 1e3
R_HIGH = 100e3

ser = E48
r_tolerance = tolerance(ser)

def v_res (r_list, index):
	# voltage ACROSS resistor (not to GND)
	return v_in * r_list[index] / sum(r_list)

def v_out (r_list, index):
	# voltage referenced to GND
	# output indexing starts at 1
	v_upper = 0
	i = 0
	for r in r_list[0:(index)]:
		v_upper += v_res(r_list, i)
		i += 1
	return v_in - v_upper

def v_out_list (r_list):
	v_list = []
	for i in range(1, len(r_list)):
		v_list.append(v_out(r_list, i))
	return v_list # length N - 1

def v_errors(v_list):
	return [x1 - x2 for (x1, x2) in zip(v_divided, v_list)]

def sum_of_squares(list):
	return sum(i*i for i in list)

def get_resistor_solution():
	#s = series(ser)
	# cartesian product
	resistors = erange(ser, R_LOW, R_HIGH) # TODO: may need to adjust
	r_product = itertools.product(resistors, repeat = N)
	errors = [inf] * N
	best_sos = inf # best sum of squares
	best_resistors = None

	for r_list in r_product:
		v_list = v_out_list(r_list) # length N - 1
		errors = v_errors(v_list)
		sos = sum_of_squares(errors)
		if sos < best_sos:
			best_sos = sos
			best_resistors = r_list

	return best_resistors

def main():
	if len(v_divided) > 1:
		if v_divided[0] < v_divided[1]:
			print('node 1 voltage should be higher than node 2 voltage')
			return

	res = get_resistor_solution()
	l = v_out_list(res)
	print(l)
	#print(l[0] * 2)
	#print(l[1] * 2)
	print(res)

if __name__ == "__main__":
	main()
