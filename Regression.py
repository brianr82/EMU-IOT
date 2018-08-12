import pandas as pd
import numpy as np
import statsmodels.api as sm
import glob


class Regression:
    def __init__(self,dataDirectory):

        self.dataDirectory = dataDirectory
        self.usage_readings = None


    def __readData(self):

        self.usage_readings = pd.concat([pd.read_csv(f, sep='\t')
                          for f in glob.glob(self.dataDirectory + '/*')]
                         , ignore_index = True)

        print('Done reading')
        self.usage_readings.head()

    def __generateRegressionFunction(self,target_utilization):

        self.__readData()
        #x= self.usage_readings["sensor_count"]
        #y= self.usage_readings["host_cpu"]


        #model = sm.OLS(y,x)
        #results = model.fit()
        #print (results.summary())



        #print(dir(results))
        #print (results.fvalue)
        #print (results.f_pvalue)
        #print (results.f_test)


        x= self.usage_readings["sensor_count"]
        x = np.vander(x,2)
        y= self.usage_readings["host_cpu"]

        model = sm.OLS(y,x)
        results = model.fit()
        print (results.summary())

        #print(results.params[0])

        print(dir(results))

        prob_fstatistic = results.f_pvalue
        x_coff = results.params[0]
        b_constant = results.params[1]

        coef_pvalue = results.pvalues[0]
        constant_pvalue= results.pvalues[1]

        print ('F Prob stat(if less than 0.05 is good): '+ str(prob_fstatistic))
        print ('Coef:' + str(x_coff))
        print ('constant:' + str(b_constant))

        print ('P Coef:' + str(coef_pvalue))
        print ('P constant:' + str(constant_pvalue))


        print('Target Utilization = ' +str(target_utilization))


        if coef_pvalue < 0.05 and constant_pvalue < 0.05:
            print('Model is statistically significant')
            predicted_number_of_sensors  =  int(round((target_utilization - b_constant) // x_coff))
            print ('Predicted Number of sensors required to reach a target utilizaiton of '+ str(target_utilization) + '% :' +  str(predicted_number_of_sensors))
            return predicted_number_of_sensors
        else:
            print ('Model is NOT statistically significant')
            return 0

    def getGenerateTestCase(self,targetUtlization):
        return self.__generateRegressionFunction(targetUtlization)









