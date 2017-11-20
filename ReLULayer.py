
class ReLULayer(Layer):
	def __init__(self, index, dimension, coordinates):
		self._dimension_ = dimension
		self.InitLayer(index, LayerType.RECTIFIED_LINEAR, dimension, dimension, coordinates, coordinates)

	def get_Dimension(self):
		return self._dimension_

	Dimension = property(fget=get_Dimension)

	def Active(self, x):
		return (x >= 0.0)

	def EvaluateConcrete(self, v):
		res = v.Map()
		if Utils.RobustnessOptions.ReLULogFile != "":
			disjunctionChoices = self.CreateDisjunctionChoices(v)
			Instrumentation.LogDisjunctionChoices(Utils.RobustnessOptions.ReLULogFile, Index, disjunctionChoices)
		return res

	def CreateDisjunctionChoices(self, input):
		disjunctionChoices = Array.CreateInstance(DisjunctionChoice, input.Count)
		i = 0
		while i < input.Count:
			disjunctionChoices[i] = DisjunctionChoice.ACTIVE if self.Active(input[i]) else DisjunctionChoice.INACTIVE
			i += 1
		return disjunctionChoices

	def Instrument(self, instr, input, output):
		disjunctionChoices = self.CreateDisjunctionChoices(input)
		instr[Index] = Instrumentation.ReLUInstrumentation(disjunctionChoices)

	def IsActivationWobbly(self, input, image):
		icpt = input.Intercept
		imagecoeffs = input.GetCoefficients().SubVector(0, image.Length)
		innerprod = imagecoeffs * DenseVector.OfArray(image)
		shouldIncrease = 1.0 if (innerprod + icpt < 0) else -1.0
		signVec = imagecoeffs.Map()
		# Adversarial image:
		adversarial_image = DenseVector.OfArray(image)
		i = 0
		while i < image.Length:
			adversarial_image[i] += shouldIncrease * signVec[i] * 0.5 * Utils.RobustnessOptions.Epsilon
			i += 1
		#print "Original activation:    {0}", innerprod + icpt;
		#print "Adversarial activation: {0}", imagecoeffs * adversarial_image + icpt;
		#Console.Read();
		return (Math.Sign(innerprod + icpt) != Math.Sign(imagecoeffs * adversarial_image + icpt))

	def EvaluateSymbolic(self, state, input):
		disjunctionChoices = state.Instrumentation[Index].DisjunctionConstraints
		Debug.Assert(InputDimension == disjunctionChoices.Length)
		output = [None] * OutputDimension
		r = Random(System.DateTime.Now.Millisecond)
		# int uncertain = 0;
		i = 0
		while i < OutputDimension:
			if disjunctionChoices[i] == DisjunctionChoice.ACTIVE:
				output[i] = input[i]
				# If we are supposed to do sampling
				if Utils.RobustnessOptions.LiveConstraintSamplingRatio != 1.0:
					# print "Sampling!";
					# if we are above threshold defer
					if r.Next(0, 100) > Utils.RobustnessOptions.LiveConstraintSamplingRatio * 100:
						state.DeferredCts.And(input[i], InequalityType.GE)
					else:
						state.CurrentCts.And(input[i], InequalityType.GE)
				else:
					state.CurrentCts.And(input[i], InequalityType.GE)
			elif disjunctionChoices[i] == DisjunctionChoice.INACTIVE:
				output[i] = LPSTerm.Const(0.0)
				# CEGAR version: defer 'dead' constraint
				state.DeferredCts.And(input[i], InequalityType.LT)
			else:
				# Original version
				# state.CurrentCts.And(input[i],InequalityType.LT);
				raise Exception("Invalid disjunction choice type!")
			i += 1
		# This is more of an experiment really ...
		# if (IsActivationWobbly(input[i], state.Origin))
		# {
		# uncertain++;
		# // Mutate state to have new disjunction choices to explore in the future
		# disjunctionChoices[i] = Instrumentation.FlipDisjunctionChoice(disjunctionChoices[i]);
		# }
		# 
		# print "** Ultra-sensitive ReLU activations {0}/{1}", uncertain, OutputDimension;
		return output

	def IsAffine(self):
		return False