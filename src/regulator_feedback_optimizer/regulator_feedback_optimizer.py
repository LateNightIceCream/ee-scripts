'''
Regulator Feedback Optimizer
RG 2022
''' 

from eseries import *
from math import inf

v_out_target = 9.0
ser = E24
must_be_greater = False
r_tolerance = tolerance(ser)
# print all results with error less than min_error
min_error = 0.1

def v_out (R1, R2):
	VREF = 1.245
	return VREF + (VREF*R1/R2)

def get_worst_case_vout (R1, R2):
	vout_p = 0
	vout_n = inf

	for i in range(-1,1):
		r1 = R1 * ( 1 +  i * r_tolerance) # tolerance is relative
		for k in range(-1, 1):
			r2 = R2 * ( 1 + k * r_tolerance)
			vout = v_out(r1, r2)

			if vout > vout_p:
				vout_p = vout
			if vout < vout_n:
				vout_n = vout
	return (vout_n, vout_p)

def print_results (R1, R2, Vout, err, vout_min, vout_max):
	print("-------------------------------------------------------")
	print("R1 = " + str(R1) + ", R2 = " + str(R2))
	print("V_out     = " + str(Vout))
	print("Error     = " + str(err))
	print("V_out_min = " + str(vout_min))
	print("V_out_max = " + str(vout_max))
	print("tol+      = " + str(vout_max - Vout))
	print("tol-      = " + str(vout_min - Vout))

def main():
	s = series(ser)
	smallest_error = inf
	for r1 in s:
		for r2 in s:
			vout  = v_out(r1, r2)

			if must_be_greater and vout < v_out_target:
				continue

			vout_tol = get_worst_case_vout(r1, r2)
			error = abs(v_out_target - vout)

			if error < min_error:
				print_results(r1, r2, vout, error, vout_tol[0], vout_tol[1])
				if error < smallest_error:
					print("=========== new optimal solution! ===========")
					smallest_error = error

if __name__ == "__main__":
	main()