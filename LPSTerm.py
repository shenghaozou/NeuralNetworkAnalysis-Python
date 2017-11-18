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
from System.Threading.Tasks import *
from System.Threading import *
from System.Diagnostics import *
from MathNet.Numerics import *
from MathNet.Numerics.LinearAlgebra import *
from MathNet.Numerics.LinearAlgebra.Double import *
# Type-class trick, thanks to Claudio Russo (crusso@microsoft.com)
class Num(object):
	def AddMul(self, tgt, src, d):
		pass
 # tgt += src*d;
	def Add(self, tgt, src):
		pass
 # tgt += src;
	def Add(self, tgt, d):
		pass
 # tgt += d;
	def Mul(self, tgt, d):
		pass
 #  tgt *= d;
	def Const(self, d):
		pass

	def CreateVector(self, capacity):
		pass

class NumInstDouble(Num):
	def AddMul(self, tgt, src, d):
		tgt += src * d

	def Add(self, tgt, src):
		tgt += src

	def Mul(self, tgt, d):
		tgt *= d

	def Const(self, d):
		return d

	def CreateVector(self, capacity):
		return SparseVector.Create(capacity, 0.0)

#public struct NumInstLPSTermVec : Num<LPSTerm,LPSTerm[]>
#{
#    public void AddMul(ref LPSTerm tgt, LPSTerm src, double d) { tgt.AddMul(src, d); }
#    public void Add(ref LPSTerm tgt, LPSTerm src) { tgt.Add(src); }
#    public void Add(ref LPSTerm tgt, double d) { tgt.Add(d);} 
#    public void Mul(ref LPSTerm tgt, double d) { tgt.Mul(d); }
#    public LPSTerm Const(double d) { return LPSTerm.Const(d);  }
#    public LPSTerm[] CreateVector(int capacity)
#    {
#        var coeffs = DenseMatrix.Create(capacity, LPSTerm.TotalVarCount(), 0.0);
#        var interc = DenseVector.Create(capacity, 0.0);
#        return new LPSTerm[](coeffs, interc);
#    }
#}
class NumInstLPSTermArr(Num):
	def AddMul(self, tgt, src, d):
		tgt.AddMul(src, d)

	def Add(self, tgt, src):
		tgt.Add(src)

	def Add(self, tgt, d):
		tgt.Add(d)

	def Mul(self, tgt, d):
		tgt.Mul(d)

	def Const(self, d):
		return LPSTerm.Const(d)

	def CreateVector(self, capacity):
		vec = Array.CreateInstance(LPSTerm, capacity)
		i = 0
		while i < capacity:
			vec[i] = LPSTerm.Const(0.0)
			i += 1
		return vec

class VCInfo(object): # = new ThreadLocal<Vector<double>>();
	def __init__(self, total_varcount):
		self._varcount_ = 0
		self._total_varcount_ = 0
		self._total_varcount_ = total_varcount
		self._tempmultstorage = ThreadLocal[Vector]()

