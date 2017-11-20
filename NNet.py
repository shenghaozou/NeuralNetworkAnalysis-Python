
class LayerType(object):
	def __init__(self):
		pass

class Layer(object):
	""" <summary>
	  A layer of the neural network and the operations it supports
	 </summary>
	"""
	def __init__(self):
		pass
		""" <summary>
		  A layer of the neural network and the operations it supports
		 </summary>
		"""
 # Which layer are we? # NB: null means there is no particular structure in the input # NB: null means there is no particular structure in the output
	def InitLayer(self, index, layerType, inputDimension, outputDimension, inputCoordinates, outputCoordinates):
		self._index_ = index
		self._layerType_ = layerType
		self._inputDimension_ = inputDimension
		self._outputDimension_ = outputDimension
		self._inputCoordinates_ = inputCoordinates
		self._outputCoordinates_ = outputCoordinates

	def get_Index(self):
		return self._index_

	Index = property(fget=get_Index)

	def get_LayerType(self):
		return self._layerType_

	LayerType = property(fget=get_LayerType)

	def get_InputDimension(self):
		return self._inputDimension_

	InputDimension = property(fget=get_InputDimension)

	def get_OutputDimension(self):
		return self._outputDimension_

	OutputDimension = property(fget=get_OutputDimension)

	def get_InputCoordinates(self):
		return self._inputCoordinates_

	InputCoordinates = property(fget=get_InputCoordinates)

	def get_OutputCoordinates(self):
		return self._outputCoordinates_

	OutputCoordinates = property(fget=get_OutputCoordinates)

	def EvaluateSymbolic(self, state, input):
		pass

	def EvaluateConcrete(self, input):
		pass

	def Instrument(self, instrumentation, input, output):
		pass

	def IsAffine(self):
		pass

class NeuralNet(object):
	""" <summary>
	 A neural network: just a collection of layers
	 </summary>
	"""
	def __init__(self):
		""" <summary>
		 A neural network: just a collection of layers
		 </summary>
		"""
		# We elevate cropping to a first-class citizen of a neural network
		# to expose it to the symbolic evaluator. If cropT == null, then no 
		# cropping happens.
		self._cropT = None
		self._layers_ = [None] * 

	def AddCropTransform(self, crop):
		self._cropT = crop

	def AddLayer(self, layer):
		self._layers_.append(layer)

	def get_Layers(self):
		return self._layers_

	Layers = property(fget=get_Layers)

	def get_LayerCount(self):
		return self._layers_.Count

	LayerCount = property(fget=get_LayerCount)

	def get_InputDimensionPostCrop(self):
		return self._layers_[0].InputDimension

	InputDimensionPostCrop = property(fget=get_InputDimensionPostCrop)

	def get_InputDimensionPreCrop(self):
		if self._cropT != None:
			return self._cropT.OriginalDimension()
		return self._layers_[0].InputDimension

	InputDimensionPreCrop = property(fget=get_InputDimensionPreCrop)

	def CropMaybe(self, image):
		if self._cropT != None:
			return self._cropT.Transform(image)
		return image

	def UnCropMaybe(self, orig, image):
		if self._cropT != None:
			return self._cropT.UnTransform(orig, image)
		return image

	def LayerTypes(self):
		layerTypes = [None] * 
		i = 0
		while i < self.LayerCount:
			layerTypes.append(self.Layers[i].LayerType)
			i += 1
		return layerTypes

	def EvaluateNNConcretePostCrop(self, input, instr):
		return self.EvaluateNNConcretePostCrop(DenseVector.OfArray(input), instr)

	def EvaluateNNConcretePostCrop(self, input, instr):
		v = input
		i = 0
		while i < self.LayerCount:
			curr = self.Layers[i]
			w = curr.EvaluateConcrete(v)
			if instr != None:
				curr.Instrument(instr, v, w)
			v = w
			i += 1
		return v.ToArray()

	def EvaluateNNSymbolicPostCrop(self, state, input):
		v = input
		i = 0
		while i < self.LayerCount:
			curr = self.Layers[i]
			stopwatch = Stopwatch()
			stopwatch.Start()
			w = curr.EvaluateSymbolic(state, v)
			stopwatch.Stop()
			v = w
			print "Symbolic interpreter: layer index: {0,2}, elapsed milliseconds = {1}", curr.Index, stopwatch.ElapsedMilliseconds
			i += 1
		return v

	def CoalesceToVirtual(self):
		newLayers = [None] * 
		currAffList = [None] * 
		i = 0
		while i < self.LayerCount:
			curr = self.Layers[i]
			if curr.IsAffine():
				currAffList.append(curr)
				continue
			# Current layer is not affine
			# If we have anything in the affine list, we should coalesce and insert before current.
			if currAffList.Count > 0:
				virt = VirtualLayer(currAffList)
				currAffList.Clear()
				newLayers.append(virt)
			newLayers.append(curr)
			i += 1
		if currAffList.Count > 0:
			virt = VirtualLayer(currAffList)
			currAffList.Clear()
			newLayers.append(virt)
		self._layers_ = newLayers