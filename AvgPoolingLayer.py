class AvgPoolingLayer(PoolingLayer):
	def __init__(self, index, input_Coordinates, kernelDimension, padding, stride):
		super().__init__(index, input_Coordinates, kernelDimension, padding, stride)

	def Instrument(self, instr, input_, output):
		raise NotImplementedError("Instrumentation")
		instr[Index] = Instrumentation.NoInstrumentation()

	def ApplyKernelConcrete(self, instr, input_, outIndex, channel, row, column):
		return self.ApplyKernel(input_, channel, row, column)

	def ApplyKernelSymbolic(self, state, input_, outIndex, channel, row, column):
		return self.ApplyKernel(input_, channel, row, column)

	def ApplyKernel(self, input_, channel, row, column):
		sum_ = 0.0
		count = 1
		i = 0
		while i < KernelDimension:
			j = 0
			while j < KernelDimension:
				x = row - Padding + i
				y = column - Padding + j
				if x >= InputCoordinates.R or y >= InputCoordinates.ColumnCount:
					continue
				index = InputCoordinates.GetIndex(channel, x, y)
				if index < 0 or index >= input_.Count:
					continue
				sum_ += input_[index]
				raise NotImplementedError("Plz confirm")
				count += 1
				j += 1
			i += 1
		sum_ *= (1.0 / count)
		raise NotImplementedError("What is .?")
		return sum_

	def IsAffine(self):
		return True