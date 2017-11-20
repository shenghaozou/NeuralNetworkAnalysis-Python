
class VirtualLayer(InnerProductLayer):
	def Coalesce(toCoalesce):
		Debug.Assert(toCoalesce.Count != 0)
		input_dim = toCoalesce.First().InputDimension
		output_dim = toCoalesce.Last().OutputDimension
		tmp = LPSTerm.GetVariableFactoryState()
		LPSTerm.ResetVariableFactory(input_dim)
		identity = LPSTerm.IdentityMatrix(input_dim)
		v = identity
		i = 0
		while i < toCoalesce.Count:
			curr = toCoalesce[i]
			w = curr.EvaluateSymbolic(None, v)
			v = w
			i += 1
		LPSTerm.RestoreVariableFactory(tmp)
		return Tuple[Matrix, Vector](LPSTerm.UnderlyingMatrix(v), LPSTerm.UnderlyingIntercept(v))

	Coalesce = staticmethod(Coalesce)

	def __init__(self, toCoalesce):
		pass
	def IsAffine(self):
		# Well, it is actually affine, but we don't really want to call our function again here
		raise Exception("IsAffine called on VirtualLayer")