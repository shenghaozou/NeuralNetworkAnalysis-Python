from numpy import array, eye, hstack, ones, vstack, zeros
import numpy as np
import LPSTerm

class CVXOPTPara(object):
    def __init__(self, input_dimension, total_constraint_count):
        self.G = None

        varCount = LPSTerm.TotalVarCount()

        print "Number of variables: " + `varCount`

        self.h = None

    def SetBounds(self, coefficients, lb, ub):
        self.SetUpperBound(coefficients, ub)
        self.SetLowerBound(coefficients, lb)


    def SetCoefficient(self, coefficients):
        if self.G == None:
            self.G = np.arange(coefficients).reshape(self.varCount, 1)
        else:
            self.G = hstack([self.G, np.arange(coefficients).reshape(self.varCount, 1)])

    def SetUpperBound(self, coefficients, intercept):
        self.SetCoefficient(coefficients)
        if self.h == None:
            self.h = np.array(intercept)
        else:
            self.h = hstack([self.h, intercept])

    def SetLowerBound(self, coefficients, intercept):
        self.SetUpperBound(coefficients, intercept)
        self.h[-1] = -self.h[-1]
        self.G[:, -1] = -self.G[:, -1]

    def Setc(self, coefficients):
        self.c = coefficients

    def reversec(self):
        self.c = -self.c

    #def SetIntegrality()????

class LPSolver(object):
    def __init__(self,input_dimension, total_constraint_count, origin, originbound):
        self.cvxPara = CVXOPTPara(input_dimension, total_constraint_count)
        self.ct_cnt = 0
        varCount = LPSTerm.TotalVarCount()

        for i in range(varCount):
            I = np.zeros(varCount)
            I[i] = 1
            if i < len(origin):
                lb = max(Utils.RobustnessOptions.MinValue, origin[i] - originbound)
                ub = min(Utils.RobustnessOptions.MaxValue, origin[i] + originbound)

                if lb <= ub:
                    self.cvxPara.SetBounds(I, lb, ub)
                else:
                    self.cvxPara.SetBounds(I, origin[i] - originbound, origin[i] + originbound)
            else:
                self.cvxPara.SetBounds(I, Utils.RobustnessOptions.MinValue, Utils.RobustnessOptions.MaxValue)

    def AddConstraint(self, ct):

        ctid = ct
        coefficients = ct.Term.GetCoefficients()
        totalvars = LPSTerm.TotalVarCount()

        if ct.Inequality == InequalityType.LT:
            self.cvxPara.SetUpperBound(coefficients, ct.Term.Intercept)
        elif ct.Inequality == InequalityType.LE:
            self.cvxPara.SetUpperBound(coefficients, ct.Term.Intercept)
        elif ct.Inequality == InequalityType.GT:
            self.cvxPara.SetLowerBound(coefficients, ct.Term.Intercept)
        elif ct.Inequality == InequalityType.GE:
            self.cvxPara.SetLowerBound(coefficients, ct.Term.Intercept)
        elif ct.Inequality == InequalityType.EQ:
            self.cvxPara.SetBounds(coefficients, ct.Term.Intercept, ct.Term.Intercept)

        self.ct_cnt += 1

    def AddConstraints(self, constraints, objective):
        numConstraints = constraints.Count
        tmp = 0
        print "LP constraints: " + `numConstraints`
        varCount = LPSTerm.TotalVarCount()

        for ct in constraints:
            self.AddConstraint(ct)
            tmp+=1

        print ""

        if objective.HasValue:
            coefficients = zeros(varCount)
            for j in range(varCount):
                coefficients[j] = objective.Value.term.GetCoefficient(j)
            self.cvxPara.Setc(coefficients)

    def SolveLowLevelLP(self):
        print "Solving LP ... "

        solver = None
        #solver = 'glpk'
        c = cvxopt.matrix(self.cvxPara.c)
        G = cvxopt.matrix(self.cvxPara.G)
        h = cvxopt.matrix(self.cvxPara.h)
        if objective.Value.type == LPSObjectiveType.Min:
            sol = cvxopt.solvers.lp(c, G, h, solver=solver)
        elif objective.Value.type == LPSObjectiveType.Max:
            self.cvxPara.reversec()
            sol = cvxopt.solvers.lp(c, G, h, solver=solver)

        return array(sol['x']).reshape((LPSTerm.TotalVarCount(),)).tolist()

