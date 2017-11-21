from __future__ import *

public abstract class PoolingLayer (Layer):
    def __init__(self, index, inputCoordinates, kernelDimension, padding, stride):
        Layer.__init__()
        self.inputCoordinates_ = inputCoordinates
        self.kernelDimension_ = kernelDimension
        self.padding_ = padding
        self.stride_ = stride

        inputDimension = self.inputCoordinates_.ChannelCount * self.inputCoordinates_.RowCount * self.inputCoordinates_.ColumnCount

        rowCount = Utils.UImageCoordinate.ComputeOutputCounts(kernelDimension, inputCoordinates.RowCount, stride, padding, True)
        columnCount = Utils.UImageCoordinate.ComputeOutputCounts(kernelDimension, inputCoordinates.ColumnCount, stride, padding, True)

        outputDimension = inputCoordinates.ChannelCount * rowCount * columnCount

        ouputCoordinates = new ImageCoordinates(inputCoordinates.ChannelCount, rowCount, columnCount)

        InitLayer(index, LayerType.POOLING_LAYER, inputDimension, outputDimension, inputCoordinates, ouputCoordinates)



    public abstract double ApplyKernelConcrete(NNInstrumentation instr, Vector<double> input, int outIndex, int channel, int row, int column)
    public abstract LPSTerm ApplyKernelSymbolic(LPSState state, LPSTerm[] input, int outIndex, int channel, int row, int column)


    protected V ApplyKernels<NumT,T,V,S>(S state, Func<S,V,int,int,int,int,T> applyKernel, V input) where NumT : struct, Num<T,V> where V : IList<T>
        output = default(NumT).CreateVector(OutputDimension)
        stride = Stride

        jbound = Utils.UImageCoordinate.ComputeOutputCounts(KernelDimension, InputCoordinates.RowCount, Stride, Padding, true)
        kbound = Utils.UImageCoordinate.ComputeOutputCounts(KernelDimension, InputCoordinates.ColumnCount, Stride, Padding, true)

        for i in range(InputCoordinates.ChannelCount):
            for j in range(rangejbound):
                for k in range(kbound):
                    index = OutputCoordinates.GetIndex(i, j, k)
                    value = applyKernel(state, input, index, i, j * stride, k * stride)
                    output[index] = value

        return output


    def EvaluateSymbolic(self, state, input):
        return ApplyKernels<NumInstLPSTermArr, LPSTerm, LPSTerm[], LPSState>(state, ApplyKernelSymbolic, input)

    def EvaluateConcrete(self, input):
        return ApplyKernels<NumInstDouble, double, Vector<double>, NNInstrumentation>(null, ApplyKernelConcrete, input)
