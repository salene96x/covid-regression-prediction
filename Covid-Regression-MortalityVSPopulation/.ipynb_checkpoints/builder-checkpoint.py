from sklearn.linear_model import LinearRegression
class Builder:
    def __init__(self, type_of_model : str, advance_data=None) -> list:
        if type_of_model == "LinearRegression":
            self.model = LinearRegression()
        return [self.model]
    def linear_regression_fit(self, x_train, y_train):
        self.model.fit(x_train, y_train)