# 
# turing-machine - Python implementation of DFA and Turing Machine
# Copyright (C) 2018  lxylxy123456
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https:#www.gnu.org/licenses/>.
# 

'''
	Some DFA and TM collections
		DFA_3mod: 	x % 3 == 0
		TM_1st: 	prints "0 1 0 1 0 1..."
		TM_cp: 		Copies "111" to "1110111"
		TM_bb1: 	1-state, 2-symbol busy beaver
		TM_bb2: 	2-state, 2-symbol busy beaver
		TM_bb3: 	3-state, 2-symbol busy beaver
		TM_bb4: 	4-state, 2-symbol busy beaver
		TM_bb5: 	5-state, 2-symbol busy beaver (takes a long time)
		TM_bb6: 	6-state, 2-symbol busy beaver (takes a long time)
		TM_HW5_3: 	Turing machine in a homework problem
		TM_HW6_2: 	Turing machine in another homework problem
		TM_Enum: 	An enumerator for UTM
		TM_Enum2: 	A simplified enumerator for UTM
	To run a DFA
		python3 Machines.py DFA_name
	To add a TM
		Use TM_name to define the machine; use TT_name to define the tape
	To run a TM
		python3 Machines.py TM_name
'''

DFA_ = {
	'Sigma': 	(0, ), 
	'Q': 		(0, 1), 
	'q0': 		0, 
	'F': 		(0, ), 
	'delta': 	{
					(0, 0): 1, 
					(1, 0): 0, 
				}, 
}

DFA_3mod = {
	'Sigma': 	(0, 1), 
	'Q': 		('A', 'B', 'C'), 
	'q0': 		'A', 
	'F': 		('A',), 
	'delta': 	{
					('A', 0): 'A', 
					('A', 1): 'B', 
					('B', 0): 'C', 
					('B', 1): 'A', 
					('C', 0): 'B', 
					('C', 1): 'C', 
				}, 
}

DFA_to_min = {
	'Sigma': 	(0, 1), 
	'Q': 		('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'), 
	'q0': 		'a', 
	'F': 		('c',), 
	'delta': 	{
					('a', 0): 'b', 
					('a', 1): 'f', 
					('b', 0): 'g', 
					('b', 1): 'c', 
					('c', 0): 'a', 
					('c', 1): 'c', 
					('d', 0): 'c', 
					('d', 1): 'g', 
					('e', 0): 'h', 
					('e', 1): 'f', 
					('f', 0): 'c', 
					('f', 1): 'g', 
					('g', 0): 'g', 
					('g', 1): 'e', 
					('h', 0): 'g', 
					('h', 1): 'c', 
				}, 
}

L = -1; C = 0; R = 1; 

# https://en.wikipedia.org/wiki/Turing_machine_examples#Turing's_very_first_example
TM_1st = {
	'Q': 		('b', 'c', 'e', 'f'), 
	'Gamma': 	('_', '0', '1'), 
	'b': 		'_', 
	'Sigma': 	('0', '1', ), 
	'q0': 		'b', 
	'F': 		('h'), 
	'R': 		(), 
	'delta': 	{
					('b', '_'): ('c', '0', R), 
					('c', '_'): ('e', '_', R), 
					('e', '_'): ('f', '1', R), 
					('f', '_'): ('b', '_', R), 
				}, 
}
TT_1st = ('_', '', '_' * 50 + '1')

# https://en.wikipedia.org/wiki/Turing_machine_examples#A_copy_subroutine
TM_cp = {
	'Q': 		('s1', 's2', 's3', 's4', 's5', 'H'), 
	'Gamma': 	(0, 1), 
	'b': 		0, 
	'Sigma': 	(1, ), 
	'q0': 		's1', 
	'F': 		('H'), 
	'R': 		(), 
	'delta': 	{
					('s1', 0): ('H', 0, C), 
					('s1', 1): ('s2', 0, R), 
					('s2', 0): ('s3', 0, R), 
					('s2', 1): ('s2', 1, R), 
					('s3', 0): ('s4', 1, L), 
					('s3', 1): ('s3', 1, R), 
					('s4', 0): ('s5', 0, L), 
					('s4', 1): ('s4', 1, L), 
					('s5', 0): ('s1', 1, R), 
					('s5', 1): ('s5', 1, L), 
				}, 
}
TT_cp = (0, [], [1] * 4)

# https://en.wikipedia.org/wiki/Busy_beaver#Examples
TM_bb1 = {
	'Q': 		('A', 'H'), 
	'Gamma': 	(0, 1), 
	'b': 		0, 
	'Sigma': 	(1, ), 
	'q0': 		'A', 
	'F': 		('H'), 
	'R': 		(), 
	'delta': 	{
					('A', 0): ('H', 1, R), 
				}, 
}
TT_bb1 = (0, )

