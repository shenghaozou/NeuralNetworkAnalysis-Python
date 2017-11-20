
class MaxPoolingLayer(PoolingLayer):
	def __init__(self, index, inputCoordinates, kernelDimension, padding, stride):
		pass
	def Instrument(self, instrumentation, input, output):
		instrumentation[Index] = Instrumentation.MaxPoolingInstrumentation([None] * OutputDimension)
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
				t.append(maxInput)
				t.AddMul(input[curIndex], -1.0)
				state.DeferredCts.And(t, InequalityType.GE)
				j += 1
			i += 1
		return maxInput

	def IsAffine(self):
		return False