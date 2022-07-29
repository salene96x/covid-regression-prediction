from sklearn.linear_model import LinearRegression
class Builder:
    def __init__(self) -> None:
        pass
    def build_model(self, type_of_model : str):
        model = None
        if type_of_model == "LinearRegression":
            model = LinearRegression()
        return model
    def linear_regression_fit(self, x_train, y_train, model):
        model.fit(x_train, y_train)
        return model