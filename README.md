# turing-machine
Python implementation of DFA and Turing Machine

## files

### libMachines.py
* Some DFA and TM collections
	* DFA_3mod: x % 3 == 0
	* TM_1st: prints "0 1 0 1 0 1..."
	* TM_cp: Copies "111" to "1110111"
	* TM_bb1: 1-state, 2-symbol busy beaver
	* TM_bb2: 2-state, 2-symbol busy beaver
	* TM_bb3: 3-state, 2-symbol busy beaver
	* TM_bb4: 4-state, 2-symbol busy beaver
	* TM_bb5: 5-state, 2-symbol busy beaver (takes a long time)
	* TM_bb6: 6-state, 2-symbol busy beaver (takes a long time)
	* TM_HW5_3: Turing machine in a homework problem
	* TM_HW6_2: Turing machine in another homework problem
	* TM_Enum: An enumerator for UTM
	* TM_Enum2: A simplified enumerator for UTM
* To add a TM
	* Use `TM_name` to define the machine; use `TT_name` to define the tape

### Machines.py
* To run a DFA
	* `python3 Machines.py DFA_name`
* To run a TM
	* `python3 Machines.py TM_name`

## Ultilization
* Admittedly, the documentation of this project is poor. please search `if 0 :` and `if 1 :` through `Machines.py` to develop features not explicitly shown. 

