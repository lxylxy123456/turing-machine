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
	Runs DFAs and TMs defined in libMachines.py
'''

import os, sys, json, itertools
from libMachines import __getattribute__ as get_machine

def pick_set(s) :
	return next(iter(s))

class AbstractMachine :
	def __init__(self, desc=None, **args) :
		if desc :
			assert not args
			args = desc
		assert set(args) == set(self.fields)
		for k, v in args.items() :
			self.__setattr__(k, v)
	def copy(self) :
		args = dict(zip(self.fields, map(self.__getattribute__, self.fields)))
		return self.__class__(args)	

class DFA(AbstractMachine) :
	fields = ('Sigma', 'Q', 'q0', 'F', 'delta')
	def to_graphviz(self) :
		d = json.dumps
		ans = []
		ans.append('digraph G {')
		ans.append('\trankdir = LR; start [width=0, height=0, label="", style='
					'invis]; ')
		ans.append('\tstart -> %s' % d(self.q0))
		for i in self.Q :
			if i in self.F :
				ans.append('\t%s[peripheries=2]; ' % d(i))
			else :
				ans.append('\t%s; ' % d(i))
		for (k, c), v in self.delta.items() :
			ans.append('\t%s -> %s [label=%s]; ' % tuple(map(d, (k, v, c))))
		ans.append('}')
		return '\n'.join(ans)
	def run(self, w, show_proc=False) :
		cur = self.q0
		state_list = [cur]
		for i in w :
			cur = self.delta[(cur, i)]
			state_list.append(cur)
		if show_proc :
			print(' '.join(map(str, state_list)))
			print(' ' + ' '.join(map(str, w)))
		return cur in self.F
	def minimize(self, combine_name=pick_set) :
		Q = set(self.Q)
		F = set(self.F)
		N = Q - F
		Pi = [[F, len(F) >= len(N)], [N, len(F) < len(N)]]	# [part, is_in_L]
		flag = True
		while flag :
			flag = False	# whether encounters "is_in_L = 1"
			for sndex, (S, s_in_L) in enumerate(Pi) :
				if not s_in_L :
					continue
				flag = True
				assert Pi[sndex][0] == S
				Pi[sndex][1] = False
				for c in self.Sigma :
					for cndex, (C, c_in_L) in enumerate(Pi.copy()) :
						Cp = set(filter(lambda x: self.delta[(x, c)] in S, C))
						Cn = C - Cp
						if Cp and Cn :
							assert Pi[cndex] == [C, c_in_L]
							Pi[cndex] = [Cp, len(Cp) <  len(Cn)]
							Pi.append(  [Cn, len(Cp) >= len(Cn)])
		Q = set(self.Q)
		F = set(self.F)
		for S, is_in_L in Pi :
			name = combine_name(S)
			s = pick_set(S)
			D = S - {s}
			Q -= S
			Q.add(name)
			if s in F :
				F -= S
				F.add(name)
			if self.q0 in S :
				self.q0 = name
			for (q, c), v in list(self.delta.items()) :
				if q in S :
					self.delta.__delitem__((q, c))
					if q == s :
						if v in S :
							self.delta[(name, c)] = name
						else :
							self.delta[(name, c)] = v
					else :
						continue
				elif v in S :
					self.delta[(q, c)] = name
		self.Q = tuple(Q)
		self.F = tuple(F)

class Tape :
	def __init__(self, default, left=[], right=[], pos=0) :
		# right includes current position
		self.default = default
		self.left = list(left)
		self.right = list(right)
		if not right :
			self.right.append(self.default)
		self.pos = pos
	def copy(self) :
		return self.__class__(self.default, self.left, self.right, self.pos)
	def __str__(self, l_len=None, r_len=None, fmt=None) :
		if fmt == None :
			fmt = ('\033[31;1m', '\033[0m', '')
		ans = ''
		content = ''
		if l_len != None :
			content += str(self.default) * (l_len - len(self.left))
		content += ''.join(map(str, self.left))
		pos = len(content) + self.pos
		content += ''.join(map(str, self.right))
		if r_len != None :
			content += str(self.default) * (r_len - len(self.right))
		ans = ''
		if pos :
			ans += fmt[2] + fmt[2].join(content[:pos])
		ans += fmt[0] + content[pos] + fmt[1]
		if pos != len(content) - 1 :
			ans += fmt[2].join(content[pos+1:]) + fmt[2]
		return ans
	def move(self, offset) :
		self.pos += offset
		if self.pos >= 0 :
			if self.pos >= len(self.right) :
				self.right.append(self.default)
		else :
			if -self.pos > len(self.left) :
				self.left.insert(0, self.default)
	def read(self) :
		if self.pos >= 0 :
			return self.right[self.pos]
		else :
			return self.left[self.pos]
	def write(self, c) :
		if self.pos >= 0 :
			self.right[self.pos] = c
		else :
			self.left[self.pos] = c

class TM(AbstractMachine) :
	'L = -1; C = 0; R = 1; '
	fields = ('Q', 'Gamma', 'b', 'Sigma', 'q0', 'F', 'R', 'delta')
	def to_graphviz(self) :
		d = json.dumps
		ans = []
		ans.append('digraph G {')
		ans.append('\trankdir = LR; start [width=0, height=0, label="", style='
					'invis]; ')
		ans.append('\tstart -> %s' % d(self.q0))
		ans.append('\tsubgraph cluster_F {')
		for i in self.F :
			ans.append('\t\t%s; ' % d(i))
		ans.append('\t\tlabel="Accept"\n\t}')
		ans.append('\tsubgraph cluster_R {')
		for i in self.R :
			ans.append('\t\t%s; ' % d(i))
		ans.append('\t\tlabel="Reject"\n\t}')
		for (k1, k2), (v1, v2, v3) in self.delta.items() :
			ans.append('\t%s -> %s [label="%s → %s, %s"]; ' % 
						(d(k1), d(v1), str(k2), str(v2), 
							{-1: 'L', 0: 'C', 1: 'R'}[v3]))
		ans.append('}')
		return '\n'.join(ans)
	def run(self, w, show_proc=False, count=itertools.count(0), fmt=None) :
		cur = self.q0
		proc = []
		ans = None
		for index in count :
			if show_proc :
				proc.append((cur, w.copy()))
			if cur in self.F : ans = True; break
			if cur in self.R : ans = False; break
			key = (cur, w.read())
			if key not in self.delta :
				break
			q, c, m = self.delta[key]	# state, char, move
			cur = q
			w.write(c)
			w.move(m)
		if show_proc :
			l_len = len(w.left)
			r_len = len(w.right)
			for i, j in proc :
				print(i, j.__str__(l_len, r_len + 1, fmt=fmt), sep='\t')
		return ans, index, w

if __name__ == '__main__' :
	typ, name = sys.argv[1].split('_', 1)
	if typ == 'DFA' :
		d = DFA(get_machine('DFA_' + name))
		w = list(map(int, '10010101010'))
		if 0 :
			print(d.run(w, True))
		else :
			# d.minimize('_'.join)
			print(d.to_graphviz())
	elif typ in ('TM', 'TT') :
		t = TM(get_machine('TM_' + name))
		if 0 :	# TM_HW6_2
			for i in range(0, 8) :
				print('\nnum_of_0s = %d' % i)
				a, i, w = t.run(Tape('_', '', '0' * i), True, 
								fmt=('(', ')', ' '))
			exit(0)
		if 1 :
			a, i, w = t.run(Tape(*get_machine('TT_' + name)), True)
			print(a, i, w.__str__(None, None), sep='\t')
		else :
			print(t.to_graphviz())
	else :
		raise ValueError

