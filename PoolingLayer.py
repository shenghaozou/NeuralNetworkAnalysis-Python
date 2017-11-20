

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