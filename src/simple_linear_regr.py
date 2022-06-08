import os

import numpy as np
from simple_linear_regr_utils import generate_data, evaluate
import pickle
import dill


def create_pickle(mdl):
    dill.dump(mdl, open('slr.pkl', 'wb'))

class SimpleLinearRegression:
    def __init__(self, iterations=15000, lr=0.1):
        self.iterations = iterations # number of iterations the fit method will be called
        self.lr = lr # The learning rate
        self.losses = [] # A list to hold the history of the calculated losses
        self.W, self.b = None, None # the slope and the intercept of the model
        self.bins = None

    def __loss(self, y, y_hat):
        """

        :param y: the actual output on the training set
        :param y_hat: the predicted output on the training set
        :return:
            loss: the sum of squared error

        """
        #ToDO calculate the loss. use the sum of squared error formula for simplicity
        loss = np.square(y - y_hat)

        self.losses.append(loss)
        return loss

    def __init_weights(self, X):
        """

        :param X: The training set
        """
        weights = np.random.normal(size=X.shape[1] + 1)
        self.W = weights[:X.shape[1]].reshape(-1, X.shape[1])
        self.b = weights[-1]

    def __sgd(self, X, y, y_hat):
        """

        :param X: The training set
        :param y: The actual output on the training set
        :param y_hat: The predicted output on the training set
        :return:
            sets updated W and b to the instance Object (self)
        """
        # ToDo calculate dW & db.

        dW = (-2 * np.dot(np.transpose(X), (y - y_hat))) / X.shape[0]
        db = (-2 * np.sum(y - y_hat)) / X.shape[0]
        #  ToDO update the self.W and self.b using the learning rate and the values for dW and db
        self.W = self.W - self.lr * dW
        self.b = self.b - self.lr * db


    def fit(self, X, y):
        """

        :param X: The training set
        :param y: The true output of the training set
        :return:
        """
        self.__init_weights(X)
        y_hat = self.predict(X)
        loss = self.__loss(y, y_hat)
        print(f"Initial Loss: {loss}")
        for i in range(self.iterations + 1):
            self.__sgd(X, y, y_hat)
            y_hat = self.predict(X)
            loss = self.__loss(y, y_hat)
            if not i % 100:
                print(f"Iteration {i}, Loss: {loss}")

        _, self.bins = np.histogram(y, density=False, bins=4)

    def predict(self, X):
        """

        :param X: The training dataset
        :return:
            y_hat: the predicted output
        """
        #ToDO calculate the predicted output y_hat. remember the function of a line is defined as y = WX + b
        y_hat = self.W * X + self.b
        return y_hat


if __name__ == "__main__":
    X_train, y_train, X_test, y_test = generate_data()
    model = SimpleLinearRegression()
    model.fit(X_train,y_train)
    hist_array, bin_array = np.histogram(y_train, density=False, bins=4)
    predicted = model.predict(X_test)
    evaluate(model, X_test, y_test, predicted)
    create_pickle(model)
    # pass

# X_train, y_train, X_test, y_test = generate_data()
# model = SimpleLinearRegression()
# model.fit(X_train,y_train)
# pickle.dump(model, open('slr.pkl', 'wb'))
# predicted = model.predict(X_test)
# evaluate(model, X_test, y_test, predicted)
