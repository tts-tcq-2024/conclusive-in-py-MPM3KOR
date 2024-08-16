from abc import ABC, abstractmethod

def infer_breach(value, lowerLimit, upperLimit):
  if value < lowerLimit:
    return 'TOO_LOW'
  if value > upperLimit:
    return 'TOO_HIGH'
  return 'NORMAL'

class Cooling_Type(ABC):
    @abstractmethod
    def classify_temperature_breach(self, temperatureInC):
        pass

class Passive_Cooling(Cooling_Type):
    def classify_temperature_breach(self, temperatureInC):
        return infer_breach(temperatureInC, 0, 35)

class Hi_Active_Cooling(Cooling_Type):
    def classify_temperature_breach(self, temperatureInC):
        return infer_breach(temperatureInC, 0, 45)

class Med_Active_Cooling(Cooling_Type):
    def classify_temperature_breach(self, temperatureInC):
        return infer_breach(temperatureInC, 0, 40)

# Alert strategies
class Send_Alert(ABC):
    @abstractmethod
    def Send_Alert(self, breach_type):
        pass

class Alert_to_Controller(Send_Alert):
    def Send_Alert(self, breach_type):
        header = 0xfeed
        print(f'{header}, {breach_type}')

class Alert_to_Email(Send_Alert):
    def Send_Alert(self, breach_type):
        recipient = "a.b@c.com"
        if breach_type == 'TOO_LOW':
            print(f'To: {recipient}')
            print('Hi, the temperature is too low')
        elif breach_type == 'TOO_HIGH':
            print(f'To: {recipient}')
            print('Hi, the temperature is too high')

# Core function using strategies
def check_and_alert(alert_strategy, cooling_type_strategy, temperatureInC):
    breach_type = cooling_type_strategy.classify_temperature_breach(temperatureInC)
    alert_strategy.Send_Alert(breach_type)

# Usage
cooling_type = Hi_Active_Cooling() 
alert = Alert_to_Controller()  

check_and_alert(alert, cooling_type, 50)
