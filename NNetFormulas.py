
class LPSObjectiveType(object):
	def __init__(self):

class LPSObjectiveKind(object):
	def __init__(self):

class LPSObjective(object):
	def __init__(self):

class NNETObjectives(object):
	def AddEpsilonBounds(cts, input, epsilon, origin):
		""" <summary>
		 Create formulae of the form:  <code> -epsilon &lt input[i] - origin[i] &lt epsilon </code>
		 </summary>
		 
		"""
		i = 0
		while i < origin.Length:
			curr = input[i]
			# i.e: origin[i] - epsilon < input[i]
			tmp = LPSTerm.Const(origin[i])
			tmp.Sub(epsilon)
			cts.And(tmp, InequalityType.LE, curr)
			# and: input[i] < epsilon + origin[i]
			tmp = LPSTerm.Const(origin[i])
			tmp.append(epsilon)
			cts.And(curr, InequalityType.LE, tmp)
			i += 1
		cts.And(epsilon, InequalityType.GT, LPSTerm.Const(0.0)) # Quantization error!
		cts.And(epsilon, InequalityType.LE, LPSTerm.Const(Utils.RobustnessOptions.Epsilon))

	AddEpsilonBounds = staticmethod(AddEpsilonBounds)

	def AddQuantizationSafety(cts, input, origin):
		r = Random()
		i = r.Next(0, origin.Length - 1)
		curr = input[i]
		# i.e: origin[i] - epsilon < input[i]
		tmp = LPSTerm.Const(origin[i] + 1.0)
		cts.And(tmp, InequalityType.LE, curr)

	AddQuantizationSafety = staticmethod(AddQuantizationSafety)

	def MinLInf(cts, input, epsilon, origin):
		return (LPSObjective(term = epsilon, type = LPSObjectiveType.Min))

	MinLInf = staticmethod(MinLInf)

	def MaxConf(output, origLabel, newLabel):
		tmp = LPSTerm.Const(0.0)
		tmp.append(output[newLabel])
		tmp.Sub(output[origLabel])
		return (LPSObjective(term = tmp, type = LPSObjectiveType.Max))

	MaxConf = staticmethod(MaxConf)

class NNetFormulas(object):
	def LabelFormula(output, label, confidence):
		""" <summary>
		 LabelFormula(output,label,confidence) gives back a formula expressing
		 that: for all i s.t. i != label, output[label] - output[i] >= confidence
		 </summary>
		 <param name="output">Output of neural network (before softmax, as given by our evaluator).</param>
		 <param name="label">The label we wish to win.</param>
		 <param name="confidence">A confidence interval for all comparisons (e.g. for quantization etc).</param>
		 <returns>The constraint expressing that our label is indeed the winning one. </returns>
		"""
		ct = LPSConstraints()
		i = 0
		while i < output.Length:
			if i != label:
				# Need: output[label] - output[i] >= confidence 
				# i.e.: output[label] - output[i] - confidence >= 0
				tmp = LPSTerm.Const(0.0) # tmp := 0
				tmp.append(output[label]) # tmp := output[label]
				tmp.AddMul(output[i], -1.0) # tmp := output[label] - output[i]
				tmp.append(-1.0 * confidence) # tmp := output[label] - output[i] - confidence
				ct.And(tmp, InequalityType.GE)
			i += 1
		return ct

	LabelFormula = staticmethod(LabelFormula)

	def OriginBoundFormula(input, origin, originBound):
		""" <summary>
		 Ensures that the input is within an originBound ball of origin, or within 0.0f - 255f, 
		 whichever is tightest.
		 </summary>
		 <returns></returns>
		"""
		Debug.Assert(input.Length == origin.Length)
		ct = LPSConstraints()
		i = 0
		while i < input.Length:
			ub = Math.Min(Utils.RobustnessOptions.MaxValue, origin[i] + originBound)
			lb = Math.Max(Utils.RobustnessOptions.MinValue, origin[i] - originBound)
			if lb <= ub:
				tmp = LPSTerm.Const(ub)
				ct.And(input[i], InequalityType.LE, tmp)
				tmp = LPSTerm.Const(lb)
				ct.And(input[i], InequalityType.GE, tmp)
			else:
				tmp = LPSTerm.Const(origin[i] + originBound)
				ct.And(input[i], InequalityType.LE, tmp)
				tmp = LPSTerm.Const(origin[i] - originBound)
				ct.And(input[i], InequalityType.GE, tmp)
			i += 1
		return ct

	OriginBoundFormula = staticmethod(OriginBoundFormula)