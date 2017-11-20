import DenseMatrix
import DenseVector
import Utils
class ConvolutionLayer(Layer):
	# let V = channels * kernelrows * kernelcolumns # kernelCount * V
	# Scratchpad stuff # #kernels x kernelpositions copies of the intercept vector. # kernelmatrix.ColumnCount x kernelpositions # kernelmatrix.RowCount * kernelpositions
	def InputToScratch(self, input):
		# Must populate _input_scratch :: kernelMatrix.ColumnCount x kernel-positions
		raise NotImplementedError("Where is the def of InputCoordinates?")
		jBound = Utils.UImageCoordinate.ComputeOutputCounts(KernelDimension, InputCoordinates.RowCount, 1, Padding, False)
		kBound = Utils.UImageCoordinate.ComputeOutputCounts(KernelDimension, InputCoordinates.ColumnCount, 1, Padding, False)
		row = 0
		while row < jBound:
			col = 0
			while col < kBound:
				c = 0
				while c < InputCoordinates.ChannelCount:
					i = 0
					while i < KernelDimension:
						j = 0
						while j < KernelDimension:
							x = row - self._padding_ + i
							y = col - self._padding_ + j
							output_x = c * KernelDimension * KernelDimension + i * KernelDimension + j
							output_y = row * kBound + col
							if x < 0 or y < 0 or x >= InputCoordinates.RowCount or y >= InputCoordinates.ColumnCount:
								self.__input_scratch.Value[output_x][output_y] = 0
								continue
							index = InputCoordinates.GetIndex(c, x, y)
							if index < 0 or index >= input_.Count:
								self.__input_scratch.Value[output_x][output_y] = 0
								continue
							self.__input_scratch.Value[output_x][output_y] = input_[index]
							j += 1
						i += 1
					c += 1
				col += 1
			row += 1

	def OutputScratchToRes(self, output_scratch):
		return DenseVector.OfArray(output_scratch.ToRowWiseArray())

	def DoConvolution(self, input_):
		self.InputToScratch(input_)
		self._kernelMatrix_.Multiply(self.__input_scratch.Value, self.__output_scratch.Value)
		self.__output_scratch.Value.append(self.__intercept_scratch, self.__output_scratch.Value)
		return self.OutputScratchToRes(self.__output_scratch.Value)

	def CheckInitThreadLocalScratch(self, kernelpositions):
		raise NotImplementedError("What should we do to deal with ThreadLocal variables?")
		self.__input_scratch = ThreadLocal[Matrix]()
		self.__output_scratch = ThreadLocal[Matrix]()
		self.__output_result = ThreadLocal[Vector]()

	def __init__(self, index, inputCoordinates, kernels, intercepts, kernelDimension, padding):
		self._kernelMatrix_ = DenseMatrix.OfRowArrays(kernels)
		self._interceptVector_ = DenseVector.OfArray(intercepts)
		self._kernelDimension_ = kernelDimension
		self._padding_ = padding
		inputDimension = inputCoordinates.ChannelCount * inputCoordinates.RowCount * inputCoordinates.ColumnCount
		self._kernelCoordinates_ = ImageCoordinates(kernels.Length, self._kernelDimension_, self._kernelDimension_)
		self._outputRowCount_ = Utils.UImageCoordinate.ComputeOutputCounts(kernelDimension, inputCoordinates.RowCount, 1, padding, False)
		self._outputColumnCount_ = Utils.UImageCoordinate.ComputeOutputCounts(kernelDimension, inputCoordinates.ColumnCount, 1, padding, False)
		self._outputChannelCount_ = kernels.Length
		outputCoordinates = ImageCoordinates(self._outputChannelCount_, self._outputRowCount_, self._outputColumnCount_)
		outputDimension = self._outputChannelCount_ * self._outputRowCount_ * self._outputColumnCount_
		self.InitLayer(index, LayerType.CONVOLUTION_LAYER, inputDimension, outputDimension, inputCoordinates, outputCoordinates)
		self._symbolic_output_storage = ThreadLocal[Array[LPSTerm]]()
		# Fast convolution stuff:
		jBound = Utils.UImageCoordinate.ComputeOutputCounts(KernelDimension, InputCoordinates.RowCount, 1, Padding, False)
		kBound = Utils.UImageCoordinate.ComputeOutputCounts(KernelDimension, InputCoordinates.ColumnCount, 1, Padding, False)
		kernelpositions = jBound * kBound
		self.CheckInitThreadLocalScratch(kernelpositions)
		self.__intercept_scratch = DenseMatrix.Create(self._kernelMatrix_.RowCount, kernelpositions, 0.0)
		k = 0
		while k < self._kernelMatrix_.RowCount:
			x = 0
			while x < kernelpositions:
				self.__intercept_scratch[k][x] = self._interceptVector_[k]
				x += 1
			k += 1

	def get_OutputRowCount(self):
		return self._outputRowCount_

	OutputRowCount = property(fget=get_OutputRowCount)

	def get_OutputColumnCount(self):
		return self._outputColumnCount_

	OutputColumnCount = property(fget=get_OutputColumnCount)

	def get_OutputChannelCount(self):
		return self._outputChannelCount_

	OutputChannelCount = property(fget=get_OutputChannelCount)

	def get_KernelCount(self):
		return self._kernelMatrix_.RowCount

	KernelCount = property(fget=get_KernelCount)

	def get_Kernels(self):
		return self._kernelMatrix_

	Kernels = property(fget=get_Kernels)

	def get_Intercepts(self):
		return self._interceptVector_

	Intercepts = property(fget=get_Intercepts)

	def get_Padding(self):
		return self._padding_

	Padding = property(fget=get_Padding)

	def get_KernelDimension(self):
		return self._kernelDimension_

	KernelDimension = property(fget=get_KernelDimension)

	def get_KernelCoordinates(self):
		return self._kernelCoordinates_

	KernelCoordinates = property(fget=get_KernelCoordinates)

	def Instrument(self, instr, input_, output):
		raise NotImplementedError("Instrumentation")
		instr[Index] = Instrumentation.NoInstrumentation()

	def ApplyKernel(self, output, input_, padding, kernel, row, column):
		i = 0
		while i < InputCoordinates.ChannelCount:
			j = 0
			while j < self.KernelDimension:
				k = 0
				while k < self.KernelDimension:
					x = row - padding + j
					y = column - padding + k
					if x < 0 or y < 0 or x >= InputCoordinates.RowCount or y >= InputCoordinates.ColumnCount:
						continue
					index = InputCoordinates.GetIndex(i, x, y)
					if index >= 0 and index < input_.Count:
						.AddMul(, input_[index], self.Kernels[kernel][self.KernelCoordinates.GetIndex(i, j, k)])
					k += 1
				j += 1
			i += 1
		.append(, self.Intercepts[kernel])
		return 

	def Evaluate(self, input_):
		raise NotImplementedError("Don't know how to deal with this situation. What is NumT?")
		output = .CreateVector(OutputDimension) # Has initialized all values to 0.0
		self.Evaluate(input_, output)
		return output

	def Evaluate(self, input_, output):
		raise NotImplementedError("Don't know how to deal with Parallelism.")
		jBound = Utils.UImageCoordinate.ComputeOutputCounts(self.KernelDimension, InputCoordinates.RowCount, 1, self.Padding, False)
		kBound = Utils.UImageCoordinate.ComputeOutputCounts(self.KernelDimension, InputCoordinates.ColumnCount, 1, self.Padding, False)
		Parallel.For(0, self.KernelCount, ParallelOptions(MaxDegreeOfParallelism = Environment.ProcessorCount), )

	def EvaluateConcrete(self, input_):
		x = self.DoConvolution(input_)
		return x

	def EvaluateSymbolic(self, state, input_):
		if not self._symbolic_output_storage.IsValueCreated:
			raise NotImplementedError("What is NumInstLPSTermArr?")
			self._symbolic_output_storage.Value = NumInstLPSTermArr.CreateVector(OutputDimension)
		self.Evaluate(input_, self._symbolic_output_storage.Value)
		return self._symbolic_output_storage.Value

	def IsAffine(self):
		return True