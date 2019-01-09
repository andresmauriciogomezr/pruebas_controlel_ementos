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


class UsuarioOperador(unittest.TestCase):

    def __init__(self, base_url, browser, requestData):    
        
        self.utilities = utilities.Utilities()
        self.base_url = base_url
        #self.browser = browser

        if browser == 'crhome' :
            self.driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
        elif browser == 'firefox' :
            self.driver = webdriver.Firefox()
        else :
            self.driver = webdriver.Ie('C:\IEDriverServer\IEDriverServer.exe')
        self.driver.maximize_window()
        
        self.username = "usuariooperador@argos.com"
        self.password = "Ingresos1*"

        self.requestData = requestData

        #time.sleep(5)
        self.utilities = utilities.Utilities()

        print("********************* Usuario Operador ************************************")

    def link_to_pending_requests(self, linkTo):
        driver = self.driver
        
        # Espera hasta que el link esté presente
        menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Ingreso Elementos')))
        menu.click() 

        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT , linkTo)))
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

    def confirm_elemants(self, confirmedElements = []):
        driver = self.driver

        # encuentra las filas de la tabla
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table#element-table')))
        elements  = table.find_elements_by_css_selector('tbody tr')
        
        for row in elements:
            columns = row.find_elements_by_css_selector('td')

            # Presiona el checkbox confirmar para el elemento
            checkbox = row.find_element_by_css_selector('input.checkbox')
            self.utilities.scrollToElement(driver, checkbox)
            checkbox.click()
            
            # Busca el elemento y le cambia el estado, luego lo actualiza
            description = columns[2].get_attribute('innerHTML').strip()
            temporalElemtn = next(item for item in self.requestData['elements'] if item["description"] == description)
            temporalElemtn['status'] = 'Salida Aprobada'
            confirmedElements.append(temporalElemtn)


        nextPageButton = driver.find_element_by_css_selector('a#element-table_next')
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

        if self.requestData['requestType'] == "Salida Activos de Argos":
            self.assert_terceeros_departure_request()
        elif self.requestData['requestType'] == "Orden de Salida":
            self.assert_orden_salida()
        elif self.requestData['requestType'] == "Solicitud de Traslado":
            self.assert_transfer_request()
        else:
            self.assert_request()

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

        print("Solicitud " + self.requestData["requestId"] + " Aprobada con " +str(len(self.requestData['elements']))+ " elementos")
        driver.quit();
        
    def assert_terceeros_departure_request(self):
        driver = self.driver

        # Busca los datos de la solicitud y hace las comparaciones correspondientes
        plantdd = driver.find_element_by_xpath('//dl[dt/label[contains(text(),"Planta Origen")]]/dd').get_attribute('innerHTML').strip()
        destinydd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Destino")]]/dd').get_attribute('innerHTML').strip()
        ingressReassondd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Motivo de Salida")]]/dd').get_attribute('innerHTML').strip()
        #returnDatedd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Fecha de Retorno")]]/dd').find_element_by_css_selector('input').get_attribute('value').strip()
        responsabledd = driver.find_element_by_xpath('//h4[contains(text(), "Responsable")]/strong').get_attribute('innerHTML').strip()
        interventordd = driver.find_element_by_xpath('//dl[dt/label[contains(text(),"Aprobado por")]]/dd').get_attribute('innerHTML').strip()
        requestTypedd = driver.find_element_by_xpath('//h3[contains(text(), "Tipo de Solicitud")]/strong').get_attribute('innerHTML').strip()

        #assert self.requestData["requestType"] == "Salida Activos de Argos"
        assert plantdd == self.requestData['plant']
        #assert self.requestData['returnDate'] == returnDatedd
        assert self.requestData['destiny'] == destinydd
        assert self.requestData['departureReasson'] == ingressReassondd
        assert self.requestData['responsable'] in responsabledd
        assert self.requestData['interventor'] == interventordd
        assert self.requestData['interventor'] == interventordd

        print("Comparados datos de solicitud...")

        # Hace las comparaciones con los elementos resultantes y los elementos guardados al momento de crear la solicitud
        self.assert_terceeros_departure_request_elements(0)        

    def assert_terceeros_departure_request_elements(self, checkedElementsAmount = 0):
        driver = self.driver
        elements = self.requestData['elements']

        # Busca los elementos en la tabla de la solicitud creada
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#element-table")))
        webElements = table.find_elements_by_css_selector('tbody tr')

        for webElement in webElements:
            # Busca los datos de cada elemento en la fila
            webElementCells = webElement.find_elements_by_css_selector('td')
            webElementDescription = webElementCells[2].get_attribute('innerHTML').strip()
            webElementCategory = webElementCells[3].get_attribute('innerHTML').strip()
            webElementAmount = webElementCells[4].get_attribute('innerHTML').strip()
            webElementSerial = webElementCells[5].get_attribute('innerHTML').strip()
            webElementStatus = webElementCells[7].get_attribute('innerHTML').strip()

            # Hace las respectivas comparaciones por elemento
            for element in elements:
                if element['description'] == webElementDescription:
                    assert self.requestData['elementCategory'] == webElementCategory
                    assert str(element['amount']) == webElementAmount
                    assert element['serial'] == webElementSerial

                    assert element['status'] == webElementStatus

                    checkedElementsAmount += 1 # Para revisar la siguiente página de la tabla y llevar el registro de lo revisado
                    break

        # Busca el botón para la siguiente pagina
        nextPageButton = driver.find_element_by_css_selector("a#element-table_next")
        if self.utilities.has_class(nextPageButton, 'disabled') == False: # Se puede presionar
            nextPageButton.click()
            self.assert_terceeros_departure_request_elements(checkedElementsAmount)
        else: # Ya no hay más paginas disponibles
            assert checkedElementsAmount == len(elements) # Compara la cantidad de elementos en la tabla con los guardados
            self.utilities.return_table_to_firstpage(driver, "element-table")
            print("Comparados datos de elementos...")

    def assert_orden_salida(self):
        driver = self.driver

        # Busca los datos de la solicitud y hace las comparaciones correspondientes
        plantdd = driver.find_element_by_xpath('//dl[dt/label[contains(text(),"Planta")]]/dd').get_attribute('innerHTML').strip()
        returnDatedd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Fecha de Retorno")]]/dd').get_attribute('innerHTML').strip()
        destinydd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Destino")]]/dd').get_attribute('innerHTML').strip()
        #responsabledd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Responsable")]]/dd').get_attribute('innerHTML').strip()
        departureReassondd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Motivo de Salida")]]/dd').get_attribute('innerHTML').strip()
        interventordd = driver.find_element_by_xpath('//dl[dt/label[contains(text(),"Aprobado por")]]/dd').get_attribute('innerHTML').strip()

        assert self.requestData["requestType"] == "Orden de Salida"
        assert plantdd == self.requestData['plant']
        assert self.requestData['returnDate'] == returnDatedd
        assert self.requestData['destiny'] == destinydd
        #assert self.requestData['responsable'] in responsabledd
        assert self.requestData['departureReasson'] in departureReassondd
        assert self.requestData['interventor'] == interventordd

        print("Comparados datos de solicitud...")

        # Hace las comparaciones con los elementos resultantes y los elementos guardados al momento de crear la solicitud
        self.assert_orden_salida_elements(0)

    def assert_orden_salida_elements(self, checkedElementsAmount = 0):
        driver = self.driver
        elements = self.requestData['elements']

        # Busca los elementos en la tabla de la solicitud creada
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#element-table")))
        webElements = table.find_elements_by_css_selector('tbody tr')

        for webElement in webElements:
            # Busca los datos de cada elemento en la fila
            webElementCells = webElement.find_elements_by_css_selector('td')
            webElementDescription = webElementCells[2].get_attribute('innerHTML').strip()
            webElementCategory = webElementCells[3].get_attribute('innerHTML').strip()
            webElementAmount = webElementCells[4].get_attribute('innerHTML').strip()
            webElementSerial = webElementCells[5].get_attribute('innerHTML').strip()
            webElementStatus = webElementCells[7].get_attribute('innerHTML').strip()

            # Hace las respectivas comparaciones por elemento
            for element in elements:
                if element['description'] == webElementDescription:
                    assert self.requestData['elementCategory'] == webElementCategory
                    assert int(element['amount']) == int(float(webElementAmount.replace(",", ".")))
                    assert element['serial'] == webElementSerial
                    assert element['status'] in webElementStatus

                    checkedElementsAmount += 1 # Para revisar la siguiente página de la tabla y llevar el registro de lo revisado
                    break

        # Busca el botón para la siguiente pagina
        nextPageButton = driver.find_element_by_css_selector("a#element-table_next")
        if self.utilities.has_class(nextPageButton, 'disabled') == False: # Se puede presionar
            nextPageButton.click()
            self.assert_orden_salida_elements(checkedElementsAmount)
        else: # Ya no hay más paginas disponibles
            assert checkedElementsAmount == len(elements) # Compara la cantidad de elementos en la tabla con los guardados
            self.utilities.return_table_to_firstpage(driver, "confirm-element-table")
            print("Comparados datos de elementos...")

    def assert_transfer_request_elements(self, checkedElementsAmount = 0):
        driver = self.driver
        elements = self.requestData['elements']

        # Busca los elementos en la tabla de la solicitud creada
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#element-table")))
        webElements = table.find_elements_by_css_selector('tbody tr')

        for webElement in webElements:
            # Busca los datos de cada elemento en la fila
            webElementCells = webElement.find_elements_by_css_selector('td')
            webElementDescription = webElementCells[2].get_attribute('innerHTML').strip()
            webElementCategory = webElementCells[3].get_attribute('innerHTML').strip()
            webElementAmount = webElementCells[4].get_attribute('innerHTML').strip().replace(",", ".")
            webElementSerial = webElementCells[5].get_attribute('innerHTML').strip()
            webElementStatus = webElementCells[7].get_attribute('innerHTML').strip()

            # Hace las respectivas comparaciones por elemento
            for element in elements:
                if element['description'] == webElementDescription:
                    assert self.requestData['elementCategory'] == webElementCategory
                    assert int(element['amount']) == int(float(webElementAmount))
                    assert element['serial'] == webElementSerial
                    assert element['status'] in webElementStatus

                    checkedElementsAmount += 1 # Para revisar la siguiente página de la tabla y llevar el registro de lo revisado
                    break

        # Busca el botón para la siguiente pagina
        nextPageButton = driver.find_element_by_css_selector("a#element-table_next")
        if self.utilities.has_class(nextPageButton, 'disabled') == False: # Se puede presionar
            nextPageButton.click()
            self.assert_transfer_request_elements(checkedElementsAmount)
        else: # Ya no hay más paginas disponibles
            assert checkedElementsAmount == len(elements) # Compara la cantidad de elementos en la tabla con los guardados
            self.utilities.return_table_to_firstpage(driver, "element-table")
            print("Comparados datos de elementos...")

    def assert_transfer_request(self):
        driver = self.driver

        # Busca los datos de la solicitud y hace las comparaciones correspondientes
        plantdd = driver.find_element_by_xpath('//dl[dt/label[contains(text(),"Planta Origen")]]/dd').get_attribute('innerHTML').strip()
        destinyPlantdd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Planta")]]/dd').get_attribute('innerHTML').strip()
        responsabledd = driver.find_element_by_xpath('//h4[contains(text(), "Responsable")]//strong').get_attribute('innerHTML').split(".")[1].strip()
        departureReassondd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Motivo de Salida")]]/dd').get_attribute('innerHTML').strip()
        #self.requestData['destiny'] = 'Destino de prueba'
        interventordd = driver.find_element_by_xpath('//dl[dt/label[contains(text(),"Aprobado por")]]/dd').get_attribute('innerHTML').strip()

        
        assert self.requestData['interventor'] == interventordd
        assert self.requestData["requestType"] == "Solicitud de Traslado"
        assert plantdd == self.requestData['plant']
        assert self.requestData['destinyPlant'] == destinyPlantdd
        assert self.requestData['departureReasson'] in departureReassondd
        assert self.requestData['responsable'] in responsabledd

        print("Comparados datos de solicitud...")

        # Hace las comparaciones con los elementos resultantes y los elementos guardados al momento de crear la solicitud
        self.assert_transfer_request_elements(0)

