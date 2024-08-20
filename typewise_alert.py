from abc import ABC, abstractmethod

class Electric_Cooling:
   
    class Cooling_Type(ABC):
        @abstractmethod
        def classify_temperature_breach(self, TemperatureInC):
            pass

    class Passive_Cooling(Cooling_Type):
        def classify_temperature_breach(self, TemperatureInC):
            return Electric_Cooling.infer_breach(TemperatureInC, 0, 35)

    class Hi_Active_Cooling(Cooling_Type):
        def classify_temperature_breach(self, TemperatureInC):
            return Electric_Cooling.infer_breach(TemperatureInC, 0, 45)

    class Med_Active_Cooling(Cooling_Type):
        def classify_temperature_breach(self, TemperatureInC):
            return Electric_Cooling.infer_breach(TemperatureInC, 0, 40)

    
    @staticmethod
    def infer_breach(value, lower_limit, upper_limit):
        if value < lower_limit:
            return 'TOO_LOW'
        if value > upper_limit:
            return 'TOO_HIGH'
        return 'NORMAL'


    class Alert(ABC):
        @abstractmethod
        def send_alert(self, breach_type):
            pass

    class Alert_to_Controller(Alert):
        def send_alert(self, breach_type):
            return f'Controller Alert: {breach_type}'

    class Alert_to_Email(Alert):
        def send_alert(self, breach_type):
            recipient = "a.b@c.com"
            if breach_type == 'TOO_LOW':
                return f'To: {recipient}\nHi, The temperature is too low'
            elif breach_type == 'TOO_HIGH':
                return f'To: {recipient}\nHi, The temperature is too high'
            return 'No Action Needed'

    
    @staticmethod
    def check_and_alert(alert_strategy, cooling_type_strategy, TemperatureInC):
        breach_type = cooling_type_strategy.classify_temperature_breach(TemperatureInC)
        return alert_strategy.send_alert(breach_type)
