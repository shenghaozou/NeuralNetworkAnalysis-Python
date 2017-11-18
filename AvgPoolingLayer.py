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

class AvgPoolingLayer(PoolingLayer):
	def __init__(self, index, inputCoordinates, kernelDimension, padding, stride):
		pass
	def Instrument(self, instr, input, output):
		instr[Index] = Instrumentation.NoInstrumentation()

	def ApplyKernelConcrete(self, instr, input, outIndex, channel, row, column):
		return self.ApplyKernel(input, channel, row, column)

	def ApplyKernelSymbolic(self, state, input, outIndex, channel, row, column):
		return self.ApplyKernel(input, channel, row, column)

	def ApplyKernel(self, input, channel, row, column):
		sum = .Const(0.0)
		count = 1
		i = 0
		while i < KernelDimension:
			j = 0
			while j < KernelDimension:
				x = row - Padding + i
				y = column - Padding + j
				if x >= InputCoordinates.RowCount or y >= InputCoordinates.ColumnCount:
					continue
				index = InputCoordinates.GetIndex(channel, x, y)
				if index < 0 or index >= input.Count:
					continue
				.Add(, input[index])
				count += 1
				j += 1
			i += 1
		.Mul(, 1.0 / count)
		return sum

	def IsAffine(self):
		return True