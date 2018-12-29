# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException
import unittest, time, re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import string
import guarda
import tercero
import interventor


import random
import os
import pprint



class EntradaSalidaElementos(unittest.TestCase):

    def setUp(self, browser = "firefox"):

        self.browser = browser
        self.base_url = "http://179.32.43.198/ControlElementos/"

    
    def test_flujo_salida_activos_argos(self):

        terceroDriver = tercero.ArgosDepartureRequest(self.base_url, self.browser)
        requestData = terceroDriver.create_departure_request()

        inverventorDriver = interventor.Interventor(self.base_url, self.browser, requestData)
        inverventorDriver.approve_request('Solicitudes Terceros')

        guardaDriver = guarda.Guarda(self.base_url, self.browser, requestData)
        guardaDriver.approve_request('Solicitudes de Terceros')

        guardaDriver = guarda.Guarda(self.base_url, self.browser, requestData)
        guardaDriver.approve_request('Solicitudes de Terceros')

        time.sleep(5)





if __name__ == "__main__":
    unittest.main()
