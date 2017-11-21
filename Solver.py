import LPSTerm
import math
import Utils

class LPSolver:
    def __init__(self, input_dimension, total_constraint_count, origin, originbound):
        self.solver_ = GurobiSolver()
        self.input_dimension_ = input_dimension
        varCount = LPSTerm.TotalVarCount()
        print "Number of variables: " + `varCount`
        self.vars_ = [None] * len(varCount)
        self.ct_cnt = 0
        for i in range(varCount):
            vid = 0
            self.solver_.AddVariable("x" + i, out vid)
            self.solver_.SetIntegrality(vid, RobustnessOptions.Integrality)
            if i < len(origin):
                lb = max(Utils.RobustnessOptions.MinValue, origin[i] - originbound)
                ub = min(Utils.RobustnessOptions.MaxValue, origin[i] + originbound)

                if lb <= ub:
                    """// Tighter bounds for the image variables!"""
                    self.solver_.SetBounds(vid, lb, ub)
                else:
                    """// Bound validation failed, very weird.Oh well just don't use the bounds.
                    // The programmer got the Min / Max values wrong."""
                    self.solver_.SetBounds(vid, origin[i] - originbound, origin[i] + originbound)
            else:
                self.solver_.SetBounds(vid, Utils.RobustnessOptions.MinValue, Utils.RobustnessOptions.MaxValue)
            vars_[i] = vid


    def AddConstraint(self, ct):
        ctid = self.ct_cnt
        self.solver_.AddRow("constraint" + self.ct_cnt, out ctid)
        coefficients = ct.Term.GetCoefficients()
        totalvars = LPSTerm.TotalVarCount()

        for j in range(totalvars):
            """
            // Due to the way MSF works, if we are adding a 0 coefficient
            // this amounts to actually removing it.However, the coefficient
            // is not there to start with, hence let's not add it, at all!
            """
            if coefficients[j] != 0
                self.solver_.SetCoefficient(ctid, self.vars_[j], coefficients[j])

        if ct.Inequality == InequalityType.LT:
            self.solver_.SetUpperBound(ctid, -ct.Term.Intercept)
        elif ct.Inequality == InequalityType.LE:
            self.solver_.SetUpperBound(ctid, -ct.Term.Intercept)
        elif ct.Inequality == InequalityType.GT:
            self.solver_.SetLowerBound(ctid, -ct.Term.Intercept)
        elif ct.Inequality == InequalityType.GE:
            self.solver_.SetLowerBound(ctid, -ct.Term.Intercept)
        elif ct.Inequality == InequalityType.EQ:
            self.solver_.SetBounds(ctid, -ct.Term.Intercept, -ct.Term.Intercept)

        self.ct_cnt += 1


    def AddConstraints(self, constraints, objective):
        numConstraints = constraints.Count
        tmp = 0
        print "LP constraints: " + 'numConstraints'
        varCount = LPSTerm.TotalVarCount()
        for ct in constraints:
            self.AddConstraint(ct)
            tmp += 1

        print ""

        if objective.HasValue:
            objid = 0
            self.solver_.AddRow("Objective", out objid)

            for j in range(varCount):
                self.solver_.SetCoefficient(objid, vars_[j], objective.Value.term.GetCoefficient(j))
            if objective.Value.type == LPSObjectiveType.Max:"""Wrong!!!!!!!!!!!!"""
                self.solver_.AddGoal(objid, 10, False)
                self.objective_id = objid
            elif objective.Value.type == LPSObjectiveType.Min:"""Wrong!!!!!!!!!!!!"""
                self.solver_.AddGoal(objid, 10, True)
                self.objective_id = objid


    def SolveLowLevelLP(self):
        """// Solve the LP"""
        print "Solving LP ... "
        pms = GurobiParams()
        pms.OutputFlag = False
        pms.TimeLimit = int(RobustnessOptions.LPTimeMilliSeconds)

        """// Try to prevent GC from happening here ...
        // First do a massive reclaim..."""
        GC.Collect(2)
        """// Then save the old GC mode and set the one now to low latency..."""
        old_gc_mode = System.Runtime.GCSettings.LatencyMode
        System.Runtime.GCSettings.LatencyMode = System.Runtime.GCLatencyMode.LowLatency
        answer = self.solver_.Solve(pms)

        """// Restore GC mode..."""
        System.Runtime.GCSettings.LatencyMode = old_gc_mode
        result = answer.LpResult

        if result != LinearResult.Optimal:
            if result != LinearResult.Feasible:
                print "LP non-feasible"
                return None
            else:
                """// Feasible"""
                print "LP feasible but non-optimal solution"
            print "LP optimal solution found"
        vs = [None] * self.input_dimension_
        for i in range(self.input_dimension_):
            vs[i] = float(answer.GetValue(self.vars_[i]))
        return vs
