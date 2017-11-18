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

class PoolingLayer(Layer):
	def get_KernelDimension(self):
		return self._kernelDimension_

	KernelDimension = property(fget=get_KernelDimension)

	def get_Padding(self):
		return self._padding_

	Padding = property(fget=get_Padding)

	def get_Stride(self):
		return self._stride_

	Stride = property(fget=get_Stride)

	def __init__(self, index, inputCoordinates, kernelDimension, padding, stride):
		self._inputCoordinates_ = inputCoordinates
		self._kernelDimension_ = kernelDimension
		self._padding_ = padding
		self._stride_ = stride
		inputDimension = self._inputCoordinates_.ChannelCount * self._inputCoordinates_.RowCount * self._inputCoordinates_.ColumnCount
		rowCount = Utils.UImageCoordinate.ComputeOutputCounts(kernelDimension, inputCoordinates.RowCount, stride, padding, True)
		columnCount = Utils.UImageCoordinate.ComputeOutputCounts(kernelDimension, inputCoordinates.ColumnCount, stride, padding, True)
		outputDimension = inputCoordinates.ChannelCount * rowCount * columnCount
		ouputCoordinates = ImageCoordinates(inputCoordinates.ChannelCount, rowCount, columnCount)
		self.InitLayer(index, LayerType.POOLING_LAYER, inputDimension, outputDimension, inputCoordinates, ouputCoordinates)

	def ApplyKernelConcrete(self, instr, input, outIndex, channel, row, column):
		pass

	def ApplyKernelSymbolic(self, state, input, outIndex, channel, row, column):
		pass

	def ApplyKernels(self, state, applyKernel, input):
		output = .CreateVector(OutputDimension)
		stride = self.Stride
		jbound = Utils.UImageCoordinate.ComputeOutputCounts(self.KernelDimension, InputCoordinates.RowCount, self.Stride, self.Padding, True)
		kbound = Utils.UImageCoordinate.ComputeOutputCounts(self.KernelDimension, InputCoordinates.ColumnCount, self.Stride, self.Padding, True)
		i = 0
		while i < InputCoordinates.ChannelCount:
			j = 0
			while j < jbound:
				k = 0
				while k < kbound:
					index = OutputCoordinates.GetIndex(i, j, k)
					value = self.applyKernel(state, input, index, i, j * stride, k * stride)
					output[index] = value
					k += 1
				j += 1
			i += 1
		return output

	def EvaluateSymbolic(self, state, input):
		return self.ApplyKernels(state, ApplyKernelSymbolic, input)

	def EvaluateConcrete(self, input):
		return self.ApplyKernels(None, ApplyKernelConcrete, input)