class InnerProductLayer(Layer):
	def get_WeightMatrix(self):
		return self._weightMatrix_

	WeightMatrix = property(fget=get_WeightMatrix)

	def get_InterceptVector(self):
		return self._interceptVector_

	InterceptVector = property(fget=get_InterceptVector)

	def __init__(self, index, weights, intercepts, inputCoordinates):
		pass

	def EvaluateConcrete(self, v):
		return (self._weightMatrix_ * v + self._interceptVector_)

	def Instrument(self, instr, input_, output):
		instr[Index] = Instrumentation.NoInstrumentation()

	def EvaluateSymbolic(self, state, input_):
		output = [None] * OutputDimension
		i = 0
		while i < OutputDimension:
			output[i] = self.doInnerProduct(state, input_, self._weightMatrixRows_[i])
			output[i].append(self._interceptVector_[i])
			i += 1
		return output

	def doInnerProduct(self, state, vs, ds):
		result = LPSTerm.Const(0.0)
		i = 0
		while i < vs.Length:
			result.AddMul(vs[i], ds[i])
			i += 1
		return result

	def IsAffine(self):
		return True