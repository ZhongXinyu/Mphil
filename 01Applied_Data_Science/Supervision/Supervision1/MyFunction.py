import numpy as np

class Function:
    def __init__(self, name, params):
        self.name = name
        self.params = params
        self.evaluate = None

class ErrorFunction(Function):
    def __init__(self, name, params):
        super().__init__(name, params)
        self.type = "ErrorFunction"
    
class MSE(ErrorFunction):
    def __init__(self, params = {}):
        super().__init__("MSE", {})
        self.evaluate = self.MSE
    
    def MSE(self, x,y):
        return np.sum(np.square(x-y))/len(x)

class MAE(ErrorFunction):
    def __init__(self, params = {}):
        super().__init__("MAE", {})
        self.evaluate = self.MAE
    
    def MAE(self, x,y):
        return np.sum(np.abs(x-y))/len(x)

class Hubber(ErrorFunction):
    def __init__(self, params = {"sigma_": 1}):
        super().__init__("Hubber", params)
        self.evaluate = self.Hubber
    
    def Hubber(self, x,y):
        # return np.sum(np.where(np.abs(x-y) < 1, 0.5 * np.square(x-y), np.abs(x-y) - 0.5))/len(x)
        return np.sum(np.where(np.abs(x-y) < self.params["sigma_"], 0.5 * np.square(x-y), self.params["sigma_"] * np.abs(x-y) - 0.5 * self.params["sigma_"]**2))/len(x)

class Lagrangian(ErrorFunction):
    def __init__(self, params = {}):
        super().__init__("Lagrangian", {})
        self.evaluate = self.Lagrangian
    
    def Lagrangian(self, x,y):


class RegularisationFunction(Function):
    def __init__(self, name, params):
        super().__init__(name, params)

class L1(RegularisationFunction):
    def __init__(self, params = {"lambda_": 0.1}):
        super().__init__("L1", params)
        self.params = params
        self.evaluate = self.L1_Reg
    
    def L1_Reg(self, params):
        return np.sum(np.abs(params)) * self.params["lambda_"]

class L2(RegularisationFunction):
    def __init__(self, params = {"lambda_": 0.1}):
        super().__init__("L2", params)
        self.params = params
        self.evaluate = self.L2_Reg
    
    def L2_Reg(self, params):
        return np.sum(np.square(params)) * self.params["lambda_"]

class elastic_net(RegularisationFunction):
    def __init__(self, params = {"lambda_": 0.1, "alpha": 0.5}):
        super().__init__("elastic_net", params)
        self.params = params
        self.evaluate = self.elastic_net
    
    def elastic_net(self, params):
        return self.params["alpha"] * self.L1_Reg(params) + (1 - self.params["alpha"]) * self.L2_Reg(params)
