# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:52:38 2020

@author: shass
"""

"Github Directory: https://github.com/shasson883/shasson883/blob/master/carRentalApp.py"

# importing carRental code

from carRental import Car, ElectricCar, PetrolCar, DieselCar, HybridCar, CarFleet

# testing Car class

if __name__ == "__main__":
    myCar = Car()
    myCar.setColour('Red')
    myCar.setMake('Ferrari')
    myCar.setModel('Testarossa')
    myCar.setMileage(54)
    myCar.setEngineSize('1.2')
    print(myCar.getColour())
    print(myCar.getMake())
    print(myCar.getModel())
    print(myCar.getMileage())
    print(myCar.getEngineSize())
    print('\ntest successful')


# testing ElectricCar class

if __name__ == "__main__":
    electric = ElectricCar()
    electric.setMake('Nissan')
    electric.setModel('Leaf')
    print(electric.getNumberFuelCells())
    print(electric.getMake())
    print(electric.getModel())
    print('\ntest successful')
    
    
# testing PetrolCar class    
    
if __name__ == "__main__":
    petrol = PetrolCar()
    petrol.setMake('Ford')
    petrol.setModel('Focus')
    petrol.setEngineSize('1.6')
    print(petrol.getMake())
    print(petrol.getModel())
    print(petrol.getEngineSize())
    print('\ntest successful')


# testing DieselCar class

if __name__ == "__main__":
    diesel = DieselCar()
    diesel.setMake('VW')
    diesel.setModel('Polo')
    diesel.setEngineSize('1.4')
    print(diesel.getMake())
    print(diesel.getModel())
    print(diesel.getEngineSize())
    print('\ntest successful')
    

# testing HybridCar class    

if __name__ == "__main__":
    hybrid = HybridCar()
    hybrid.setMake('Toyota')
    hybrid.setModel('Prius')
    hybrid.setEngineSize('1.0')
    print(hybrid.getNumberFuelCells())
    print(hybrid.getMake())
    print(hybrid.getModel())
    print(hybrid.getEngineSize())
    print('\ntest successful')


# testing CarFleet class 

if __name__ == "__main__":
    europcar = CarFleet()
    europcar.getElectricCars()
    europcar.getPetrolCars()
    europcar.getDieselCars()
    europcar.getHybridCars()
    europcar.checkCarsInStock()
    europcar.mainMenu()
    europcar.save_csv()
    print('\ntest successful')



 

    
