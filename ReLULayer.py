from __future__ import *
import numpy as np
import random
import time
import Layer
import Utils

class ReLULayer (Layer):
    def __init__(self, index, dimension, coordinates):
        self.dimension_ = dimension
        InitLayer(index, LayerType.RECTIFIED_LINEAR, dimension, dimension, coordinates, coordinates)

    def __Active(self, x):
        return x >= 0.0

    def EvaluateConcrete(self, v):
        res = v.Map(x= > __Active(x)? x: 0.0 )
        if Utils.RobustnessOptions.ReLULogFile != "":
            disjunctionChoices = CreateDisjunctionChoices(v)
            Instrumentation.LogDisjunctionChoices(Utils.RobustnessOptions.ReLULogFile, Index, disjunctionChoices)
        return res

    def CreateDisjunctionChoices(self, input):
        disjunctionChoices = [None] * len(input)
        for i in range(len(input)):
            disjunctionChoices[i] =  DisjunctionChoice.ACTIVE if self.__Active(input[i]) else DisjunctionChoice.INACTIVE
        return disjunctionChoices

    def Instrument(self, instr, input, output):
        disjunctionChoices = CreateDisjunctionChoices(input)
        instr[Index] = Instrumentation.ReLUInstrumentation(disjunctionChoices)

    def IsActivationWobbly(self, input, image):
        icpt = input.Intercept
        imagecoeffs = input.GetCoefficients().SubVector(0, len(image))
        innerprod = imagecoeffs * DenseVector.OfArray(image)
        shouldIncrease = 1.0 if innerprod + icpt < 0 else -1.0
        signVec = imagecoeffs.Map(x= > (x >= 0) ? 1.0: -1.0);

        """"// Adversarial image:"""
        adversarial_image = DenseVector.OfArray(image)

        for i in range(len(image)):
            adversarial_image[i] += shouldIncrease * signVec[i] * 0.5 * Utils.RobustnessOptions.Epsilon


        return (np.sign(innerprod + icpt) != np.sign(imagecoeffs * adversarial_image + icpt))

    def EvaluateSymbolic(self, state, input):
        disjunctionChoices = state.Instrumentation[Index].DisjunctionConstraints
        assert InputDimension == disjunctionChoices.Length
        output = [None] * OutputDimension
        r = random.seed(time.time())
        for i in range(OutputDimension):
            if disjunctionChoices[i] == DisjunctionChoice.ACTIVE:
                output[i] = input[i]
                """// If we are supposed to do sampling"""
                if Utils.RobustnessOptions.LiveConstraintSamplingRatio != 1.0:
                    """// if we are above threshold defer"""
                    if random.randrange(0, 100) > int(Utils.RobustnessOptions.LiveConstraintSamplingRatio * 100):
                        state.DeferredCts.And(input[i], InequalityType.GE)
                    else:
                        state.CurrentCts.And(input[i], InequalityType.GE)

                else:
                    state.CurrentCts.And(input[i], InequalityType.GE)
            elif disjunctionChoices[i] == DisjunctionChoice.INACTIVE:
                output[i] = LPSTerm.Const(0.0)
                """// CEGAR version: defer 'dead' constraint """
                state.DeferredCts.And(input[i], InequalityType.LT)
            else:
                raise Exception("Invalid disjunction choice type!")
        return output

def IsAffine(self):
    return False