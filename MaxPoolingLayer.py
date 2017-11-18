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
from System.Linq import *
from System.Text import *
from System.Threading.Tasks import *
from MathNet.Numerics.LinearAlgebra import *
from MathNet.Numerics.LinearAlgebra.Double import *

class MaxPoolingLayer(PoolingLayer):
	def __init__(self, index, inputCoordinates, kernelDimension, padding, stride):
		pass
	def Instrument(self, instrumentation, input, output):
		instrumentation[Index] = Instrumentation.MaxPoolingInstrumentation(Array.CreateInstance(int, OutputDimension))
		self.ApplyKernels(instrumentation, ApplyKernelConcrete, input)

	def ApplyKernelConcrete(self, instr, input, outIndex, channel, row, column):
		argMax = InputCoordinates.GetIndex(channel, row, column)
		max = input[argMax]
		i = 0
		while i < KernelDimension:
			j = 0
			while j < KernelDimension:
				if i == 0 and j == 0:
					continue
				x = row - Padding + i
				y = column - Padding + j
				if x >= InputCoordinates.RowCount or y >= InputCoordinates.ColumnCount:
					continue
				index = InputCoordinates.GetIndex(channel, x, y)
				if index < 0 or index >= input.Count:
					continue
				if max < input[index]:
					argMax = index
					max = input[index]
				j += 1
			i += 1
		if instr != None:
			instr[Index].Selections[outIndex] = argMax
		return max

	def ApplyKernelSymbolic(self, state, input, outIndex, channel, row, column):
		selections = state.Instrumentation[Index].Selections
		maxIndex = selections[outIndex]
		maxInput = input[maxIndex]
		i = 0
		while i < KernelDimension:
			j = 0
			while j < KernelDimension:
				x = row - Padding + i
				y = column - Padding + j
				if x >= InputCoordinates.RowCount or y >= InputCoordinates.ColumnCount:
					continue
				curIndex = InputCoordinates.GetIndex(channel, x, y)
				if curIndex == maxIndex:
					continue
				if curIndex < 0 or curIndex >= input.Length:
					continue
				# maxInput - input[curIndex] >= 0 
				t = LPSTerm.Const(0.0)
				t.Add(maxInput)
				t.AddMul(input[curIndex], -1.0)
				state.DeferredCts.And(t, InequalityType.GE)
				j += 1
			i += 1
		return maxInput

	def IsAffine(self):
		return False