# --------------------------------------------------------------------------------------------------
# Neural Network Analysis Framework
#
# Copyright(c) Microsoft Corporation
# All rights reserved.
#
# MIT License
#  
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
#  associated documentation files (the "Software"), to deal in the Software without restriction,
#  including without limitation the rights to use, copy, modify, merge, publish, distribute,
#  sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#  
#  The above copyright notice and this permission notice shall be included in all copies or
#  substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
#  NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# --------------------------------------------------------------------------------------------------

from System.Collections import *
from System.Collections.Generic import *
from System.Text import *
from System.Diagnostics import *

class InequalityType(object):
	""" <summary>
	 Constraint operator
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 Constraint operator
		 </summary>
		"""

class LPSConstraint(object):
	""" <summary>
	 If x = Term, op = Inequality, represents  x `op` 0
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 If x = Term, op = Inequality, represents  x `op` 0
		 </summary>
		"""
 # default = false. Have we added this constraint to the solver? No. Yikes.
class LPSConstraints(IEnumerable):
	""" <summary>
	 A simple (list-implemented) set of constraints and inequalities that
	 encode an LP instance. The list-based implementation exists because 
	 we only iterate/insert. If we need more, make sure to optimize this!
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 A simple (list-implemented) set of constraints and inequalities that
		 encode an LP instance. The list-based implementation exists because 
		 we only iterate/insert. If we need more, make sure to optimize this!
		 </summary>
		"""
		# To support O(1) extension
		self._constraints_ = List[LPSConstraint]()
		# To support O(1) union 
		self._unioned_ = List[LPSConstraints]()
		self._constraintCount_ = 0

	def And(self, s):
		self._unioned_.Add(s)
		self._constraintCount_ += s.constraintCount_

	def And(self, term, inequality):
		self._constraints_.Add(LPSConstraint(Inequality = inequality, Term = term))
		self._constraintCount_ += 1

	# (left `binop` right), equivalently: (left - right `binop` 0)
	# NB: Allocates, does not overwrite the left or right term.
	def And(self, left, inequality, right):
		t = LPSTerm.Const(0.0)
		t.Add(left)
		t.AddMul(right, -1.0)
		self.And(t, inequality)

	def get_Count(self):
		return self._constraintCount_

	Count = property(fget=get_Count)

	def GetEnumerator(self):
		enumerator = constraints_.GetEnumerator()
		while enumerator.MoveNext():
			o = enumerator.Current
		enumerator = unioned_.GetEnumerator()
		while enumerator.MoveNext():
			s = enumerator.Current
			enumerator = s.constraints_.GetEnumerator()
			while enumerator.MoveNext():
				o = enumerator.Current

	def ToList(self):
		ret = List[LPSConstraint](self._constraints_)
		enumerator = unioned_.GetEnumerator()
		while enumerator.MoveNext():
			s = enumerator.Current
			enumerator = s.constraints_.GetEnumerator()
			while enumerator.MoveNext():
				o = enumerator.Current
				ret.Add(o)
		return ret