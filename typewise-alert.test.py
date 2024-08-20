import unittest
from typewise_alert import Electric_Cooling

class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        self.assertTrue(Electric_Cooling.infer_breach(20, 50, 100) == 'TOO_LOW')

    def test_infer_breach_too_high(self):
        self.assertEqual(Electric_Cooling.infer_breach(120, 50, 100), 'TOO_HIGH')

    def test_infer_breach_normal(self):
        self.assertEqual(Electric_Cooling.infer_breach(70, 50, 100), 'NORMAL')

    def test_passive_cooling_breach(self):
        cooling = Electric_Cooling.Passive_Cooling()
        self.assertEqual(cooling.classify_temperature_breach(50), 'TOO_HIGH')
        self.assertEqual(cooling.classify_temperature_breach(30), 'NORMAL')

    def test_hi_active_cooling_breach(self):
        cooling = Electric_Cooling.Hi_Active_Cooling()
        self.assertEqual(cooling.classify_temperature_breach(90), 'TOO_HIGH')
        self.assertEqual(cooling.classify_temperature_breach(40), 'NORMAL')

    def test_med_active_cooling_breach(self):
        cooling = Electric_Cooling.Med_Active_Cooling()
        self.assertEqual(cooling.classify_temperature_breach(90), 'TOO_HIGH')
        self.assertEqual(cooling.classify_temperature_breach(35), 'NORMAL')

    def test_controller_alert(self):
        alert = Electric_Cooling.Alert_to_Controller()
        self.assertEqual(alert.send_alert('TOO_HIGH'), 'Controller Alert: TOO_HIGH')

    def test_email_alert(self):
        alert = Electric_Cooling.Alert_to_Email()
        self.assertEqual(alert.send_alert('TOO_HIGH'), 'To: a.b@c.com\nHi, The temperature is too high')
        self.assertEqual(alert.send_alert('TOO_LOW'), 'To: a.b@c.com\nHi, The temperature is too low')
        self.assertEqual(alert.send_alert('NORMAL'), 'No Action Needed')

    def test_check_and_alert(self):
        
        result = Electric_Cooling.check_and_alert(Electric_Cooling.Alert_to_Controller(), Electric_Cooling.Hi_Active_Cooling(), 50)
        self.assertEqual(result, 'Controller Alert: TOO_HIGH')

        
        result = Electric_Cooling.check_and_alert(Electric_Cooling.Alert_to_Email(), Electric_Cooling.Passive_Cooling(), 30)
        self.assertEqual(result, 'No Action Needed')

        
        result = Electric_Cooling.check_and_alert(Electric_Cooling.Alert_to_Email(), Electric_Cooling.Med_Active_Cooling(), 45)
        self.assertEqual(result, 'To: a.b@c.com\nHi, The temperature is too high')

if __name__ == '__main__':
    unittest.main()
