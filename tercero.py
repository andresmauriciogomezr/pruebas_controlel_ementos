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

class IngressRequest(unittest.TestCase):

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
        
        self.username = "saludocupacional@agrepuestos.com"
        self.password = "saludocupacional@agrepuestos.com"

        self.plantName = "CANTERA EL TRIUNFO"

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
            "Picos",
            "Mazos",
            "Cuñas",
            "Paletas",
            "Alicates",
            "Desatornilladores",
            "Plomada",
            "Sierras",
        ]

        self.equipo = [
            "Bailejo",
            "Barra",
            "Canastilla",
            "Champeadora",
            "Cizalla",
            "Espátula",
            "Paleta",
            "Perro",
            "Parihuela",
            "Plomada",
            "Taladro",
        ]

        self.consumibles = [
            "Arena",
            "Cemento",
            "Gravilla",
            "Cable Coaxial",
            "Cable de Red",
            "ACPM",
            "Varilla",
            "Perro",
            "Cable Electrico",
        ]

        self.requestData = { 
            'elements' : [], 
            'consumables' : [] 
        }

        #time.sleep(5)

        print("********************* Tercero ************************************")

    def link_to_new_request(self, linkTo):
        driver = self.driver
        
        # Espera hasta que el link esté presente
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Ingreso Elementos')))
        driver.find_element_by_link_text("Ingreso Elementos").click()

        # Espera hasta que el link esté presente y hace un "mouseover sobre el link"
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Nueva Solicitud')))
        mouse = ActionChains(driver)
        mouse.move_to_element(link)
        mouse.perform()

        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, linkTo)))
        link.click()

    def fill_data_request(self):
        driver = self.driver

        # Hace foco en el input para el trabajador
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#trabajadorInput')))
        dataListInput.click()

        # Consigue las opciones presentes en el dataList
        dataList = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TrabajadorId')))
        options = dataList.find_elements_by_tag_name('option')

        # selectiona aleatoriamente una de la opciones y consigue el texto
        randomIndex = random.randrange(1,len(options))
        optionText = options[randomIndex].get_attribute("value")

        # Ingresa el texto en el input para seleccionar el trabajador
        dataListInput.clear()
        dataListInput.send_keys(optionText)
        self.requestData['trabajador'] = optionText

        # Selecciona una planta aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#plantaId-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_visible_text(self.plantName)
        self.requestData['plant'] = self.plantName

        # Selecciona un motivo de ingreso aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#ingressReason-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_index(randomIndex)
        self.requestData['ingressReasson'] = select.first_selected_option.text

        # Clic en el botón continuar
        continueButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.btn-success')))
        continueButton.click()

    def fill_data_consumables_request(self):
        driver = self.driver

        # Hace foco en el input para el trabajador
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#trabajadorInput')))
        dataListInput.click()

        # Consigue las opciones presentes en el dataList
        dataList = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TrabajadorId')))
        options = dataList.find_elements_by_tag_name('option')

        # selectiona aleatoriamente una de la opciones y consigue el texto
        randomIndex = random.randrange(1,len(options))
        optionText = options[randomIndex].get_attribute("value")

        # Ingresa el texto en el input para seleccionar el trabajador
        dataListInput.clear()
        dataListInput.send_keys(optionText)

        # Selecciona una planta aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#plantaId-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_visible_text(self.plantName)

        # Digita un motivo de Ingreso
        ingressReasonInput = driver.find_element_by_css_selector('textarea[name="OpenIngressReason"]')
        ingressReasonInput.clear()
        ingressReasonInput.send_keys("Motivo de ingreso de prueba para Enrada de consumibles")

        # Clic en el botón continuar
        continueButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.btn-success')))
        continueButton.click()

    def fill_element_data(self):
        driver = self.driver

        # Selecciona un tipo de elemento aleatoriamente
        select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#form_element-type')))
        select = Select(select)
        elementTypeIndex = random.randrange(1,len(select.options))
        
        elementTypeIndex = 2

        # De acuerdo al tipo de elemento se selecciona un elemento de la lista
        if elementTypeIndex == 2:
            elementDescription = self.herramientas[random.randrange(0,len(self.herramientas) - 1)]
        else:
            elementDescription = self.equipo[random.randrange(0,len(self.equipo) - 1)]
        

        #if elementDescription not in self.requestData['elements']: # Para no ingresar elementos repetidos
        if not any(d['description'] == elementDescription for d in self.requestData['elements']):
            select.select_by_index(elementTypeIndex)

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

            price = random.randrange(10000,100000)
            priceInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#form_element-price')))
            priceInput.clear()
            priceInput.send_keys(price)


            self.requestData['elements'].append({
                'description' : elementDescription,
                'amount' : amount,
                'serial' : serial,
                'price' : price,
                'status' : 'Por Ingresar'
                })

            # Clic en el botón continuar
            addElementButton = driver.find_element_by_css_selector("form#elment-form").find_element_by_css_selector("input.btn-primary")
            addElementButton.click()

    def fill_consumables_data(self):
        driver = self.driver

        consumableDescription = self.consumibles[random.randrange(0,len(self.consumibles) - 1)]
        if consumableDescription not in self.requestData['consumables']: # Para no ingresar consumibles repetidos

            self.requestData['consumables'].append(consumableDescription)# Lo agrega a la lista de información de la solicitud

            descriptionInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea#form_element-description')))
            descriptionInput.clear()
            descriptionInput.send_keys(consumableDescription)

            # La cantidad es un número aleatorio
            amount = random.randrange(1,100)
            amountInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#form_element-amount')))
            amountInput.clear()
            amountInput.send_keys(amount)

            # Selecciona aleatoriamente una unidad de medida
            select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#form_MeasurementUnit')))
            select = Select(select)
            index = random.randrange(1,len(select.options))
            select.select_by_index(index)


            # Clic en el botón continuar
            addElementButton = driver.find_element_by_css_selector("form#elment-form").find_element_by_css_selector("input.btn-primary")
            addElementButton.click()

    def create_element_ingress_request(self):
        driver = self.driver

        self.utilities.login(self.driver, self.base_url, self.username, self.password)
        self.link_to_new_request('Entrada de Elementos')
        self.fill_data_request()


        elementAmount = random.randrange(1,30)
        #elementAmount = 1

        for i in range(elementAmount):
            self.fill_element_data()
            WebDriverWait(driver, 10).until(EC.element_located_selection_state_to_be((By.CSS_SELECTOR, 'table#myTable'), False))

        sendRequestButton = driver.find_element_by_css_selector("a#saveRequest-button")
        mouse = ActionChains(driver)
        mouse.move_to_element(sendRequestButton).click()
        mouse.perform()

        # Busca el consecutivo en el titulo
        titles = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'blockquote'))).find_elements_by_css_selector("H4")
        consecutive = titles[0].find_element_by_css_selector('strong')
        consecutive = consecutive.get_attribute('innerHTML')
        self.requestData['requestId'] = consecutive

        # Hace las comparaciones respectivas de la solicitud creada
        self.assert_request()
        
        print("Solicitud "+str(consecutive)+" Creada con " +str(len(self.requestData['elements']))+ " elementos")

        driver.quit();
        return self.requestData

    def assert_request(self):
        driver = self.driver

        # Busca los datos de la solicitud y hace las comparaciones correspondientes
        plantdd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Planta")]]/dd').get_attribute('innerHTML').strip()
        ingressReassondd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Motivo de ingreso")]]/dd').get_attribute('innerHTML').strip()
        responsabledd = driver.find_element_by_xpath('//dl[dt[contains(text(),"Responsable")]]/dd').get_attribute('innerHTML').strip()

        assert plantdd == self.requestData['plant']
        assert ingressReassondd == self.requestData['ingressReasson']
        assert self.requestData['trabajador'] in responsabledd
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
            webElementDescription = webElementCells[1].get_attribute('innerHTML').strip()
            webElementSerial = webElementCells[3].get_attribute('innerHTML').strip()
            webElementAmount = webElementCells[4].get_attribute('innerHTML').strip()
            webElementPrice = webElementCells[5].get_attribute('innerHTML').strip()
            webElementStatus = webElementCells[7].get_attribute('innerHTML').strip()

            # Hace las respectivas comparaciones por elemento
            for element in elements:
                if element['description'] == webElementDescription:
                    assert element['serial'] == webElementSerial
                    #assert element['amount'] == webElementAmount
                    assert str(element['price']) == webElementPrice
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



    def create_consumables_ingress_request(self):
        driver = self.driver

        self.utilities.login(self.driver, self.base_url, self.username, self.password)
        self.link_to_new_request('Entrada de Consumibles')
        self.fill_data_consumables_request()

        consumablesAmount = random.randrange(1,10)
        #consumablesAmount = 1

        for i in range(consumablesAmount):
            self.fill_consumables_data()
            WebDriverWait(driver, 10).until(EC.element_located_selection_state_to_be((By.CSS_SELECTOR, 'table#myTable'), False))

        # Envía la solicitud
        sendRequestButton = driver.find_element_by_link_text("Enviar Solicitud")
        mouse = ActionChains(driver)
        mouse.move_to_element(sendRequestButton).click()
        mouse.perform()

        # Busca el consecutivo en el titulo
        titles = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'blockquote'))).find_elements_by_css_selector("H4")
        consecutive = titles[0].find_element_by_css_selector('strong')
        consecutive = consecutive.get_attribute('innerHTML').strip()

        self.requestData['requestId'] = consecutive

        driver.quit();
        return self.requestData

