# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:42:40 2020

@author: shass
"""

"Github Directory: https://github.com/shasson883/shasson883/blob/master/carRental.py"

import csv

# defining the parent class 'Car'

class Car(object):
    
    def __init__(self):
        self.__colour = ''
        self.__make = ''
        self.__model = ''
        self.__mileage = 0
        self.engineSize = ''

    # Setters

    def setColour(self, colour):
        self.__colour = colour

    def setMake(self, make):
        self.__make = make

    def setModel(self, model):
        self.__model = model

    def setMileage(self, mileage):
        self.__mileage = mileage
        
    def setEngineSize(self, engineSize):
        self.__engineSize = engineSize        
        
    # Getters    

    def getColour(self):
        return self.__colour

    def getMake(self):
        return self.__make

    def getModel(self):
        return self.__model

    def getMileage(self):
        return self.__mileage
    
    def getEngineSize(self):
        return self.__engineSize


# defining the sub class 'ElectricCar' which encompasses parent class 'Car'
        
class ElectricCar(Car):
    
    def __init__(self):
        Car.__init__(self)
        self.__numberFuelCells = 1
        
    def setNumberFuelCells(self, numberFuelCells):
        self.__numberFuelCells = numberFuelCells    
        
    def getNumberFuelCells(self):
        return self.__numberFuelCells
    
        
# defining the sub class 'PetrolCar' which encompasses parent class 'Car'
        
class PetrolCar(Car):
    
    def __init__(self):
        Car.__init__(self)
        self.__engineSize = ''
        
    def setEngineSize(self, engineSize):
        self.__engineSize = engineSize 
        
    def getEngineSize(self):
        return self.__engineSize
    

# defining the sub class 'DieselCar' which encompasses parent class 'Car'
        
class DieselCar(Car):
    
    def __init__(self):
        Car.__init__(self)
        self.__engineSize = ''
            
    def setEngineSize(self, engineSize):
        self.__engineSize = engineSize
        
    def getEngineSize(self):
        return self.__engineSize        
        
        
# defining the sub class 'HybridCar' which encompasses parent class 'Car'        
        
class HybridCar(Car):
    
    def __init__(self):
        Car.__init__(self)
        self.__numberFuelCells = 1
        self.__engineSize = ''
        
    def setNumberFuelCells(self, numberFuelCells):
        self.__numberFuelCells = numberFuelCells        
        
    def setEngineSize(self, engineSize):
        self.__engineSize = engineSize  
            
    def getNumberFuelCells(self):
        return self.__numberFuelCells

    def getEngineSize(self):
        return self.__engineSize
  

# defining the parent class 'CarFleet'

class CarFleet(object):
    
    def __init__(self):
        
        # creating lists to hold inventory of car types
        
        self.__electric_cars = []
        self.__petrol_cars = []
        self.__diesel_cars = []
        self.__hybrid_cars = []
        
        # Setting the total value of cars for each type
        
        for i in range(1, 7):
            self.__electric_cars.append(ElectricCar())
        for i in range(1, 21):
            self.__petrol_cars.append(PetrolCar())
        for i in range(1, 7):
            self.__diesel_cars.append(DieselCar())
        for i in range(1, 5):
            self.__hybrid_cars.append(HybridCar())

    # Getters - return car type lists

    def getElectricCars(self):
        return self.__electric_cars

    def getPetrolCars(self):
        return self.__petrol_cars

    def getDieselCars(self):
        return self.__diesel_cars

    def getHybridCars(self):
        return self.__hybrid_cars

    # check stock of specific car types, return string output    

    def checkCarsInStock(self):
        print('Number of Electric Cars : ' + str(len(self.getElectricCars())))
        print('Number of Petrol Cars : ' + str(len(self.getPetrolCars())))
        print('Number of Diesel Cars : ' + str(len(self.getDieselCars())))
        print('Number of Hybrid Cars : ' + str(len(self.getHybridCars())))

    # confirm car rental selection & reduce inventory of specific type by defined value 

    def rent(self, type):
        if type == 'E':
            return self.__electric_cars.pop()
        elif type == 'P':
            return self.__petrol_cars.pop()
        elif type == 'D':
            return self.__diesel_cars.pop()        
        elif type == 'H':
            return self.__hybrid_cars.pop()        

    # return car which increases inventory of specific type by the defined value

    def returnCar(self, type, car):
        if type == 'E':
            self.__electric_cars.append(car)
        elif type == 'P':
            self.__petrol_cars.append(car)
        elif type == 'D':
            self.__diesel_cars.append(car)
        elif type == 'H':
            self.__hybrid_cars.append(car)            




# defining the car rental application

    def mainMenu(self):
        rentedCar = None
        print('Welcome to Europcar\n')
        print('Current cars in stock:\n')
        self.checkCarsInStock()
        answer = input('Would you like to rent a car R or return a car U press any key to quit: ')
        answer = answer.upper()
        if answer == 'R':
            type = input('What car would you like to rent: - E for electric, P for petrol, D for diesel, H for hybrid: ')
            type = type.upper()
            rentedCar = self.rent(type)
            print('\n')
            self.mainMenu()
        elif answer == 'U':
            type = input('What car would you like to return - E for electric, P for petrol, D for diesel, H for hybrid: ')
            type = type.upper()
            self.returnCar(type, rentedCar)
            print('\n')
            self.mainMenu()
        else:
            print('Thank you for using Europcar, the service has now been closed')

# defining the save function to capture total inventory and inventory currently available for rental in .csv format

    def save_csv(self):
        with open('C:/Users/shass/Documents/Python/bigdata/CA2/europcar_rental_status.csv', mode = 'w', newline = '') as file:
            fieldnames = ['Car Type', 'Total Inventory', 'Currently Available']
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerow({'Car Type': 'Electric', 'Total Inventory': '6', 'Currently Available': str(len(self.getElectricCars()))})
            writer.writerow({'Car Type': 'Petrol', 'Total Inventory': '20', 'Currently Available': str(len(self.getPetrolCars()))})
            writer.writerow({'Car Type': 'Diesel', 'Total Inventory': '10', 'Currently Available': str(len(self.getDieselCars()))})
            writer.writerow({'Car Type': 'Hybrid', 'Total Inventory': '4', 'Currently Available': str(len(self.getHybridCars()))})   