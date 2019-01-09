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




class selector_got_options(object):
  """An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator, minOptionsNumber):
    self.locator = locator
    self.minOptionsNumber = minOptionsNumber

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    options = Select(element).options
    if len(options) > self.minOptionsNumber:
        return element
    else:
        return False

class OrderRequest(unittest.TestCase):

    def __init__(self, base_url, browser):    
        print("********************* Usuario Argos ************************************")
        
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
        
        self.username = "primerusuarioargos@argos.com.co"
        self.password = "Ingresos1*"

        self.zonaFrancaPlant = "PLANTA CEMENTOS CARTAGENA ZFA"
        self.plantName = "CANTERA EL TRIUNFO"

        self.interventorName = 'Andrés Mauricio Gómez'

        self.herramientas = [
            "Allanadoras",
            "Cortadoras de Pavimento",
            "Placas Compactadoras",
            "Mezcladoras",
            "Rotomartillo",
            "Carretillas y Ruedas",
            "Carga y Levante",
            "Bombas Hidraulicas",
            "Compactadoras Hidraulicas",
            "Esmeriladores Hidraulicos",
            "Fuentes de Poder Hidraulico",
            "Malacates",
            "Mototaladros",
            "Sierras Hidraulicas",
            "Vibroapisonadores",
            "Amoladora",
        ]

        self.requestData = { 
            'elements' : [], 
        }

        #time.sleep(5)

    def link_to_new_request(self, linkTo):
        driver = self.driver
        
        # Espera hasta que el link esté presente
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Ingreso Elementos')))
        link.click()

        # Espera hasta que el link esté presente y hace un "mouseover sobre el link"
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Nueva Solicitud')))
        mouse = ActionChains(driver)
        mouse.move_to_element(link)
        mouse.perform()


        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, linkTo)))
        link.click()

    def fill_data_request(self):
        driver = self.driver
        self.requestData['requestType'] = "Orden de Salida"

        # Selecciona una planta aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#plantaId-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        #select.select_by_visible_text(self.plantName)
        isZonaFranca = random.randrange(0,2) # Random entre 0 y 1 para definir si es zona franca
        #isZonaFranca = 1
        if(isZonaFranca == 1):
            select.select_by_visible_text(self.zonaFrancaPlant)
            self.requestData["isZonaFranca"] = True
            self.requestData['plant'] = self.zonaFrancaPlant
        else:
            select.select_by_visible_text(self.plantName)
            self.requestData['plant'] = self.plantName
            self.requestData["isZonaFranca"] = False


        # Selecciona una categoría de elemento
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#elementCategory-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_index(randomIndex)
        self.requestData['elementCategory'] = select.first_selected_option.text

        # Selecciona un interventor
        dataListInput = WebDriverWait(driver, 10).until(selector_got_options((By.CSS_SELECTOR, 'select#interventor-combobox'), 1))
        select = Select(dataListInput)
        select.select_by_visible_text(self.interventorName)
        self.requestData['interventor'] = select.first_selected_option.text.strip()

        #Ingresa un destino
        destinyInput = driver.find_element_by_css_selector('input#destination-form')
        destinyInput.clear()
        destinyInput.send_keys('Destino de prueba')
        self.requestData['destiny'] = 'Destino de prueba'

        #Ingresa el documento de un responsable
        destinyInput = driver.find_element_by_css_selector('input#responsable-form')
        destinyInput.clear()
        destinyInput.send_keys('40021346')
        self.requestData['responsable'] = '40021346'

        # Selecciona un motivo de salida aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#activity-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_index(randomIndex)
        self.requestData['departureReasson'] = select.first_selected_option.text

        returnCheckbox = driver.find_element_by_css_selector('input#returnDate-checkbox')
        returnCheckbox.click()
        returnInput = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#returnDate-form')))
        returnInput.clear()
        #returnInput.send_keys('28/12/2018')
        self.utilities.selectDate(driver, returnInput, "28")
        self.requestData['returnDate'] = '28/01/2019'

        # Clic en el botón continuar
        continueButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.btn-success')))
        continueButton.click()

    def fill_element_data(self):
        driver = self.driver

        elementDescription = self.herramientas[random.randrange(0,len(self.herramientas) - 1)]

        if not any(d['description'] == elementDescription for d in self.requestData['elements']): # Para no ingresar elementos repetidos
            descriptionInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea#form_element-description')))
            descriptionInput.clear()
            descriptionInput.send_keys(elementDescription)

            # La cantidad es un número aleatorio
            amount = random.randrange(1,10)
            amountInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#form_element-amount')))
            amountInput.clear()
            amountInput.send_keys(amount)

            # Si la cantidad de elementos es mayor a 1, se pone N/A como serial, si no un serial aleatorio
            serial = "N/A"
            if(amount == 1):
                serial = randomword(10)
            serialInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#form_element-serial')))
            serialInput.clear()
            serialInput.send_keys(serial)        

            # Clic en el botón continuar
            addElementButton = driver.find_element_by_css_selector("form#elment-form").find_element_by_css_selector("input.btn-primary")
            addElementButton.click()

            self.requestData['elements'].append({
                'description' : elementDescription,
                'amount' : amount,
                'serial' : serial,
                'status' : 'en Espera Aprobación'
                })

    def create_order_request(self):
        driver = self.driver

        self.utilities.login(self.driver, self.base_url, self.username, self.password)
        self.link_to_new_request('Orden de Salida')
        self.fill_data_request()

        elementAmount = random.randrange(1,30)
        elementAmount = 1

        for i in range(elementAmount):
            self.fill_element_data()
            WebDriverWait(driver, 10).until(EC.element_located_selection_state_to_be((By.CSS_SELECTOR, 'table#myTable'), False))


        sendRequestButton = driver.find_element(By.XPATH, '//button[text()="Enviar Solicitud"]')
        mouse = ActionChains(driver)
        mouse.move_to_element(sendRequestButton).click()
        mouse.perform()

        modalWindow = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#approveConfirmation-modal')))
        acceptButton = WebDriverWait(modalWindow, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn-success')))
        acceptButton.click()

        # Busca el consecutivo en el titulo
        titles = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'blockquote'))).find_elements_by_css_selector("H4")
        consecutive = titles[0].find_element_by_css_selector('strong')
        consecutive = consecutive.get_attribute('innerHTML')

        self.requestData['requestId'] = consecutive.strip()

        self.assert_request()

        driver.quit();
        print("Orden de Salida creada con consecutivo " + consecutive + ", y " + str(len(self.requestData['elements'])) + " elementos")

        return self.requestData

    def assert_request(self):
        driver = self.driver

        # Busca los datos de la solicitud y hace las comparaciones correspondientes
        plantdd = driver.find_element_by_xpath('//dl[dt/label[contains(text(),"Pla")]]/dd').get_attribute('innerHTML').strip()
        destinydd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Destino")]]/dd').get_attribute('innerHTML').strip()
        departureReassondd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Motivo de Salida")]]/dd').get_attribute('innerHTML').strip()
        returnDatedd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Fecha de Retorno")]]/dd').get_attribute('innerHTML').strip()
        responsabledd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Responsable")]]/dd').get_attribute('innerHTML').strip()

        assert plantdd == self.requestData['plant']
        assert destinydd == self.requestData['destiny']
        assert self.requestData['departureReasson'] == departureReassondd
        assert self.requestData['responsable'] == responsabledd 
        assert self.requestData['returnDate'] == returnDatedd
        #self.requestData['interventor'] = select.first_selected_option.text
        print("Comparados datos de solicitud...")

        # Hace las comparaciones con los elementos resultantes y los elementos guardados al momento de crear la solicitud
        self.assert_elements()

    def assert_elements(self, checkedElementsAmount = 0):
        driver = self.driver
        elements = self.requestData['elements']

        # Busca los elementos en la tabla de la solicitud creada
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#element-table")))
        webElements = table.find_elements_by_css_selector('tbody tr')

        for webElement in webElements:
            # Busca los datos de cada elemento en la fila
            webElementCells = webElement.find_elements_by_css_selector('td')
            webElementDescription = webElementCells[0].get_attribute('innerHTML').strip()
            webElementCategory = webElementCells[1].get_attribute('innerHTML').strip()
            webElementAmount = webElementCells[2].get_attribute('innerHTML').strip()
            webElementSerial = webElementCells[3].get_attribute('innerHTML').strip()
            webElementStatus = webElementCells[5].get_attribute('innerHTML').strip()

            # Hace las respectivas comparaciones por elemento
            for element in elements:
                if element['description'] == webElementDescription:
                    assert self.requestData['elementCategory'] == webElementCategory
                    assert element['amount'] == int(float(webElementAmount.replace(',', '.')))
                    assert element['serial'] == webElementSerial
                    assert element['status'] in webElementStatus

                    checkedElementsAmount += 1 # Para revisar la siguiente página de la tabla y llevar el registro de lo revisado
                    break

        # Busca el botón para la siguiente pagina
        nextPageButton = driver.find_element_by_css_selector("a#element-table_next")
        if self.utilities.has_class(nextPageButton, 'disabled') == False: # Se puede presionar
            nextPageButton.click()
            self.assert_elements(checkedElementsAmount)
        else: # Ya no hay más paginas disponibles
            assert checkedElementsAmount == len(elements) # Compara la cantidad de elementos en la tabla con los guardados
            print("Comparados datos de elementos...")

class TransferRequest(unittest.TestCase):

    def __init__(self, base_url, browser):    
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
        
        self.username = "primerusuarioargos@argos.com.co"
        self.password = "Ingresos1*"

        self.plantName = "CANTERA EL TRIUNFO"
        self.zonaFrancaPlant = "PLANTA CEMENTOS CARTAGENA ZFA"
        self.destinYPlantName = "ALMAGRAN"

        self.interventorName = 'Andrés Mauricio Gómez'

        self.herramientas = [
            "Allanadoras",
            "Cortadoras de Pavimento",
            "Placas Compactadoras",
            "Mezcladoras",
            "Rotomartillo",
            "Carretillas y Ruedas",
            "Carga y Levante",
            "Bombas Hidraulicas",
            "Compactadoras Hidraulicas",
            "Esmeriladores Hidraulicos",
            "Fuentes de Poder Hidraulico",
            "Malacates",
            "Mototaladros",
            "Sierras Hidraulicas",
            "Vibroapisonadores",
            "Amoladora",
        ]

        self.requestData = { 
            'elements' : [], 
        }

        #time.sleep(5)

    def link_to_new_request(self, linkTo):
        driver = self.driver
        
        # Espera hasta que el link esté presente
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Ingreso Elementos')))
        link.click()

        # Espera hasta que el link esté presente y hace un "mouseover sobre el link"
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Nueva Solicitud')))
        mouse = ActionChains(driver)
        mouse.move_to_element(link)
        mouse.perform()


        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, linkTo)))
        link.click()

    def fill_data_request(self):
        driver = self.driver
        self.requestData['requestType'] = "Solicitud de Traslado"

        # Selecciona una planta aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#plantaId-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        isZonaFranca = random.randrange(0,2) # Random entre 0 y 1 para definir si es zona franca
        isZonaFranca = 1
        if(isZonaFranca == 1):
            select.select_by_visible_text(self.zonaFrancaPlant)
            self.requestData["isZonaFranca"] = True
            self.requestData['plant'] = self.zonaFrancaPlant
        else:
            select.select_by_visible_text(self.plantName)
            self.requestData['plant'] = self.plantName
            self.requestData["isZonaFranca"] = False


        # Selecciona una categoría de elemento
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#elementCategory-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_index(randomIndex)
        self.requestData['elementCategory'] = select.first_selected_option.text

        # Seleccione una planta destino
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#destinationPlantaId-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_visible_text(self.destinYPlantName)
        self.requestData['destinyPlant'] = select.first_selected_option.text

        # Selecciona un motivo de salida aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#activity-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_index(randomIndex)
        self.requestData['departureReasson'] = select.first_selected_option.text

        # Selecciona un interventor
        dataListInput = WebDriverWait(driver, 10).until(selector_got_options((By.CSS_SELECTOR, 'select#interventor-combobox'), 1))
        select = Select(dataListInput)
        select.select_by_visible_text(self.interventorName)
        self.requestData['interventor'] = select.first_selected_option.text.strip()

        #Ingresa un destino
        destinyInput = driver.find_element_by_css_selector('input#destination-form')
        destinyInput.clear()
        destinyInput.send_keys('Destino de prueba')
        self.requestData['destiny'] = 'Destino de prueba'

        #Ingresa un responsable
        destinyInput = driver.find_element_by_xpath('//div[label[contains(text(), "CC. Responsable")]]//input')
        destinyInput.clear()
        destinyInput.send_keys('72984843')
        self.requestData['responsable'] = '72984843'

        # Clic en el botón continuar
        continueButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.btn-success')))
        continueButton.click()

    def fill_element_data(self):
        driver = self.driver

        elementDescription = self.herramientas[random.randrange(0,len(self.herramientas) - 1)]

        if not any(d['description'] == elementDescription for d in self.requestData['elements']): # Para no ingresar elementos repetidos

            descriptionInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea#form_element-description')))
            descriptionInput.clear()
            descriptionInput.send_keys(elementDescription)

            # La cantidad es un número aleatorio
            amount = random.randrange(1,10)
            amountInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#form_element-amount')))
            amountInput.clear()
            amountInput.send_keys(amount)

            # Si la cantidad de elementos es mayor a 1, se pone N/A como serial, si no un serial aleatorio
            serial = "N/A"
            if(amount == 1):
                serial = randomword(10)
            serialInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#form_element-serial')))
            serialInput.clear()
            serialInput.send_keys(serial)        

            # Clic en el botón continuar
            addElementButton = driver.find_element_by_css_selector("form#elment-form").find_element_by_css_selector("input.btn-primary")
            addElementButton.click()

            self.requestData['elements'].append({
                'description' : elementDescription,
                'amount' : amount,
                'serial' : serial,
                'status' : 'en Espera Aprobación'
                })

    def create_transfer_request(self):
        driver = self.driver

        self.utilities.login(self.driver, self.base_url, self.username, self.password)
        self.link_to_new_request('Solicitud de Traslado')
        self.fill_data_request()

        elementAmount = random.randrange(1,30)
        elementAmount = 30

        for i in range(elementAmount):
            self.fill_element_data()
            WebDriverWait(driver, 10).until(EC.element_located_selection_state_to_be((By.CSS_SELECTOR, 'table#myTable'), False))


        sendRequestButton = driver.find_element(By.XPATH, '//button[text()="Enviar Solicitud"]')
        mouse = ActionChains(driver)
        mouse.move_to_element(sendRequestButton).click()
        mouse.perform()

        modalWindow = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#approveConfirmation-modal')))
        acceptButton = WebDriverWait(modalWindow, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn-success')))
        acceptButton.click()

        # Busca el consecutivo en el titulo
        titles = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'blockquote'))).find_elements_by_css_selector("H4")
        consecutive = titles[0].find_element_by_css_selector('strong')
        consecutive = consecutive.get_attribute('innerHTML')

        self.requestData['requestId'] = consecutive.strip()

        driver.quit();
        print("Solicitud de Traslado creada con consecutivo " + consecutive + ", y " + str(len(self.requestData['elements'])) + " elementos")

        return self.requestData
    


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))
