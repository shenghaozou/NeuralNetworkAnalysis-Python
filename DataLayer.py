import abc
import DenseMatrix
import DenseVector

class ITransform(object):
	def __init__(self):
		__metaclass__ = abc.ABCMeta
	@abc.abstractmethod
	def TransformedCoordinates(self):
		raise NotImplementedError("Please use a concrete ITransform object")

	@abc.abstractmethod
	def OriginalCoordinates(self):
		raise NotImplementedError("Please use a concrete ITransform object")

	@abc.abstractmethod
	def TransformedDimension(self):
		raise NotImplementedError("Please use a concrete ITransform object")

	@abc.abstractmethod
	def OriginalDimension(self):
		raise NotImplementedError("Please use a concrete ITransform object")

	@abc.abstractmethod
	def Transform(self, input):
		raise NotImplementedError("Please use a concrete ITransform object")

	@abc.abstractmethod
	def UnTransform(self, original, image):
		raise NotImplementedError("Please use a concrete ITransform object")

	@abc.abstractmethod
	def Transform(self, input):
		raise NotImplementedError("Please use a concrete ITransform object")

class CropTransform(ITransform):
	def __init__(self, inputCoordinates, inputDimension, cropSize, fromCenter):
		self._fromCenter_ = True
		self._cropSize_ = cropSize
		self._inputDimension_ = inputDimension
		self._inputCoordinates_ = inputCoordinates
		self._outputDimension_ = cropSize * cropSize * inputCoordinates.ChannelCount
		self._outputCoordinates_ = ImageCoordinates(inputCoordinates.ChannelCount, cropSize, cropSize)
		
	def OriginalCoordinates(self):
		return self._inputCoordinates_

	def OriginalDimension(self):
		return self._inputDimension_

	def TransformedCoordinates(self):
		return self._outputCoordinates_

	def TransformedDimension(self):
		return self._outputDimension_

	def UnTransform(self, orig, image):
		ret = DenseVector.Create(orig.Count(), 0.0)
		orig.CopyTo(ret)
		# Now ret is a copy of orig, so simply overwrite the relevant pixels
		center_row = self._inputCoordinates_.RowCount / 2
		center_col = self._inputCoordinates_.ColumnCount / 2
		topleft_row = center_row - self._cropSize_ / 2
		topleft_col = center_col - self._cropSize_ / 2
		channel = 0
		while channel < self._inputCoordinates_.ChannelCount:
			i = 0
			while i < self._cropSize_:
				j = 0
				while j < self._cropSize_:
					input_idx = self._inputCoordinates_.GetIndex(channel, topleft_row + i, topleft_col + j)
					output_idx = self._outputCoordinates_.GetIndex(channel, i, j)
					if input_idx >= 0 and input_idx < self._inputDimension_ and output_idx >= 0 and output_idx < self._outputDimension_:
						ret[input_idx] = image[output_idx]
					j += 1
				i += 1
			channel += 1
		return ret

	def TransformGeneric(self, input):
		if not self._fromCenter_:
			raise NotImplementedException("Non-center image cropping not supported yet!")
		center_row = self._inputCoordinates_.RowCount / 2
		center_col = self._inputCoordinates_.ColumnCount / 2
		topleft_row = center_row - self._cropSize_ / 2
		topleft_col = center_col - self._cropSize_ / 2
		output = .CreateVector(self._outputCoordinates_.ChannelCount * self._outputCoordinates_.RowCount * self._outputCoordinates_.ColumnCount)
		channel = 0
		while channel < self._inputCoordinates_.ChannelCount:
			i = 0
			while i < self._cropSize_:
				j = 0
				while j < self._cropSize_:
					input_idx = self._inputCoordinates_.GetIndex(channel, topleft_row + i, topleft_col + j)
					output_idx = self._outputCoordinates_.GetIndex(channel, i, j)
					if input_idx >= 0 and input_idx < self._inputDimension_ and output_idx >= 0 and output_idx < self._outputDimension_:
						z = .Const(0.0)
						.Add(, input[input_idx])
						output[output_idx] = z
					j += 1
				i += 1
			channel += 1
		return output

	def Transform(self, input):
		#             Utils.UDraw.DisplayImageAndPause(Utils.UArray.ToRGBArray(input.ToArray(), 128, 127), 32, 32, true);
		output = self.TransformGeneric(input)
		#            Utils.UDraw.DisplayImageAndPause(Utils.UArray.ToRGBArray(output.ToArray(), 128, 127), 30, 30, true);
		return output

	def Transform(self, input):
		return self.TransformGeneric(input)

