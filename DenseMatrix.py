import numpy as np
class DenseMatrix(object):
    def __init__():
        pass
    
    def Create(row, column, initValue):
        self.matrix = np.full((row, column), initValue)
        self.RowCount = row
        self.columnCount = column

    
    def OfRowArrays(kernels):
        raise SyntaxError

    def Multiply(other, result):
        np.matmul(self.matrix, other.matrix, result.matrix)
    
