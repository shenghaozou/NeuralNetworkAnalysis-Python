
class NNetReader(object):
	def ReadBytes(input, byteCount):
		bytes = input.ReadBytes(byteCount)
		Array.Reverse(bytes)
		return bytes

	ReadBytes = staticmethod(ReadBytes)

	def ReadInt32(input):
		bytes = NNetReader.ReadBytes(input, 4)
		return BitConverter.ToInt32(bytes, 0)

	ReadInt32 = staticmethod(ReadInt32)

	def ReadSingle(input):
		bytes = NNetReader.ReadBytes(input, 4)
		return BitConverter.ToSingle(bytes, 0)

	ReadSingle = staticmethod(ReadSingle)

	def ReadInt32_TextNewLine(input):
		str = input.ReadLine()
		return Int32.Parse(str)

	ReadInt32_TextNewLine = staticmethod(ReadInt32_TextNewLine)

	def ReadSingle_TextNewLine(input):
		str = input.ReadLine()
		return Double.Parse(str)

	ReadSingle_TextNewLine = staticmethod(ReadSingle_TextNewLine)

	def ReadDataLayer(index, readInt32, readSingle, inputCoordinates, inputDim):
		has_transform_param = NNetReader.readInt32()
		if has_transform_param == 0:
			layer = DataLayer(index, inputDim, inputCoordinates)
			return Tuple[CropTransform, Layer](None, layer)
		# Scale 
		scale = 1.0
		has_scale = NNetReader.readInt32()
		if has_scale != 0:
			scale = NNetReader.readSingle()
		# Mirror 
		has_mirror = NNetReader.readInt32() # ignore
		# Crop size
		cropT_ = None
		has_crop_siz = NNetReader.readInt32()
		if has_crop_siz != 0:
			crop_siz = NNetReader.readInt32()
			cropT_ = CropTransform(inputCoordinates, inputDim, crop_siz, True)
		# Mean value
		mean_val = [None] * 
		mean_val_cnt = NNetReader.readInt32()
		x = 0
		while x < mean_val_cnt:
			mean_val.append(NNetReader.readSingle())
			x += 1
		# Mean file
		has_mean_file = NNetReader.readInt32()
		mean_image = None
		if has_mean_file != 0:
			mean_image_siz = NNetReader.readInt32()
			if mean_image_siz > 0:
				mean_image = [None] * mean_image_siz
			x = 0
			while x < mean_image_siz:
				mean_image[x] = NNetReader.readSingle()
				x += 1
		dataLayerInputCoordinates = inputCoordinates
		dataLayerInputDim = inputDim
		dataLayerMeanImage = mean_image
		if cropT_ != None:
			dataLayerInputCoordinates = cropT_.TransformedCoordinates()
			dataLayerInputDim = cropT_.TransformedDimension()
			if mean_image != None:
				dataLayerMeanImage = cropT_.Transform(DenseVector.OfArray(mean_image)).ToArray()
		l = DataLayer(index, dataLayerInputDim, dataLayerInputCoordinates, scale, dataLayerMeanImage, mean_val)
		return Tuple[CropTransform, Layer](cropT_, l)

	ReadDataLayer = staticmethod(ReadDataLayer)

	def ReadInnerProductLayer(index, readInt32, readSingle, inputCoordinates, inputDim):
		# Caffe format:
		# K : input dimension
		# N : output dimension
		# A : N * K dimensional matrix (row major order)
		# B : N dimensional vector
		# Matrix formula: output = A * input + B
		# Array formula: output[i] = (\sum_j A[i][j] * x[j]) + B[i]
		inputDimension = NNetReader.readInt32()
		outputDimension = NNetReader.readInt32()
		weights = [None] * outputDimension
		i = 0
		while i < outputDimension:
			weights[i] = [None] * inputDimension
			j = 0
			while j < inputDimension:
				weights[i][j] = NNetReader.readSingle()
				j += 1
			i += 1
		intercept = [None] * outputDimension
		i = 0
		while i < outputDimension:
			intercept[i] = NNetReader.readSingle()
			i += 1
		print "Dimensions: " + inputDimension + " * " + outputDimension
		return InnerProductLayer(index, weights, intercept, inputCoordinates)

	ReadInnerProductLayer = staticmethod(ReadInnerProductLayer)

	def ReadRectifiedLinearLayer(index, readInt32, readSingle, inputCoordinates, inputDim):
		return ReLULayer(index, inputDim, inputCoordinates)

	ReadRectifiedLinearLayer = staticmethod(ReadRectifiedLinearLayer)

	def ReadSoftmaxLayer(readInt32, readSingle):
		return None

	ReadSoftmaxLayer = staticmethod(ReadSoftmaxLayer)

	def ReadConvolutional(index, readInt32, readSingle, inputCoordinates, inputDim):
		kernelCount = NNetReader.readInt32()
		kernelDimension = NNetReader.readInt32()
		padding = NNetReader.readInt32()
		# read kernels
		kernelTotalDataCount = NNetReader.readInt32()
		kernelDataCount = kernelTotalDataCount / kernelCount
		kernels = [None] * kernelCount
		i = 0
		while i < kernelCount:
			kernels[i] = [None] * kernelDataCount
			j = 0
			while j < kernelDataCount:
				kernels[i][j] = NNetReader.readSingle()
				j += 1
			i += 1
		# read intercepts
		interceptTotalDataCount = NNetReader.readInt32()
		if interceptTotalDataCount != kernelCount:
			raise Exception("Invalid parameters!")
		intercepts = [None] * kernelCount
		i = 0
		while i < kernelCount:
			intercepts[i] = NNetReader.readSingle()
			i += 1
		channelCount = (kernelDataCount / (kernelCount * kernelDimension * kernelDimension))
		kernelCoordinates = ImageCoordinates(channelCount, kernelDimension, kernelDimension)
		return ConvolutionLayer(index, inputCoordinates, kernels, intercepts, kernelDimension, padding)

	ReadConvolutional = staticmethod(ReadConvolutional)

	def ReadPooling(index, readInt32, readSingle, inputCoordinates):
		kernelDimension = NNetReader.readInt32()
		stride = NNetReader.readInt32()
		padding = NNetReader.readInt32()
		poolMeth = NNetReader.readInt32()
		if kernelDimension == 0:
			print "Kernel dimension = 0, treating this as global pooling!"
			Debug.Assert(inputCoordinates.ColumnCount == inputCoordinates.RowCount)
			Debug.Assert(padding == 0)
			kernelDimension = inputCoordinates.ColumnCount
		if poolMeth == 0: # MAX
			print "Pool method = MAX"
			return MaxPoolingLayer(index, inputCoordinates, kernelDimension, padding, stride)
		else: # AVG 
			print "Pool method = AVG"
			return AvgPoolingLayer(index, inputCoordinates, kernelDimension, padding, stride)

	ReadPooling = staticmethod(ReadPooling)

	def ReadLayer(index, readInt32, readSingle, inputCoordinates, inputDim, cropT):
		typeID = NNetReader.readInt32()
		cropT = None
		Console.Write("Reading layer with index {0,2}, of type {1}, input dimension {2}:", index, typeID, inputDim)
		if typeID == 0: # "Data"
			print "Data"
			res = NNetReader.ReadDataLayer(index, readInt32, readSingle, inputCoordinates, inputDim)
			cropT = res.Item1
			return res.Item2
		elif typeID == 1: # "InnerProduct"
			Console.Write("InnerProduct")
			return NNetReader.ReadInnerProductLayer(index, readInt32, readSingle, inputCoordinates, inputDim)
		elif typeID == 2: # "ReLU"
			print "ReLU"
			return NNetReader.ReadRectifiedLinearLayer(index, readInt32, readSingle, inputCoordinates, inputDim)
		elif typeID == 3: # "SoftmaxWithLoss"
			print "SoftMax"
			return NNetReader.ReadSoftmaxLayer(readInt32, readSingle)
		elif typeID == 4: # "Convolution"
			print "Convolution"
			return NNetReader.ReadConvolutional(index, readInt32, readSingle, inputCoordinates, inputDim)
		elif typeID == 5: # "Pooling"
			Console.Write("Pooling, ")
			return NNetReader.ReadPooling(index, readInt32, readSingle, inputCoordinates)
		elif typeID == 6: # "Dropout"
			Console.Write("Dropout, ")
			return None
		else:
			raise Exception("Layer type ID not recognized: " + typeID)

	ReadLayer = staticmethod(ReadLayer)

	def ReadNeuralNet(readInt32, readSingle, inputDimension, inputCoordinates):
		nn = NeuralNet()
		layerCount = NNetReader.readInt32()
		curDimension = inputDimension
		curCoordinates = inputCoordinates
		cropT = None
		i = 0
		while i < layerCount:
			layer = NNetReader.ReadLayer(i, readInt32, readSingle, curCoordinates, curDimension, )
			if layer != None:
				nn.AddLayer(layer)
				curDimension = layer.OutputDimension
				curCoordinates = layer.OutputCoordinates
				if layer.LayerType == LayerType.DATA_LAYER and cropT != None:
					nn.AddCropTransform(cropT)
			i += 1
		# Currently disabled because perf gains are not enough, in fact things seem somewhat slower ... 
		# Console.Write("Linearizing sequences of linear layers ...");
		# Coalesce affine layers for running the network more optimally
		# nn.CoalesceToVirtual();
		# GC.Collect(2);
		# print "Done.";
		return nn

	ReadNeuralNet = staticmethod(ReadNeuralNet)

	def ReadBinNeuralNet(file, inputDimension, inputCoordinates):
		""" <summary>
		 Reading from our own binary format. These are the networks we get as output of our protobuf utilities from Caffe.
		 </summary>
		 <param name="file"></param>
		 <param name="inputDimension"></param>
		 <param name="inputCoordinates"></param>
		 <returns></returns>
		"""
		print "Reading neural net from file: " + file

	ReadBinNeuralNet = staticmethod(ReadBinNeuralNet)

	def ReadTxtNeuralNet(file, inputDimension, inputCoordinates):
		""" <summary>
		 Reading from our own text format. These are the networks we we get as output from our Torch/LUA experiments.
		 </summary>
		 <param name="file"></param>
		 <param name="inputDimension"></param>
		 <param name="inputCoordinates"></param>
		 <returns></returns>
		"""
		print "Reading neural net from file: " + file

	ReadTxtNeuralNet = staticmethod(ReadTxtNeuralNet)