class LPSTerm(object):
	""" <summary>
	 Representation of a linear term, like 0.3 x0 + 0.0 x1 + .... 4.3 xn + interecept_
	 We use a Dictionary of coefficients from variable positions (0 for x0, etc).
	 Keys without a corresponding entry are meant to have coefficient 0.0.
	 </summary>
	"""
	# Set to null to ensure someone does call InitVariableFactory() below first!
	def IdentityMatrix(howmany):
		#Matrix<double> coeffs = DenseMatrix.CreateIdentity(howmany);
		#Vector<double> interc = DenseVector.Create(howmany, 0.0);
		# return new LPSTerm[](coeffs, interc);
		terms = Array.CreateInstance(LPSTerm, howmany)
		pos = 0
		i = 0
		while i < howmany:
			coeffs = SparseVector.Create(howmany, 0.0)
			coeffs[pos += 1] = 1.0
			terms[i] = LPSTerm(coeffs, 0.0)
			i += 1
		return terms

	IdentityMatrix = staticmethod(IdentityMatrix)

	def UnderlyingMatrix(terms):
		# Stopwatch s = new Stopwatch();
		# s.Start();
		res = SparseMatrix.Create(terms.Length, LPSTerm.TotalVarCount(), 0.0)
		i = 0
		while i < terms.Length:
			res.SetRow(i, terms[i].GetCoefficients())
			i += 1
		# s.Stop();
		# Console.WriteLine("To underlying matrix: {0} milliseconds",s.ElapsedMilliseconds);
		return res

	UnderlyingMatrix = staticmethod(UnderlyingMatrix)

	def UnderlyingTransposeMatrix(terms):
		res = DenseMatrix.Create(LPSTerm.TotalVarCount(), terms.Length, 0.0)
		i = 0
		while i < terms.Length:
			res.SetColumn(i, terms[i].GetCoefficients())
			i += 1
		return res

	UnderlyingTransposeMatrix = staticmethod(UnderlyingTransposeMatrix)

	def UnderlyingIntercept(terms):
		intercept = DenseVector.Create(terms.Length, 0.0)
		i = 0
		while i < terms.Length:
			intercept[i] = terms[i].Intercept
			i += 1
		return intercept

	UnderlyingIntercept = staticmethod(UnderlyingIntercept)

	def FromUnderlyingAlgebra(outm, outv):
		ret = Array.CreateInstance(LPSTerm, outm.RowCount)
		i = 0
		while i < outm.RowCount:
			ret[i] = LPSTerm(outm.Row(i), outv[i])
			i += 1
		return ret

	FromUnderlyingAlgebra = staticmethod(FromUnderlyingAlgebra)

	def FromUnderlyingTransposeAlgebra(outm, outv):
		ret = Array.CreateInstance(LPSTerm, outm.ColumnCount)
		i = 0
		while i < outm.ColumnCount:
			ret[i] = LPSTerm(outm.Column(i), outv[i])
			i += 1
		return ret

	FromUnderlyingTransposeAlgebra = staticmethod(FromUnderlyingTransposeAlgebra)

	def FreshVariables(howmany):
		tmp = Array.CreateInstance(LPSTerm, howmany)
		i = 0
		while i < howmany:
			tmp[i] = LPSTerm.FreshVariable()
			i += 1
		return tmp

	FreshVariables = staticmethod(FreshVariables)

	def FreshVariable():
		tmp = LPSTerm()
		tmp.coefficients_[self._vcinfo_.varcount_] = 1.0
		tmp.intercept_ = 0.0
		self._vcinfo_.varcount_ += 1
		return tmp

	FreshVariable = staticmethod(FreshVariable)

	def GetVariableFactoryState():
		return self._vcinfo_

	GetVariableFactoryState = staticmethod(GetVariableFactoryState)

	def ResetVariableFactory(total_variables):
		self._vcinfo_ = VCInfo(total_variables)
		self._vcinfo_.varcount_ = 0
		self._vcinfo_.total_varcount_ = total_variables

	ResetVariableFactory = staticmethod(ResetVariableFactory)

	def RestoreVariableFactory(info):
		self._vcinfo_ = info

	RestoreVariableFactory = staticmethod(RestoreVariableFactory)

	def TotalVarCount():
		return self._vcinfo_.total_varcount_

	TotalVarCount = staticmethod(TotalVarCount)

	def __init__(self):
		self._addmulcounter = 0
		self._vcinfo_ = None
		self._coefficients_ = SparseVector.Create(self._vcinfo_.total_varcount_, 0.0)
		self._intercept_ = 0.0

	def __init__(self):
		self._addmulcounter = 0
		self._vcinfo_ = None
		self._coefficients_ = SparseVector.Create(self._vcinfo_.total_varcount_, 0.0)
		self._intercept_ = 0.0

	def get_VarCount(self):
		return self._vcinfo_.varcount_

	VarCount = property(fget=get_VarCount)

	def Clear(self):
		self._coefficients_.Clear()

	def Densify(self):
		self._coefficients_ = DenseVector.OfVector(self._coefficients_)

	def Sparsify(self):
		self._coefficients_ = SparseVector.OfVector(self._coefficients_)

	def GetCoefficients(self):
		return self._coefficients_

	def GetCoefficient(self, i):
		return self._coefficients_[i]

	def SetCoefficient(self, i, d):
		self._coefficients_[i] = d

	def get_Intercept(self):
		return self._intercept_

	def set_Intercept(self, value):
		self._intercept_ = value

	Intercept = property(fget=get_Intercept, fset=set_Intercept)

	def ToString(self):
		ret = ""
		i = 0
		while i < self._vcinfo_.total_varcount_:
			ret += self.GetCoefficient(i) + "*X" + i + " + "
			i += 1
		ret += self.Intercept
		return ret

	# this += v
	def Add(self, v):
		self._coefficients_.Add(v.coefficients_, self._coefficients_)
		self._intercept_ += v.intercept_

	def Sub(self, v):
		self._coefficients_ -= v.coefficients_
		self._intercept_ -= v.intercept_

	def Add(self, d):
		self._intercept_ += d

	# this += d*v
	def AddMul(self, v, d):
		v.coefficients_.Multiply(d, self._vcinfo_.tempmultstorage.Value)
		self._coefficients_.Add(self._vcinfo_.tempmultstorage.Value, self._coefficients_)
		self._intercept_ += d * v.intercept_
		self._addmulcounter += 1

	def AddMulVec(self, v_coeffm, v_intcps, d_vec): # this += v1*d1 + .... vn*dn
		#Matrix<double> v_coeffm = LPSTerm.UnderlyingMatrix(v);
		#Vector<double> v_intcps = LPSTerm.UnderlyingIntercept(v);
		mul = d_vec * v_coeffm
		self._coefficients_.Add(mul, self._coefficients_)
		self._intercept_ += v_intcps * d_vec

	def Const(d):
		v = LPSTerm()
		v.intercept_ = d
		return v

	Const = staticmethod(Const)

	def Mul(self, d):
		self._coefficients_ *= d
		self._intercept_ *= d