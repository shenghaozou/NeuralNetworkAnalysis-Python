from __future__ import *
import InnerProductLayer
import LPSTerm

class VirtualLayer (InnerProductLayer):
    def Coalesce(self, toCoalesce):
        assert len(toCoalesce) != 0
        input_dim = toCoalesce[0].InputDimension
        output_dim = toCoalesce[-1].OutputDimension

        tmp = LPSTerm.GetVariableFactoryState()
        LPSTerm.ResetVariableFactory(input_dim)

        identity = LPSTerm.IdentityMatrix(input_dim)
        v = identity
        for i in range(0, len(toCoalesce)):
            curr = toCoalesce[i]
            w = curr.EvaluateSymbolic(None, v)
            v = w

        LPSTerm.RestoreVariableFactory(tmp)

        return (LPSTerm.UnderlyingMatrix(v), LPSTerm.UnderlyingIntercept(v))


    def __init__(self, toCoalesce):
        InnerProductLayer.__init__(self, toCoalesce[0].Index, self.Coalesce(toCoalesce), toCoalesce[0].InputCoordinates)


    def IsAffine(self):
        """Well, it is actually affine, but we don't really want to call our function again here"""
        raise Exception("IsAffine called on VirtualLayer")