class DataLayer(Layer):
	# Scaling
	# Mean image, NB: only one of the two can be non-null. 
	# Invariant: their coordinates must be the coordinates of this layer
	# NB: Mirror not really implemented ... 
	# Nullable<bool> mirror_ = null;
	def __init__(self, index, inputDimension, inputCoordinates, scale, meanImage, meanChannel):
		self._scale_ = 1.0
		self._meanImage_ = None
		self._meanChannel_ = None
		self._scale_ = scale
		self._meanImage_ = meanImage
		if meanChannel != None and meanChannel.Count > 0:
			channel_count = inputCoordinates.ChannelCount
			self._meanChannel_ = Array.CreateInstance(Double, channel_count)
			i = 0
			while i < channel_count:
				self._meanChannel_[i] = meanChannel[i % meanChannel.Count()]
				i += 1
		self.InitLayer(index, LayerType.DATA_LAYER, inputDimension, inputDimension, inputCoordinates, inputCoordinates)

	def __init__(self, index, inputDimension, inputCoordinates, scale, meanImage, meanChannel):
		self._scale_ = 1.0
		self._meanImage_ = None
		self._meanChannel_ = None
		self._scale_ = scale
		self._meanImage_ = meanImage
		if meanChannel != None and meanChannel.Count > 0:
			channel_count = inputCoordinates.ChannelCount
			self._meanChannel_ = Array.CreateInstance(Double, channel_count)
			i = 0
			while i < channel_count:
				self._meanChannel_[i] = meanChannel[i % meanChannel.Count()]
				i += 1
		self.InitLayer(index, LayerType.DATA_LAYER, inputDimension, inputDimension, inputCoordinates, inputCoordinates)

	def Instrument(self, instr, input, output):
		instr[Index] = Instrumentation.NoInstrumentation()

	def IsAffine(self):
		return False
 # Oh well just just don't coalesce across data layer although technically it's entirely possible
	def EvaluateConcrete(self, input):
		# If we have a meanImage ...
		if self._meanImage_ != None:
			return (input - DenseVector.OfArray(self._meanImage_)) * self._scale_
		# If we have a meanChannel ... 
		if self._meanChannel_ != None and self._meanChannel_.Count() > 0:
			cur = input
			channel = 0
			while channel < InputCoordinates.ChannelCount:
				r = 0
				while r < InputCoordinates.RowCount:
					c = 0
					while c < InputCoordinates.ColumnCount:
						index = InputCoordinates.GetIndex(channel, r, c)
						cur[index] = (input[index] - self._meanChannel_[channel]) * self._scale_
						c += 1
					r += 1
				channel += 1
			return cur
		# If we are only doing scaling ... 
		return (input * self._scale_)

	def EvaluateSymbolic(self, state, input):
		cur = .CreateVector(input.Length)
		# If we have a meanImage ...
		if self._meanImage_ != None:
			i = 0
			while i < input.Length:
				cur[i].Sub(LPSTerm.Const(self._meanImage_[i])) # - mean
				cur[i].Add(input[i]) # + input
				cur[i].Mul(self._scale_)
				i += 1
			return cur
		# If we have a meanChannel ... 
		if self._meanChannel_ != None and self._meanChannel_.Count() > 0:
			channel = 0
			while channel < InputCoordinates.ChannelCount:
				r = 0
				while r < InputCoordinates.RowCount:
					c = 0
					while c < InputCoordinates.ColumnCount:
						index = InputCoordinates.GetIndex(channel, r, c)
						cur[index].Sub(LPSTerm.Const(self._meanChannel_[channel]))
						cur[index].Add(input[index])
						cur[index].Mul(self._scale_)
						c += 1
					r += 1
				channel += 1
			return cur
		# Finally, if we are only doing scaling ...
		i = 0
		while i < input.Length:
			cur[i].Add(input[i])
			cur[i].Mul(self._scale_)
			i += 1
		return cur