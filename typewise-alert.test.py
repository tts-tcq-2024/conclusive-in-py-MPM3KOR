import unittest
import typewise_alert

class TypewiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')

    def test_infer_breach_too_high(self):
        self.assertEqual(typewise_alert.infer_breach(120, 50, 100), 'TOO_HIGH')

    def test_infer_breach_normal(self):
        self.assertEqual(typewise_alert.infer_breach(70, 50, 100), 'NORMAL')

    def test_passive_cooling_breach(self):
        cooling = typewise_alert.Passive_Cooling()
        self.assertEqual(cooling.classify_temperature_breach(45), 'TOO_HIGH')
        self.assertEqual(cooling.classify_temperature_breach(28), 'NORMAL')

    def test_hi_active_cooling_breach(self):
        cooling = typewise_alert.Hi_Active_Cooling()
        self.assertEqual(cooling.classify_temperature_breach(65), 'TOO_HIGH')
        self.assertEqual(cooling.classify_temperature_breach(40), 'NORMAL')

    def test_med_active_cooling_breach(self):
        cooling = typewise_alert.Med_Active_Cooling()
        self.assertEqual(cooling.classify_temperature_breach(47), 'TOO_HIGH')
        self.assertEqual(cooling.classify_temperature_breach(33), 'NORMAL')

    def test_controller_alert(self):
        alert = typewise_alert.Alert_to_Controller()
        self.assertEqual(alert.Send_Alert('TOO_HIGH'), 'Controller Alert: TOO_HIGH')

    def test_email_alert(self):
        alert = typewise_alert.Alert_to_Email()
        self.assertEqual(alert.Send_Alert('TOO_HIGH'), 'To: a.b@c.com\nHi, The temperature is too high')
        self.assertEqual(alert.Send_Alert('TOO_LOW'), 'To: a.b@c.com\nHi, The temperature is too low')
        self.assertEqual(alert.Send_Alert('NORMAL'), 'No Action Needed')

    def test_check_and_alert(self):
        result = typewise_alert.check_and_alert(typewise_alert.Alert_to_Controller(), typewise_alert.Hi_Active_Cooling(), 50)
        self.assertEqual(result, 'Controller Alert: TOO_HIGH')

        
        result = typewise_alert.check_and_alert(typewise_alert.Alert_to_Email(), typewise_alert.Passive_Cooling(), 30)
        self.assertEqual(result, 'No action needed')

        # Test with MedActiveCooling and EmailAlert
        result = typewise_alert.check_and_alert(typewise_alert.Alert_to_Email(), typewise_alert.Med_Active_Cooling(), 45)
        self.assertEqual(result, 'To: a.b@c.com\nHi, The temperature is too high')


if __name__ == '__main__':
    unittest.main()
