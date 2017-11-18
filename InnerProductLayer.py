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

from System.Collections.Generic import *
from MathNet.Numerics.LinearAlgebra import *
from MathNet.Numerics.LinearAlgebra.Double import *
from MathNet.Numerics import *

class InnerProductLayer(Layer):
	def get_WeightMatrix(self):
		return self._weightMatrix_

	WeightMatrix = property(fget=get_WeightMatrix)

	def get_InterceptVector(self):
		return self._interceptVector_

	InterceptVector = property(fget=get_InterceptVector)

	def __init__(self, index, weights, intercepts, inputCoordinates):

	def __init__(self, index, weights, intercepts, inputCoordinates):

	def __init__(self, index, weights, intercepts, inputCoordinates):

	def EvaluateConcrete(self, v):
		return (self._weightMatrix_ * v + self._interceptVector_)

	def Instrument(self, instr, input, output):
		instr[Index] = Instrumentation.NoInstrumentation()

	def EvaluateSymbolic(self, state, input):
		output = Array.CreateInstance(LPSTerm, OutputDimension)
		i = 0
		while i < OutputDimension:
			output[i] = self.doInnerProduct(state, input, self._weightMatrixRows_[i])
			output[i].Add(self._interceptVector_[i])
			i += 1
		return output

	def doInnerProduct(self, state, vs, ds):
		result = LPSTerm.Const(0.0)
		i = 0
		while i < vs.Length:
			result.AddMul(vs[i], ds[i])
			i += 1
		return result

	def IsAffine(self):
		return True