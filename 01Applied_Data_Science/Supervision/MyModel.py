from scipy.optimize import minimize 
### A good follow up project would be to implement the minimisation algorithm myself

from MyFunction import *
import numpy as np

class MyModel:
    ### Construct a polynomial model with the order as a hyper parameter and customisable loss function

    def __init__(self, initial_coefficients = None, order = 1, loss_function = "MSE", loss_function_params = {}, regularisation_function = None):
        
        self.order = order

        self.ErrorFunctionDict = {"MSE": MSE(), "MAE": MAE(), "Hubber": Hubber(loss_function_params)}
        
        self.RegularisationFunctionDict = {"L1": L1, "L2": L2, "elastic_net": elastic_net}

        if loss_function in self.ErrorFunctionDict:
            self.loss_function = self.ErrorFunctionDict[loss_function]
        else:
            self.loss_function = loss_function
        
        self.regularisation_function = regularisation_function

        if initial_coefficients is None:
            self.coefficients = [0]*(self.order + 1)
        else:
            self.coefficients = initial_coefficients
        
        self.loss = 0
        
        self.x = []
        
        self.y = []
    
    def fit(self, x, y):
        self.x = x
        self.y = y
        #########################
        ### Minimise the loss ###
        # This is going to find a set of coefficients that minimises the loss function, probably similar to gradient descent method.
        coefficients = minimize(self.function_to_minimise, self.coefficients)
        
        #########################
        self.coefficients = coefficients.x
        self.loss = self.loss_function.evaluate(self.function(self.x, self.coefficients), self.y)

    def predict(self, x_test):
        return self.function(x_test, self.coefficients)
    
    def test_loss(self, x_test, y_test):
        return self.loss_function.evaluate(self.function(x_test, self.coefficients), y_test)


    def function_to_minimise(self, params):
        ### The function to minimise the is loss function which takes in the predicted values and the actual values as parameters
        ### It is the sum of the loss function and the regularisation function
        if self.regularisation_function is None:
            return self.loss_function.evaluate(self.function(self.x, params), self.y)
        else:
            return self.loss_function.evaluate(self.function(self.x, params), self.y) + self.regularisation_function.evaluate(params)

    def function(self, x, params):
        return self.polynomial(x, params) ### change to customisable function

    ########################################
    """
    Types of loss functions:

    Later I can define a class for errors and regularisation functions and then use them here.
    """

    def polynomial(self, x, params):
        order = len(params) - 1
        prediction = np.zeros(len(x))
        for i in range (0,order+1):
            prediction += params[i] * (x ** i)
        return prediction


class KNN: 
    def __init__(self, k = 5, method = "mean"):
        self.k = k
        self.x = []
        self.y = []
        self.method = method
        self.kernal = None  