TM_bb2 = {
	'Q': 		('A', 'B', 'H'), 
	'Gamma': 	(0, 1), 
	'b': 		0, 
	'Sigma': 	(1, ), 
	'q0': 		'A', 
	'F': 		('H'), 
	'R': 		(), 
	'delta': 	{
					('A', 0): ('B', 1, R), 
					('A', 1): ('B', 1, L), 
					('B', 0): ('A', 1, L), 
					('B', 1): ('H', 1, R), 
				}, 
}
TT_bb2 = (0, )

# https://en.wikipedia.org/wiki/Turing_machine_examples#3-state_Busy_Beaver
TM_bb3 = {
	'Q': 		('A', 'B', 'C', 'H'), 
	'Gamma': 	(0, 1), 
	'b': 		0, 
	'Sigma': 	(1, ), 
	'q0': 		'A', 
	'F': 		('H'), 
	'R': 		(), 
	'delta': 	{
					('A', 0): ('B', 1, R), 
					('A', 1): ('C', 1, L), 
					('B', 0): ('A', 1, L), 
					('B', 1): ('B', 1, R), 
					('C', 0): ('B', 1, L), 
					('C', 1): ('H', 1, R), 
				}, 
}
TT_bb3 = (0, )

# https://en.wikipedia.org/wiki/Busy_beaver#Examples
TM_bb4 = {
	'Q': 		('A', 'B', 'C', 'D', 'H'), 
	'Gamma': 	(0, 1), 
	'b': 		0, 
	'Sigma': 	(1, ), 
	'q0': 		'A', 
	'F': 		('H'), 
	'R': 		(), 
	'delta': 	{
					('A', 0): ('B', 1, R), 
					('A', 1): ('B', 1, L), 
					('B', 0): ('A', 1, L), 
					('B', 1): ('C', 0, L), 
					('C', 0): ('H', 1, R), 
					('C', 1): ('D', 1, L), 
					('D', 0): ('D', 1, R), 
					('D', 1): ('A', 0, R), 
				}, 
}
TT_bb4 = (0, )

TM_bb5 = {
	'Q': 		('A', 'B', 'C', 'D', 'E', 'H'), 
	'Gamma': 	(0, 1), 
	'b': 		0, 
	'Sigma': 	(1, ), 
	'q0': 		'A', 
	'F': 		('H'), 
	'R': 		(), 
	'delta': 	{
					('A', 0): ('B', 1, R), 
					('A', 1): ('C', 1, L), 
					('B', 0): ('C', 1, R), 
					('B', 1): ('B', 1, R), 
					('C', 0): ('D', 1, R), 
					('C', 1): ('E', 0, L), 
					('D', 0): ('A', 1, L), 
					('D', 1): ('D', 1, L), 
					('E', 0): ('H', 1, R), 
					('E', 1): ('A', 0, L), 
				}, 
}
TT_bb5 = (0, )

TM_bb6 = {
	'Q': 		('A', 'B', 'C', 'D', 'E', 'F', 'H'), 
	'Gamma': 	(0, 1), 
	'b': 		0, 
	'Sigma': 	(1, ), 
	'q0': 		'A', 
	'F': 		('H'), 
	'R': 		(), 
	'delta': 	{
					('A', 0): ('B', 1, R), 
					('A', 1): ('E', 1, L), 
					('B', 0): ('C', 1, R), 
					('B', 1): ('F', 1, R), 
					('C', 0): ('D', 1, L), 
					('C', 1): ('B', 0, R), 
					('D', 0): ('E', 1, R), 
					('D', 1): ('C', 0, L), 
					('E', 0): ('A', 1, L), 
					('E', 1): ('D', 0, R), 
					('F', 0): ('H', 1, L), 
					('F', 1): ('C', 1, R), 
				}, 
}
TT_bb6 = (0, )

# TM in classes

TM_HW5_3 = {
	'Q': 		('q1', 'q2', 'q3', 'q4', 'q5', 'qA', 'qR'), 
	'Gamma': 	('0', 'x', '_'), 
	'b': 		('_',), 
	'Sigma': 	('0',), 
	'q0': 		'q1', 
	'F': 		('qA',), 
	'R': 		('qR',), 
	'delta': 	{
					('q1', '0'): ('q2', '_', R), 
					('q1', '_'): ('qR', '_', R), 
					('q1', 'x'): ('qR', '_', R), 
					('q2', '0'): ('q3', 'x', R), 
					('q2', '_'): ('qA', '_', R), 
					('q2', 'x'): ('q2', 'x', R), 
					('q3', '0'): ('q4', '0', R), 
					('q3', '_'): ('q5', '_', L), 
					('q3', 'x'): ('q3', 'x', R), 
					('q4', '0'): ('q3', 'x', R), 
					('q4', '_'): ('qR', '_', R), 
					('q4', 'x'): ('q4', 'x', R), 
					('q5', '0'): ('q5', '0', L), 
					('q5', '_'): ('q2', '_', R), 
					('q5', 'x'): ('q5', 'x', L), 
				}, 
}
TT_HW5_3 = ('_', '', '0' * 6)

