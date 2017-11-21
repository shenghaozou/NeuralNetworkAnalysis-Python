from enum import Enum
import Utils
import random
class LPSObjectiveType(Enum):
    Min = 0
    Max = 1

class LPSObjectiveKind(Enum):
    MinLinf = 0
    MaxConf = 1

class LPSObjective(object):
    def __init__(self):
        self.term = None
        self.type = None

class NNETObjectives(object):
    """
    // / < summary >
    /// Create formulae of the form:  <code> -epsilon &lt input[i] - origin[i] &lt epsilon </code>
    // / < / summary >
    """
    @staticmethod
    def AddEpsilonBounds(self, cts, input, epsilon, origin):
        for i in range(len(origin)):
            curr = input[i]
            tmp = LPSTerm.Const(origin[i])
            tmp.Sub(epsilon)
            cts.And(tmp, InequalityType.LE, curr)

            tmp = LPSTerm.Const(origin[i])
            tmp.Add(epsilon)
            cts.And(curr, InequalityType.LE, tmp)



            cts.And(epsilon, InequalityType.GT, LPSTerm.Const(0.0))
            cts.And(epsilon, InequalityType.LE, LPSTerm.Const(Utils.RobustnessOptions.Epsilon))

    @staticmethod
    def AddQuantizationSafety(self, cts, input, origin):
        r = random.Random()
        i = r.randrange(0, len(origin) - 1)
        curr = input[i]
        tmp = LPSTerm.Const(origin[i] + 1.0)
        cts.And(tmp, InequalityType.LE, curr)

    @staticmethod
    def MinLInf(self, cts, input, epsilon, origin):
        return LPSObjective(epsilon, LPSObjectiveType.Min)

    @staticmethod
    def MaxConf(self, output, origLabel, newLabel):
        tmp = LPSTerm.Const(0.0)
        tmp.Add(output[newLabel])
        tmp.Sub(output[origLabel])
        return LPSObjective(tmp, LPSObjectiveType.Max)

class NNetFormulas(object):
    """
    // / < summary >
    // LabelFormula(output, label, confidence) gives back a formula expressing
    // that: for all i s.t.i != label, output[label] - output[i] >= confidence
    // / < / summary >
    // / < param name="output" > Output of neural network (before softmax, as given by our evaluator).< / param >
    // / < param name="label" > The label we wish to win.< / param >
    // / < param name="confidence" > A confidence interval for all comparisons (e.g.for quantization etc).< / param >
    // / < returns > The constraint expressing that our label is indeed the winning one.< / returns >
    """
    @staticmethod
    def LabelFormula(self, output, label, confidence = 0):
        ct = new LPSConstraints()
        for i in range(len(output)):
            if i != label:
                """
                Need: output[label] - output[i] >= confidence
                i.e.: output[label] - output[i] - confidence >= 0
                """
                tmp = LPSTerm.Const(0.0)
                tmp.Add(output[label])
                tmp.AddMul(output[i], -1.0)
                tmp.Add(-1.0 * confidence)
                ct.And(tmp, InequalityType.GE)
        return ct


    """
    Ensures that the input is within an originBound ball of origin, or within 0.0f - 255f,
    whichever is tightest.
    """
    @staticmethod
    def OriginBoundFormula(self, input, origin, originBound):
        assert len(input) == len(origin)
        ct = LPSConstraints()
        for i in range(len(input)):
            ub = min(Utils.RobustnessOptions.MaxValue, origin[i] + originBound)
            lb = max(Utils.RobustnessOptions.MinValue, origin[i] - originBound)

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

        return ct