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
        
        self.utilities = utilities.Utilities()
        self.base_url = base_url
        #self.browser = browser

        if browser == 'crhome' :
            self.driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
        elif browser == 'firefox' :
            self.driver = webdriver.Firefox()
        else :
            self.driver = webdriver.Ie('C:\IEDriverServer\IEDriverServer.exe')
        
        self.username = "usuarioargos@argos.com.co"
        self.password = "usuarioargos@argos.com.co"

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
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Nueva Solicitud')))
        link.click()

        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, linkTo)))
        link.click()

    def fill_data_request(self):
        driver = self.driver

        # Selecciona una planta aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#plantaId-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_visible_text(self.plantName)

        # Selecciona una categoría de elemento
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#elementCategory-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_index(randomIndex)

        # Selecciona un interventor
        dataListInput = WebDriverWait(driver, 10).until(selector_got_options((By.CSS_SELECTOR, 'select#interventor-combobox'), 1))
        select = Select(dataListInput)
        select.select_by_visible_text(self.interventorName)

        #Ingresa un destino
        destinyInput = driver.find_element_by_css_selector('input#destination-form')
        destinyInput.clear()
        destinyInput.send_keys('Destino de prueba')

        #Ingresa el documento de un responsable
        destinyInput = driver.find_element_by_css_selector('input#responsable-form')
        destinyInput.clear()
        destinyInput.send_keys('40021346')

        # Selecciona un motivo de salida aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#activity-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_index(randomIndex)

        returnCheckbox = driver.find_element_by_css_selector('input#returnDate-checkbox')
        returnCheckbox.click()
        returnInput = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#returnDate-form')))
        returnInput.clear()
        returnInput.send_keys('28/12/2018')
        self.utilities.selectDate(driver, returnInput, "28")

        # Clic en el botón continuar
        continueButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.btn-success')))
        continueButton.click()

    def fill_element_data(self):
        driver = self.driver

        elementDescription = self.herramientas[random.randrange(0,len(self.herramientas) - 1)]

        if elementDescription not in self.requestData['elements']: # Para no ingresar elementos repetidos
            self.requestData['elements'].append(elementDescription)

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

    def create_order_request(self):
        driver = self.driver

        self.utilities.login(self.driver, self.base_url, self.username, self.password)
        self.link_to_new_request('Orden de Salida')
        self.fill_data_request()

        elementAmount = random.randrange(1,30)
        #elementAmount = 1

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

        return self.requestData


class TransferRequest(unittest.TestCase):

    def __init__(self, base_url, browser):    
        
        self.base_url = base_url
        #self.browser = browser

        if browser == 'crhome' :
            self.driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
        elif browser == 'firefox' :
            self.driver = webdriver.Firefox()
        else :
            self.driver = webdriver.Ie('C:\IEDriverServer\IEDriverServer.exe')
        
        self.username = "usuarioargos@argos.com.co"
        self.password = "usuarioargos@argos.com.co"

        self.plantName = "CANTERA EL TRIUNFO"
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

    def link_to_new_request(self, linkTo):
        driver = self.driver
        
        # Espera hasta que el link esté presente
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Nueva Solicitud')))
        link.click()

        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, linkTo)))
        link.click()

    def fill_data_request(self):
        driver = self.driver

        # Selecciona una planta aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#plantaId-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_visible_text(self.plantName)

        # Selecciona una categoría de elemento
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#elementCategory-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_index(randomIndex)

        # Seleccione una planta destino
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#destinationPlantaId-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_visible_text(self.destinYPlantName)

        # Selecciona un motivo de salida aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#activity-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_index(randomIndex)

        # Selecciona un interventor
        dataListInput = WebDriverWait(driver, 10).until(selector_got_options((By.CSS_SELECTOR, 'select#interventor-combobox'), 1))
        select = Select(dataListInput)
        select.select_by_visible_text(self.interventorName)

        #Ingresa un destino
        destinyInput = driver.find_element_by_css_selector('input#destination-form')
        destinyInput.clear()
        destinyInput.send_keys('Destino de prueba')


        """
        returnCheckbox = driver.find_element_by_css_selector('input#returnDate-checkbox')
        returnCheckbox.click()
        returnInput = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#returnDate-form')))
        returnInput.clear()
        returnInput.send_keys('28/12/2018')
        #self.selectDate(driver, returnInput, "28")
        """

        # Clic en el botón continuar
        continueButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.btn-success')))
        continueButton.click()

    def fill_element_data(self):
        driver = self.driver

        elementDescription = self.herramientas[random.randrange(0,len(self.herramientas) - 1)]

        if elementDescription not in self.requestData['elements']: # Para no ingresar elementos repetidos
            self.requestData['elements'].append(elementDescription)

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

    def create_transfer_request(self):
        driver = self.driver

        self.login()
        self.link_to_new_request('Solicitud de Traslado')
        self.fill_data_request()

        elementAmount = random.randrange(1,30)
        #elementAmount = 1

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

        return self.requestData
    


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))