class DepartureRequest(unittest.TestCase):

    def __init__(self, base_url, browser, ingressRequestData):    
        
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
        
        self.username = "saludocupacional@agrepuestos.com"
        self.password = "saludocupacional@agrepuestos.com"
        self.interventorName = 'Andrés Mauricio Gómez'

        self.requestId = ingressRequestData['requestId']
        self.requestData = ingressRequestData

        print("********************* Tercero ************************************")

    def link_to_new_request(self, linkTo):
        driver = self.driver
        
        # Espera hasta que el link esté presente
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Ingreso Elementos')))
        driver.find_element_by_link_text("Ingreso Elementos").click()

        # Espera hasta que el link esté presente y hace un "mouseover sobre el link"
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Nueva Solicitud')))
        mouse = ActionChains(driver)
        mouse.move_to_element(link)
        mouse.perform()

        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, linkTo)))
        link.click()

    def find_ingress_request(self):
        driver = self.driver
        requestId = self.requestId

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
            requestButton = WebDriverWait(requestRow, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn-success')))
            requestButton.click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Generar Salida'))).click()
        else:
            driver.find_element_by_css_selector('a#request_table_next').click()
            self.find_ingress_request()

    def select_all_elements(self, newAmount = 10000):
        driver = self.driver

        # Selecciona un tipo de elemento aleatoriamente
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table#intvory-table')))
        elements  = table.find_elements_by_css_selector('tbody tr')
        
        for row in elements:
            amountInput = row.find_element_by_css_selector('input.newAmount')
            amount = amountInput.get_attribute('value')

            if newAmount != 10000:
                newAmount = str(round( (int(amount)/2)+1 )) # la Mitad redondeada a 1
    
            amountInput.clear()
            amountInput.send_keys(newAmount)

            checkbox = row.find_element_by_css_selector('input[type="checkbox"]')
            checkbox.click()

        driver.find_element_by_css_selector('button#addElementsButton').click() 

    def select_some_elements(self, relatedElements = []):
        driver = self.driver

        # Selecciona un tipo de elemento aleatoriamente
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table#intvory-table')))
        elements  = table.find_elements_by_css_selector('tbody tr')
        
        for row in elements:
            amountInput = row.find_element_by_css_selector('input.newAmount')
            amount = amountInput.get_attribute('value')
            description = row.find_elements_by_css_selector('td')[2].get_attribute('innerHTML').strip()

            # Saca aleatoríamente un porcentaje de la cantidad entre 10 y 100 para obtener una cantidad a salir
            newAmountPercent = random.randrange(10, 100, 10) / 100
            newAmount = round( (int(int(amount) * newAmountPercent)))
            if newAmount < 1: # Minimo uno
                newAmount = 1
            newAmount = str(newAmount)
    
            amountInput.clear()
            amountInput.send_keys(newAmount)

            checkbox = row.find_element_by_css_selector('input[type="checkbox"]')
            checkbox.click()

            # Agrega el elemento confirmado
            relatedElements.append(next(item for item in self.requestData['elements'] if item["description"] == description))

        nextPageButton = driver.find_element_by_css_selector('a#intvory-table_next')
        if self.utilities.has_class(nextPageButton, 'disabled') == False: # Se puede presionar
            nextPageButton.click()
            return self.select_all_elements(relatedElements)

        else:
            driver.find_element_by_css_selector('button#addElementsButton').click()
            return relatedElements
    
    def create_element_departure_request(self):
        driver = self.driver

        self.utilities.login(self.driver, self.base_url, self.username, self.password)
        self.link_to_new_request('Salida de Elementos')
        self.find_ingress_request()

        self.assert_request() # Verifica que los elementos y las cantidades coincidan con lo aprobado pro el guarda al entrar
        
        #self.select_all_elements()
        relatedElements = self.select_some_elements()

        driver.find_element(By.CSS_SELECTOR, 'div.submit-request-button').find_element_by_css_selector('input').click()
        print("Solicitud " +str(self.requestData['requestId'])+ " creada con "+ str(len(relatedElements)))

        self.requestData['ElementsIngressed'] = self.requestData['elements']
        self.requestData['elements'] = relatedElements
        driver.quit();
        
        return self.requestData

    def modify_element_departure_request(self):
        driver = self.driver

        self.utilities.login(self.driver, self.base_url, self.username, self.password)
        self.link_to_pending_requests()

        # Encuentra la fila de la tabla que corresponde a la solicitud buscada, hace clic en el botón "Detalles"
        requestRow = self.utilities.find_request(driver, 'table#request_table', self.requestId, 'a#request_table_next', 0)
        requestButton = WebDriverWait(requestRow, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn-success')))
        requestButton.click()

        # Presiona el botón modificar
        modifyButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Modificar')))
        modifyButton.click()

        self.remove_elements()
        self.select_all_elements()

        driver.find_element(By.CSS_SELECTOR, 'div.submit-request-button').find_element_by_css_selector('input').click()

        driver.quit();

    def remove_elements(self):
        driver = self.driver

        # Selecciona un tipo de elemento aleatoriamente
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table#elements-table')))
        elements  = table.find_elements_by_css_selector('tbody tr')
        
        for row in elements:
            removeElementButton = row.find_element_by_css_selector('button.btn-danger')
            removeElementButton.click()

    def link_to_pending_requests(self):
        driver = self.driver
        
        # Espera hasta que el link esté presente
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Ingreso Elementos')))
        link.click()

        # Espera hasta que el link esté presente y hace un "mouseover sobre el link"
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Ver Solicitudes')))
        mouse = ActionChains(driver)
        mouse.move_to_element(link)
        mouse.perform()

        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Solicitudes Pendientes")))
        link.click()

    def fill_data_request(self):
        driver = self.driver

        # Hace foco en el input para el trabajador
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#trabajadorInput')))
        dataListInput.clear()
        dataListInput.click()

        # Consigue las opciones presentes en el dataList
        dataList = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TrabajadorId')))
        options = dataList.find_elements_by_tag_name('option')

        # selectiona aleatoriamente una de la opciones y consigue el texto
        randomIndex = random.randrange(1,len(options))
        optionText = options[randomIndex].get_attribute("value")

        # Ingresa el texto en el input para seleccionar el trabajador
        dataListInput.clear()
        dataListInput.send_keys(optionText)

        # Selecciona una planta aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#interventor-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_visible_text(self.interventorName)

    def select_all_consumables(self):
        driver = self.driver

        # Selecciona un tipo de elemento aleatoriamente
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table#intvory-table')))
        elements  = table.find_elements_by_css_selector('tbody tr')
        
        for row in elements:
            amountInput = row.find_element_by_css_selector('input.newAmount')
            
            # Busca la cantidad maxima permitida en la tercer columna de la tabla
            maxAmount = row.find_elements_by_css_selector('td')[3].find_element_by_css_selector('p')
            maxAmount = maxAmount.get_attribute('innerHTML').split(',')[0]
            maxAmount = maxAmount.strip()

            # ingresa la mitada de la cantidad máxima
            newAmount = str(round( (int(maxAmount)/2)+1 )) # la Mitad redondeada a 1
            amountInput.clear()
            amountInput.send_keys(newAmount)

            checkbox = row.find_element_by_css_selector('input[type="checkbox"]')
            checkbox.click()

        driver.find_element_by_css_selector('button#addElementsButton').click() 

    def create_consumables_departure_request(self):
        driver = self.driver

        self.utilities.login(self.driver, self.base_url, self.username, self.password)
        self.link_to_new_request('Salida de Consumibles')
        self.find_ingress_request()
        self.fill_data_request()
        self.select_all_consumables()

        driver.find_element(By.CSS_SELECTOR, 'div.submit-request-button').find_element_by_css_selector('button').click()

        modalWindow = driver.find_element_by_css_selector('#approveConfirmation-modal')
        modalWindow = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#approveConfirmation-modal')))
        acceptButton = modalWindow.find_element_by_css_selector('button.btn-success').click()

        driver.quit();

    def assert_request(self):
        driver = self.driver

        # Busca los datos de la solicitud y hace las comparaciones correspondientes
        plantdiv = driver.find_element_by_xpath('//div[label[contains(text(),"Planta")]]')
        plant = plantdiv.find_element_by_css_selector('input').get_attribute('value').strip()
        responsable = driver.find_element_by_css_selector('input#trabajadorInput').get_attribute('value').strip()

        assert plant == self.requestData['plant']
        assert self.requestData['trabajador'] in responsable

        print("Comparados datos de solicitud...")

        # Hace las comparaciones con los elementos resultantes y los elementos guardados al momento de crear la solicitud
        self.assert_elements()

    def assert_elements(self, checkedElementsAmount = 0):
        driver = self.driver
        elements = self.requestData['elements']

        # Busca los elementos en la tabla de la solicitud creada
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#intvory-table")))
        webElements = table.find_elements_by_css_selector('tbody tr')

        for webElement in webElements:
            # Busca los datos de cada elemento en la fila
            webElementCells = webElement.find_elements_by_css_selector('td')
            webElementDescription = webElementCells[2].get_attribute('innerHTML').strip()
            webElementMaxAmount = webElementCells[3].text.strip().split('-')[0]
            webElementAmount = webElementCells[4].find_element_by_css_selector('input').get_attribute('value')

            # Hace las respectivas comparaciones por elemento
            for element in elements:
                if element['description'] == webElementDescription:
                    assert int(webElementMaxAmount) == element['amount']
                    assert int(webElementAmount) == element['amount']
                    checkedElementsAmount += 1 # Para revisar la siguiente página de la tabla y llevar el registro de lo revisado
                    break

        # Busca el botón para la siguiente pagina
        nextPageButton = driver.find_element_by_css_selector("a#intvory-table_next")
        if self.utilities.has_class(nextPageButton, 'disabled') == False: # Se puede presionar
            nextPageButton.click()
            self.assert_elements(checkedElementsAmount)
        else: # Ya no hay más paginas disponibles
            self.utilities.return_table_to_firstpage(driver, "intvory-table")
            assert checkedElementsAmount == len(elements) # Compara la cantidad de elementos en la tabla con los guardados
            print("Comparados datos de elementos...")

class ArgosDepartureRequest(unittest.TestCase):

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
        
        self.username = "pruebagomez@fortoxsa.com"
        self.password = "Ingresos1*"

        self.plantName = "CANTERA EL TRIUNFO"
        self.zonaFrancaPlant = "PLANTA CEMENTOS CARTAGENA ZFA"

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

        print("********************* Tercero ************************************")
        #time.sleep(5)

    def link_to_new_request(self, linkTo):
        driver = self.driver
        
        # Espera hasta que el link esté presente
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Ingreso Elementos')))
        driver.find_element_by_link_text("Ingreso Elementos").click()

        # Espera hasta que el link esté presente y hace un "mouseover sobre el link"
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Nueva Solicitud')))
        mouse = ActionChains(driver)
        mouse.move_to_element(link)
        mouse.perform()

        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, linkTo)))
        link.click()

    def fill_data_request(self):
        driver = self.driver
        self.requestData['requestType'] = "Salida Activos de Argos"

        # Hace foco en el input para el trabajador
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#trabajadorInput')))
        dataListInput.click()

        # Consigue las opciones presentes en el dataList
        dataList = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TrabajadorId')))
        options = dataList.find_elements_by_tag_name('option')

        # selectiona aleatoriamente una de la opciones y consigue el texto
        randomIndex = random.randrange(1,len(options))
        optionText = options[randomIndex].get_attribute("value")
        self.requestData['responsable'] = optionText

        # Ingresa el texto en el input para seleccionar el trabajador
        dataListInput.clear()
        dataListInput.send_keys(optionText)

        # Selecciona un motivo de salida aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#activity-form')))
        select = Select(dataListInput)
        randomIndex = random.randrange(1,len(select.options))
        select.select_by_index(randomIndex)
        self.requestData['departureReasson'] = select.first_selected_option.text

        #Ingresa un destino
        destinyInput = driver.find_element_by_css_selector('input#destination-form')
        destinyInput.clear()
        destinyInput.send_keys('Destino de prueba')
        self.requestData['destiny'] = 'Destino de prueba'

        # Selecciona una planta aleatoriamente
        dataListInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#plantaId-form')))
        select = Select(dataListInput)
        isZonaFranca = random.randrange(0,2) # Random entre 0 y 1 para definir si es zona franca
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

        # Selecciona una categoría de elemento
        dataListInput = WebDriverWait(driver, 10).until(selector_got_options((By.CSS_SELECTOR, 'select#interventor-combobox'), 1))
        select = Select(dataListInput)
        select.select_by_visible_text(self.interventorName)
        self.requestData['interventor'] = self.interventorName

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

    def create_departure_request(self):
        driver = self.driver

        self.utilities.login(self.driver, self.base_url, self.username, self.password)
        self.link_to_new_request('Salida de Activos Argos')
        self.fill_data_request()

        elementAmount = random.randrange(1,30)
        #elementAmount = 1

        for i in range(elementAmount):
            self.fill_element_data()
            WebDriverWait(driver, 10).until(EC.element_located_selection_state_to_be((By.CSS_SELECTOR, 'table#myTable'), False))


        sendRequestButton = driver.find_element(By.XPATH, '//button[text()="Enviar Solicitud"]')
        self.utilities.scrollToElement(driver, sendRequestButton)
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

        print("Solicitud " + consecutive +" creada con " + str(len(self.requestData["elements"])) + " elementos")

        driver.quit();

        return self.requestData

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))



