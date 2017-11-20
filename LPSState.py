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


class DisjunctionChoice(object):
	def __init__(self):

class DCSComparer(IEqualityComparer):
	def Equals(self, a, b):
		return Instrumentation.EqualDisjunctionChoices(a, b)

	def GetHashCode(self, a):
		ret = 0
		i = 0
		while i < a.Length:
			if a[i] == DisjunctionChoice.ACTIVE:
				ret += 1
			i += 1
		return ret

class Instrumentation(object): # RELU # MAXPOOLING
	def __init__(self):
		self._DisjunctionConstraints = None
		self._Selections = None
		self._DCLog = Dictionary[KeyValuePair, List]()
		self._Collisions = 0

	def EqualDisjunctionChoices(a, b):
		i = 0
		while i < Math.Min(a.Length, b.Length):
			if a[i] != b[i]:
				return False
			i += 1
		return True

	EqualDisjunctionChoices = staticmethod(EqualDisjunctionChoices)

	def DisjunctionChoiceStr(dc):
		if dc == DisjunctionChoice.ACTIVE:
			return "A"
		elif dc == DisjunctionChoice.INACTIVE:
			return "I"
		elif dc == DisjunctionChoice.EITHER:
			return "E"
		else:
			raise Exception("FlipDisjunctionChoice: can't happen")

	DisjunctionChoiceStr = staticmethod(DisjunctionChoiceStr)

	def InitReLULogging():
		self._DCLog = Dictionary[KeyValuePair, List]()
		self._Collisions = 0

	InitReLULogging = staticmethod(InitReLULogging)

	def LogDisjunctionChoices(fn, layeridx, dcs):
		hash = DCSComparer().GetHashCode(dcs)
		idx = KeyValuePair[int, int](layeridx, hash)
		if self._DCLog.ContainsKey(idx):
			entries = self._DCLog[idx]
			for e in entries:
			while enumerator.MoveNext():
				entry = enumerator.Current
				if Instrumentation.EqualDisjunctionChoices(dcs, entry):
					self._Collisions += 1
					return 
			entries.append(dcs)
		else:
			self._DCLog[idx] = []
			self._DCLog[idx].append(dcs)

	LogDisjunctionChoices = staticmethod(LogDisjunctionChoices)

	def FlipDisjunctionChoice(dc):
		if dc == DisjunctionChoice.ACTIVE:
			return DisjunctionChoice.INACTIVE
		elif dc == DisjunctionChoice.INACTIVE:
			return DisjunctionChoice.ACTIVE
		elif dc == DisjunctionChoice.EITHER:
			return DisjunctionChoice.EITHER
		else:
			raise Exception("FlipDisjunctionChoice: can't happen")

	FlipDisjunctionChoice = staticmethod(FlipDisjunctionChoice)

	def ReLUInstrumentation(choices):
		ret = Instrumentation()
		ret.LayerType = self._LayerType.RECTIFIED_LINEAR
		ret.DisjunctionConstraints = choices
		ret.Selections = None
		return ret

	ReLUInstrumentation = staticmethod(ReLUInstrumentation)

	def MaxPoolingInstrumentation(choices):
		ret = Instrumentation()
		ret.LayerType = self._LayerType.POOLING_LAYER
		ret.DisjunctionConstraints = None
		ret.Selections = choices
		return ret

	MaxPoolingInstrumentation = staticmethod(MaxPoolingInstrumentation)

	def NoInstrumentation():
		ret = Instrumentation()
		return ret

	NoInstrumentation = staticmethod(NoInstrumentation)

class NNInstrumentation(Dictionary):
	pass

class LPSState(object):
	# The ones we cache for a different round of CEGAR
	# The ones we collect as we interpret
	# NB: null for the layers where we have no instrumentation
	def get_Instrumentation(self):
		return self._instrumentation_

	Instrumentation = property(fget=get_Instrumentation)

	def get_Origin(self):
		return self._origin_

	Origin = property(fget=get_Origin)

	def ClearConstraints(self):
		self._deferredConstraints_ = LPSConstraints()
		self._currentConstraints_ = LPSConstraints()

	def get_CurrentCts(self):
		return self._currentConstraints_

	CurrentCts = property(fget=get_CurrentCts)

	def get_DeferredCts(self):
		return self._deferredConstraints_

	DeferredCts = property(fget=get_DeferredCts)

	def __init__(self, instrumentation, origin):
		self._deferredConstraints_ = LPSConstraints()
		self._currentConstraints_ = LPSConstraints()
		self._instrumentation_ = instrumentation
		self._origin_ = origin