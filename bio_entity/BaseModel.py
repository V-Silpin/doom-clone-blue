from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, x, y, health, strength, speed):
        self.x = x
        self.y = y
        self.health = health
        self.strength = strength
        self.speed = speed
        self.mask = None
        
    @abstractmethod
    def locomotion(self):
        pass

    @abstractmethod
    def offense(self):
        pass
    
    @abstractmethod
    def collide(self):
        pass