# A sensor simulator class

import random

class Sensor:
    '''
        This module is responsible for producing the sensor data based on some specified criteria
        Author's Github --> sam-a-d
    '''
    
    def __init__(\
                    self, \
                    electricity=(1.5,25),   # watt-hour
                    water=(0.3,35),         # gallon
                    natural_gas=(0, 0.03),  # Cubic meter
                    air_pollution=(0.3,17), # AQI
                    crude_oil=(0.3,3.33),   # gallon
                ):
        
        self.electricity = electricity
        self.water = water
        self.natural_gas = natural_gas
        self.air_pollution = air_pollution
        self.crude_oil = crude_oil

        # Storing the generated powers and pass them to the producer
        self.genElectricity, self.genWater, self.genNaturalGas, self.genCrudeOil = (None, None, None, None);
    
    # Resource utilization unit -------
    # 1.
    def getElectricity(self, *args):

        self.electricity = args[0] if args else self.electricity
        self.genElectricity = round(random.uniform(*self.electricity), 2)
        return self.genElectricity

    # 2. 
    def getWater(self, *args):

        self.water = args[0] if args else self.water
        return round(random.uniform(*self.water), 2)
    
    # 3.
    def getNaturalGas(self, *args):

        self.natural_gas = args[0] if args else self.natural_gas
        self.genNaturalGas = round(random.uniform(*self.natural_gas), 2)
        return self.genNaturalGas

    # 4.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    def getCrudeOil(self, *args):

        self.crude_oil = args[0] if args else self.crude_oil
        return round(random.uniform(*self.crude_oil), 2)
    
    # 5.
    def getAirPollution(self, *args):

        self.air_pollution = args[0] if args else self.air_pollution
        return round(random.uniform(*self.air_pollution), 2)
    
    # the resouce production unit -------

    def __biased_random(self):
        if random.random() < 0.8:  # 80% chance
            return random.uniform(0, 0.5)  # Generate a number between 0-0.5
        else:
            return random.uniform(0.5, 1)  # Generate a number between 0.5-1

    # 1. Solar energy production --> Linked with electricity consumption 
    def getSolarProduction(self, *args):
        
        return self.genElectricity * self.__biased_random()

    # 2. Hydrological energy production  --> Linked with electricity consumption
    def getHydrologicalProduction(self):

        return self.genElectricity * self.__biased_random()

    # 3. Wind energy production --> Linked with electricity consumption
    def getWindProduction(self, *args):
        
        return self.genElectricity * self.__biased_random()

    # 4. Biogas production --> Linked with natural gas consumption
    def getBioGasProduction(self, *args):
        
        return self.genNaturalGas * self.__biased_random()

    # 1-4 RES ---> Renewable Energy Production
    # def renewableEnergyProduction(self, *args):
    #     return self.__biased_random()

