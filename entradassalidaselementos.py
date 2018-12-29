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


import random
import os
import pprint



class EntradaSalidaElementos(unittest.TestCase):

    def setUp(self, browser = "crhome"):

        self.browser = browser
        self.base_url = "http://179.32.43.198/ControlElementos/"
        #self.base_url = "http://localhost:52087/"

    def ttest_flujo_entrada_elementos(self):

        terceroDriver = tercero.IngressRequest(self.base_url, self.browser)
        requestData = terceroDriver.create_element_ingress_request()

        #requestData = {'requestId' : '170' }
        guardaDriver = guarda.Guarda(self.base_url, self.browser, requestData)
        guardaDriver.approve_request('Solicitudes de Terceros')

        #time.sleep(5)

    def ttest_flujo_salida_elementos(self):
        #requestData = self.requestData
        requestData = {'requestId' : "229" }

        terceroDriver = tercero.DepartureRequest(self.base_url, self.browser, requestData['requestId'])
        terceroDriver.create_element_departure_request()

        guardaDriver = guarda.Guarda(self.base_url, self.browser, requestData)
        guardaDriver.approve_request('Solicitudes de Terceros')

        time.sleep(5)

    def test_flujo_normal_entrada_salida_elementos(self):

        terceroDriver = tercero.IngressRequest(self.base_url, self.browser)
        requestData = terceroDriver.create_element_ingress_request()

        #requestData = {'requestId' : '170' }
        guardaDriver = guarda.Guarda(self.base_url, self.browser, requestData)
        requestData = guardaDriver.approve_request('Solicitudes de Terceros')

        terceroDriver = tercero.DepartureRequest(self.base_url, self.browser, requestData)
        terceroDriver.create_element_departure_request()
        return
        guardaDriver = guarda.Guarda(self.base_url, self.browser, requestData)
        guardaDriver.approve_request('Solicitudes de Terceros')

    def ttest_editar_salida_elementos(self):

        requestData = {'requestId' : '189' }

        terceroDriver = tercero.DepartureRequest(self.base_url, self.browser, requestData['requestId'])
        terceroDriver.modify_element_departure_request()

        time.sleep(5)

        return

        guardaDriver = guarda.Guarda(self.base_url, self.browser, requestData)
        guardaDriver.approve_request('Solicitudes de Terceros')


if __name__ == "__main__":
    unittest.main()
