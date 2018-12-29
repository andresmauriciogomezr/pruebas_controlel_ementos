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
import utilities
import random
import os
import pprint

#import interventor

class Guarda(unittest.TestCase):

    def __init__(self, base_url, browser, requestData):    
        
        self.utilities = utilities.Utilities()
        self.base_url = base_url

        if browser == 'crhome' :
            self.driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
        elif browser == 'firefox' :
            self.driver = webdriver.Firefox()
        else :
            self.driver = webdriver.Ie('C:\IEDriverServer\IEDriverServer.exe')
        
        self.username = "guardacanteraeltriunfo@argos.com"
        self.password = "guardacanteraeltriunfo@argos.com"

        self.requestData = requestData

        print("********************* Guarda ************************************")
        #time.sleep(5)

    def link_to_pending_requests(self, linkTo):
        driver = self.driver
        
        # Espera hasta que el link esté presente
        menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Ingreso Elementos')))
        menu.click()

        # Espera hasta que el link esté presente y hace clic
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, linkTo)))
        mouse = ActionChains(driver)
        mouse.move_to_element(link).click()
        mouse.perform()

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

    def confirm_elemants(self, confirmedElements = []):
        driver = self.driver

        # encuentra las filas de la tabla
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table#confirm-element-table')))
        elements  = table.find_elements_by_css_selector('tbody tr')
            
        for row in elements:
            randomNumber = random.randrange(1,11)
            if randomNumber < 9:# Le da el 90% de probabilidad de aprobar el elemento
                columns = row.find_elements_by_css_selector('td')
                
                # Arma unas observaciones con la descripción y la cntidad
                description = columns[2].get_attribute('innerHTML').strip()
                amount = columns[3].get_attribute('innerHTML').strip()
                observations = 'Confirmando ' + description + ' - Cantidad: ' + amount                

                # Agrega las observaciones
                observationsInput = row.find_element_by_css_selector('textarea.guardObservations')
                observationsInput.clear()
                observationsInput.send_keys(observations)

                # Presiona el botón confirmar para el elemento
                confirmElementButton = row.find_element_by_css_selector('button.confirm-button')
                confirmElementButton.click()

                # Agrega el elemento confirmado
                confirmedElements.append(next(item for item in self.requestData['elements'] if item["description"] == description))


        nextPageButton = driver.find_element_by_css_selector('a#confirm-element-table_next')
        if self.utilities.has_class(nextPageButton, 'disabled') == False: # Se puede presionar
            nextPageButton.click()
            return self.confirm_elemants(confirmedElements)
        else:
            return confirmedElements
            
    def approve_request(self, linkTo):
        driver = self.driver

        self.utilities.login(self.driver, self.base_url, self.username, self.password)
        self.link_to_pending_requests(linkTo)
        self.find_request()

        # Hace las comparaciones necesarias
        self.assert_request()

        # Confirma los elementos
        confirmedElements = self.confirm_elemants()
    
        # confirma la solicitud
        confirmRequestButton = driver.find_element_by_css_selector('button#request-confirm-button')
        confirmRequestButton.click()

        print("Solicitud " +self.requestData['requestId']+ " confirmada con " +str(len(confirmedElements))+ " elementos confirmados")
        if len(confirmedElements) < len(self.requestData['elements']):# La contidad de elementos confirmados es menor a la cantidad real de elementos
            # Hace clic en el botón confirma de la ventana emergente p
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button#confirm-ingress-modal-button'))).click()


        # Actualiza los elementos de la solicitud con lo que fueron confirmados
        self.requestData['elements'] = confirmedElements
        
        driver.quit();

        return self.requestData

    def assert_request(self):
        driver = self.driver
        self.utilities = utilities.Utilities()

        # Busca los datos de la solicitud y hace las comparaciones correspondientes
        responsabledd = driver.find_element_by_xpath('//h4[contains(text(), "Responsable")]').get_attribute('innerHTML').strip()

        assert self.requestData['trabajador'] in responsabledd

        print("Comparados datos de solicitud")
        # Hace las comparaciones con los elementos resultantes y los elementos guardados al momento de crear la solicitud
        self.assert_elements()

    def assert_elements(self, checkedElementsAmount = 0):
        driver = self.driver
        elements = self.requestData['elements']

        # Busca los elementos en la tabla de la solicitud creada
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#confirm-element-table")))
        webElements = table.find_elements_by_css_selector('tbody tr')

        for webElement in webElements:
            # Busca los datos de cada elemento en la fila
            webElementCells = webElement.find_elements_by_css_selector('td')
            webElementDescription = webElementCells[2].get_attribute('innerHTML').strip()
            webElementAmount = webElementCells[4].get_attribute('innerHTML').strip()
            webElementSerial = webElementCells[5].get_attribute('innerHTML').strip()

            # Hace las respectivas comparaciones por elemento
            for element in elements:
                if element['description'] == webElementDescription:
                    assert element['serial'] == webElementSerial
                    #assert int(element['amount']) == int(float(webElementAmount))

                    checkedElementsAmount += 1 # Para revisar la siguiente página de la tabla y llevar el registro de lo revisado
                    break

        # Busca el botón para la siguiente pagina
        nextPageButton = driver.find_element_by_css_selector("a#confirm-element-table_next")
        if self.utilities.has_class(nextPageButton, 'disabled') == False: # Se puede presionar
            nextPageButton.click()
            self.assert_elements(checkedElementsAmount)
        else: # Ya no hay más paginas disponibles
            assert checkedElementsAmount == len(elements) # Compara la cantidad de elementos en la tabla con los guardados
            #Regresa la tabla a la primer pagina
            self.utilities.return_table_to_firstpage(driver, "confirm-element-table")
            print("Comparados datos de elementos")
