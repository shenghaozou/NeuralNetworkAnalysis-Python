# --------------------------------------------------------------------------------------------------
# Neural Network Analysis Framework
#
# Copyright(c) Microsoft Corporation
# All rights reserved.
#
# MIT License
#  
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
#  associated documentation files (the "Software"), to deal in the Software without restriction,
#  including without limitation the rights to use, copy, modify, merge, publish, distribute,
#  sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#  
#  The above copyright notice and this permission notice shall be included in all copies or
#  substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
#  NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# --------------------------------------------------------------------------------------------------

from System.Collections.Generic import *
from System.Linq import *
from System.Text import *
from System.Diagnostics import *
from MathNet.Numerics.LinearAlgebra import *
from MathNet.Numerics.LinearAlgebra.Double import *
from MathNet.Numerics import *

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