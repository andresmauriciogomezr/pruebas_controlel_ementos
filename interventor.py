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


import random
import os
import pprint


class Interventor(unittest.TestCase):

    def __init__(self, base_url, browser, requestData):    
        
        self.base_url = base_url
        #self.browser = browser

        if browser == 'crhome' :
            self.driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
        elif browser == 'firefox' :
            self.driver = webdriver.Firefox()
        else :
            self.driver = webdriver.Ie('C:\IEDriverServer\IEDriverServer.exe')
        
        self.username = "agomezr@argos.com.co"
        self.password = "agomezr@argos.com.co"

        self.requestData = requestData

        #time.sleep(5)


    def login(self):
        driver = self.driver
        driver.get(self.base_url)

        # Espera hasta que se muestre el botón Terceros
        TercerosButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnUserTercero')))
        TercerosButton.click()


        emailInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#Email')))
        emailInput.clear()
        emailInput.send_keys(self.username)
        
        
        passwordInput = driver.find_element_by_css_selector("input#Password")
        passwordInput.clear()
        passwordInput.send_keys(self.password)

        
        # El Botón de inicio de sesión
        driver.find_element_by_css_selector("input.btn-primary").click()


    def link_to_pending_requests(self, linkTo):
        driver = self.driver
        
        # Espera hasta que el link esté presente
        menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Ingreso Elementos')))
        menu.click() 

        # Espera hasta que el link esté presente y hace clic
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, linkTo)))
        mouse = ActionChains(driver)
        mouse.move_to_element(link)
        mouse.perform()

        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT , 'Solicitudes Pendientes')))
        link.click()


    def find_request(self):
        driver = self.driver
        requestId = self.requestData['requestId'] # viene desde el tercero que crea la solicitud

        # encuentra las filas de la tabla
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table#request_table')))
        elements  = table.find_elements_by_css_selector('tbody tr')

        # Busca en la primer columna de cada fila el consecutivo de la solicitud a gestionar
        requestRow = None
        for row in elements:
            # Busca la primer columna, extrae el consecutivo y lo limpia para comparar
            idCell = row.find_elements_by_css_selector('th')[0]
            consecutive = idCell.get_attribute('innerHTML').strip()

            if consecutive == requestId: # Encuentra la solicitud
                requestRow = row
                break
        
        if requestRow is not None:
            # Busca el botón "Revisar" y lo presiona
            requestButton = WebDriverWait(requestRow, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn-primary')))
            requestButton.click()
        else:
            driver.find_element_by_css_selector('a#request_table_next').click()
            self.find_request()


    def confirm_elemants(self):
        driver = self.driver

        # encuentra las filas de la tabla
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table#element-table')))
        elements  = table.find_elements_by_css_selector('tbody tr')
        
        for row in elements:
            columns = row.find_elements_by_css_selector('td')

            # Presiona el checkbox confirmar para el elemento
            checkbox = row.find_element_by_css_selector('input.checkbox')
            checkbox.click()
        
        try: # Trata de cambiar la pagina de la tabla y la vuelve a recorrer
            driver.find_element_by_css_selector('a#confirm-element-table_next').click()
            self.confirm_elemants()
        except:
            return
            # Confirma la solicitud
            confirmRequestButton = driver.find_element_by_css_selector('button#request-confirm-button')
            confirmRequestButton.click()



    def approve_request(self, linkTo):
        driver = self.driver

        self.login()
        self.link_to_pending_requests(linkTo)
        self.find_request()
        self.confirm_elemants()

        # Presiona el botón "Aprobar Seleccionados"
        try:
            driver.find_element(By.XPATH, '//button[text()="Aprobar Seleccionados"]').click()
        except:
            driver.find_element(By.XPATH, '//button[text()="Aprobar Selección"]').click()

        # Confirma la aprobación en la ventana modal emervente
        modalWindow = driver.find_element_by_css_selector('#approveConfirmation-modal')
        modalWindow = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#approveConfirmation-modal')))
        acceptButton = modalWindow.find_element_by_css_selector('button.btn-success').click()

        driver.quit();
        


