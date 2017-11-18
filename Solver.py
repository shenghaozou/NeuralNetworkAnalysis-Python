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
from Microsoft.SolverFoundation.Common import *
from Microsoft.SolverFoundation.Services import *
from SolverFoundation.Plugin.Gurobi import *
from MathNet.Numerics.LinearAlgebra import *
from MathNet.Numerics.LinearAlgebra.Double import *
from MathNet.Numerics import *

class LPSolver(object):
	def __init__(self, input_dimension, total_constraint_count, origin, originbound):
		self._ct_cnt = 0 # Just the image, not the epsilon # Bounding rectangle
		self._solver_ = GurobiSolver()
		self._input_dimension_ = input_dimension
		varCount = LPSTerm.TotalVarCount()
		Console.WriteLine("Number of variables: " + varCount)
		self._vars_ = Array.CreateInstance(int, varCount)
		i = 0
		while i < varCount:
			self._solver_.AddVariable("x" + i, )
			self._solver_.SetIntegrality(vid, RobustnessOptions.Integrality)
			if i < origin.Length:
				lb = Math.Max(Utils.RobustnessOptions.MinValue, origin[i] - originbound)
				ub = Math.Min(Utils.RobustnessOptions.MaxValue, origin[i] + originbound)
				if lb <= ub:
					# Tighter bounds for the image variables!
					self._solver_.SetBounds(vid, lb, ub)
				else:
					# Bound validation failed, very weird. Oh well just don't use the bounds. 
					# The programmer got the Min/Max values wrong.
					self._solver_.SetBounds(vid, origin[i] - originbound, origin[i] + originbound)
			else:
				self._solver_.SetBounds(vid, Utils.RobustnessOptions.MinValue, Utils.RobustnessOptions.MaxValue)
			self._vars_[i] = vid
			i += 1

	def AddConstraint(self, ct):
		ctid = self._ct_cnt
		self._solver_.AddRow("constraint" + self._ct_cnt, )
		coefficients = ct.Term.GetCoefficients()
		totalvars = LPSTerm.TotalVarCount()
		j = 0
		while j < totalvars:
			# Due to the way MSF works, if we are adding a 0 coefficient
			# this amounts to actually removing it. However, the coefficient
			# is not there to start with, hence let's not add it, at all! 
			if coefficients[j] != 0:
				self._solver_.SetCoefficient(ctid, self._vars_[j], coefficients[j])
			j += 1
		if ct.Inequality == InequalityType.LT:
			self._solver_.SetUpperBound(ctid, -ct.Term.Intercept) # - RobustnessOptions.StrictInequalityLambda * Math.Abs(ct.Term.Intercept));
		elif ct.Inequality == InequalityType.LE:
			self._solver_.SetUpperBound(ctid, -ct.Term.Intercept)
		elif ct.Inequality == InequalityType.GT:
			self._solver_.SetLowerBound(ctid, -ct.Term.Intercept) # + RobustnessOptions.StrictInequalityLambda * Math.Abs(ct.Term.Intercept));
		elif ct.Inequality == InequalityType.GE:
			self._solver_.SetLowerBound(ctid, -ct.Term.Intercept)
		elif ct.Inequality == InequalityType.EQ:
			# solver_.SetValue(ctid, -ct.Term.Intercept); WRONG
			self._solver_.SetBounds(ctid, -ct.Term.Intercept, -ct.Term.Intercept)
		else:
			pass
		self._ct_cnt += 1

	def AddConstraints(self, constraints, objective):
		# Constraints
		numConstraints = constraints.Count
		tmp = 0
		Console.WriteLine("LP constraints: " + numConstraints)
		varCount = LPSTerm.TotalVarCount()
		enumerator = constraints.GetEnumerator()
		while enumerator.MoveNext():
			ct = enumerator.Current
			self.AddConstraint(ct)
			tmp += 1
		# Console.Write("\rAdding LP constraints: {0:0.000}%", (double)tmp * 100.0 / numConstraints);
		Console.WriteLine()
		if objective.HasValue:
			self._solver_.AddRow("Objective", )
			j = 0
			while j < varCount:
				self._solver_.SetCoefficient(objid, self._vars_[j], objective.Value.term.GetCoefficient(j))
				j += 1
			# objConstr += objective.Value.term.GetCoefficient(j) * vars[j];
			if objective.Value.type == LPSObjectiveType.Max:
				self._solver_.AddGoal(objid, 10, False)
				self._objective_id = objid
			elif objective.Value.type == LPSObjectiveType.Min:
				self._solver_.AddGoal(objid, 10, True)
				self._objective_id = objid

	def SolveLowLevelLP(self):
		# Solve the LP
		Console.Write("Solving LP ... ")
		pms = GurobiParams()
		pms.OutputFlag = False
		pms.TimeLimit = RobustnessOptions.LPTimeMilliSeconds
		# Try to prevent GC from happening here ...
		# First do a massive reclaim ... 
		GC.Collect(2)
		# Then save the old GC mode and set the one now to low latency ... 
		old_gc_mode = System.Runtime.GCSettings.LatencyMode
		System.Runtime.GCSettings.LatencyMode = System.Runtime.GCLatencyMode.LowLatency
		answer = self._solver_.Solve(pms)
		# Restore GC mode ... 
		System.Runtime.GCSettings.LatencyMode = old_gc_mode
		# DV: For now!
		#double solval = answer.GetSolutionValue(objective_id).ToDouble();
		#Console.WriteLine("Objective (row) value: {0}", solval);
		#Console.WriteLine("Objective (variable) GetValue: {0}", answer.GetValue(vars_[LPSTerm.TotalVarCount() - 1]).ToDouble());
		#var report = solver_.GetReport(LinearSolverReportType.None);
		#Console.WriteLine("Report:");
		#Console.WriteLine(report);
		result = answer.LpResult
		if result != LinearResult.Optimal:
			if result != LinearResult.Feasible:
				Console.WriteLine("LP non-feasible")
				return None
			else: # Feasible
				Console.WriteLine("LP feasible but non-optimal solution")
		Console.WriteLine("LP optimal solution found")
		vs = Array.CreateInstance(Double, self._input_dimension_)
		i = 0
		while i < self._input_dimension_:
			vs[i] = answer.GetValue(self._vars_[i]).ToDouble()
			i += 1
		return vs