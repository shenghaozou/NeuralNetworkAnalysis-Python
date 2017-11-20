from enum import Enum
class InequalityType(Enum):
	EQ = 1
	GE = 2
	GT = 3
	LE = 4
	LT = 5

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
		pass

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
		self._constraints_ = [None] * 
		# To support O(1) union 
		self._unioned_ = [None] * 
		self._constraintCount_ = 0

	def And(self, s):
		self._unioned_.append(s)
		self._constraintCount_ += s.constraintCount_

	def And(self, term, inequality):
		self._constraints_.append(LPSConstraint(Inequality = inequality, Term = term))
		self._constraintCount_ += 1

	# (left `binop` right), equivalently: (left - right `binop` 0)
	# NB: Allocates, does not overwrite the left or right term.
	def And(self, left, inequality, right):
		t = LPSTerm.Const(0.0)
		t.append(left)
		t.AddMul(right, -1.0)
		self.And(t, inequality)

	def get_Count(self):
		return self._constraintCount_

	Count = property(fget=get_Count)

	def GetEnumerator(self):
		raise NotImplementedError("not sure")
		for e in self._constraints_:
			yield o
		for o in self._unioned_:
			for e in e._constraints_:
				yield o

	def ToList(self):
		raise NotImplementedError("not sure")
		ret = self._constraints_[:]
		for e in self._unioned_:
			for o in e._constraints_:
				ret.append(o)
		return ret