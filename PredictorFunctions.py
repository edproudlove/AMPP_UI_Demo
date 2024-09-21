#File with stuff that can be imported into the UI code
import numpy as np

#I think this should be a function that everyhting can use 
def calcReynoldsAndBLThickness(temp, u, d):
    #Function calcaultes density, viscosity and Reynolds number for given Temp, veolocity and dimeter:
    density = 753.596 + 1.87748 * temp - 0.003564 * np.power(temp, 2.0)
    viscosity = 0.001002 * np.power(10.0, ((1.3277*(293.15-temp)-0.001053*np.power((298.15-temp), 2))/(temp-168.15)))

    Re = (density * u * d)/viscosity
    BL_thickness = 25 * np.power(Re, -(7/8)) * d

    return [Re, BL_thickness,density, viscosity]


class CorrosionPredictor():
    def __init__(self, model, x_scaler, y_scaler=None, input_params=None):
        self.model = model
        self.x_scaler = x_scaler
        self.y_scaler = y_scaler
        self.input_params = input_params

    def predict(self, P, T, d, v, ph):
        #Function that can get a model prediction from input data
        Re, BL_thickness,density, viscosity = calcReynoldsAndBLThickness(T, v, d)
        input_data = np.array([P, T, Re, BL_thickness, density, viscosity])
        input_data_trasnformed = self.x_scaler.transform(input_data.reshape(1, -1))
        pred = self.model.predict(input_data_trasnformed, verbose = 0)[0][0]

        # print(input_data)
        # print(input_data_trasnformed)

        self.pred = pred
        return pred

    def predict_v2(self, P, T, ph, d, v):
        #Function that can get a model prediction from input data - For the version that needs pH, Temp and Pressure
        input_data = np.array([ph, T+273.15, np.log10(v), np.log10(P), np.log10(d)])
        input_data_trasnformed = self.x_scaler.transform(input_data.reshape(1, -1))
        pred = self.model.predict(input_data_trasnformed, verbose = 0)[0][0]

        # print(input_data)
        # print(input_data_trasnformed)

        self.pred = pred
        return pred

    def displayPredictorFormat():
        print('This model takes ...')


if __name__ == '__main__':
    print('Dont run this as main, its just a test')