TM_HW6_2 = {
	'Q': 		('q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'qA', 'qR'), 
	'Gamma': 	('0', 'x', 'y', 'z', '_'), 
	'b': 		('_',), 
	'Sigma': 	('0',), 
	'q0': 		'q1', 
	'F': 		('qA',), 
	'R': 		('qR',), 
	'delta': 	{
					('q1', '0'): ('q2', '_', R), 
					('q1', '_'): ('qR', '_', R), 
					('q1', 'x'): ('qR', 'x', R), 
					('q1', 'y'): ('qR', 'y', R), 
					('q1', 'z'): ('qR', 'z', R), 
					('q2', '0'): ('q3', 'z', L), 
					('q2', '_'): ('q5', '_', R), 	# Consumed correctly
					('q2', 'x'): ('q2', 'x', R), 
					('q2', 'y'): ('qR', 'y', R), 
					('q2', 'z'): ('qR', 'z', R), 
					('q3', '0'): ('qR', '0', R), 
					('q3', '_'): ('q5', '_', R), 	# Consumed correctly
					('q3', 'x'): ('q4', 'y', R), 
					('q3', 'y'): ('q3', 'y', L), 
					('q3', 'z'): ('q3', 'z', L), 
					('q4', '0'): ('q3', 'z', L), 
					('q4', '_'): ('qR', '_', R), 	# Consumed incorrectly
					('q4', 'x'): ('qR', 'x', R), 
					('q4', 'y'): ('q4', 'y', R), 
					('q4', 'z'): ('q4', 'z', R), 
					('q5', '0'): ('q6', '0', L), 
					('q5', '_'): ('qA', '_', R), 	# Consumed correctly
					('q5', 'x'): ('q5', 'x', R), 
					('q5', 'y'): ('q5', 'x', R), 
					('q5', 'z'): ('q5', 'x', R), 
					('q6', '0'): ('qR', '0', R), 
					('q6', '_'): ('q2', '_', R), 
					('q6', 'x'): ('q6', 'x', L), 
					('q6', 'y'): ('qR', 'y', R), 
					('q6', 'z'): ('qR', 'z', R), 
				}, 
}
TT_HW6_2 = ('_', '', '0' * 2)

TM_Enum = {
	'Q': 		('q0', 'q1', 'q2'), 
	'Gamma': 	('$', '1', '2', '3', '_'), 
	'b': 		('_',), 
	'Sigma': 	('1', 'X'), 
	'q0': 		'q0', 
	'F': 		(), 
	'R': 		(), 
	'delta': 	{
					('q0', '$'): ('q1', '$', R), 	# output state
					('q1', '1'): ('q2', '2', L), 
					('q1', '2'): ('q2', '3', L), 
					('q1', '3'): ('q1', '1', R), 
					('q1', '_'): ('q2', '1', L), 
					('q2', '1'): ('q2', '1', L), 
					('q2', '2'): ('q2', '2', L), 
					('q2', '3'): ('q2', '3', L), 
					('q2', '$'): ('q0', '$', C), 
				}, 
}
TT_Enum = ('_', '', '$1' + '_' * 3 + 'X')

TM_Enum2 = {
	'Q': 		('q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'qA', 'qR'), 
	'Gamma': 	('$', '1', '2', '3', 'X', '_'), 
	'b': 		('_',), 
	'Sigma': 	('1', 'X'), 
	'q0': 		'q1', 
	'F': 		(), 
	'R': 		(), 
	'delta': 	{
					('q1', '_'): ('q2', '$', R), 
					('q2', '1'): ('q2', '1', R), 
					('q2', '2'): ('q2', '1', R), 
					('q2', '3'): ('q2', '1', R), 
					('q2', '_'): ('q3', '1', C), 
					('q3', '1'): ('q3', '2', C), 	# q3: output state
					('q3', '2'): ('q3', '3', C), 
					('q3', '3'): ('q4', '3', C), 
					('q4', '1'): ('q5', '2', R), 
					('q4', '2'): ('q5', '3', R), 
					('q4', '3'): ('q4', '3', L), 
					('q4', '$'): ('q2', '$', R), 
					('q5', '1'): ('q5', '1', R), 
					('q5', '2'): ('q5', '1', R), 
					('q5', '3'): ('q5', '1', R), 
					('q5', '_'): ('q3', '_', L), 
				}, 
}
TT_Enum2 = ('_', '', '_' * 5 + 'X')

