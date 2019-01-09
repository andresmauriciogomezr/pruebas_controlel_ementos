import unittest, time, re
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
import pprint



class Utilities(unittest.TestCase):


    def login(self, driver, base_url, username, password):
        #driver = self.driver
        driver.get(base_url)

        # Espera hasta que se muestre el botón Terceros
        TercerosButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnUserTercero')))
        TercerosButton.click()

        emailInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//section[@id="loginFormTercero"]/form//input[@id="Email"]')))
        emailInput.clear()
        emailInput.send_keys(username)
        
        passwordInput = driver.find_element_by_xpath('//section[@id="loginFormTercero"]/form//input[@id="Password"]')
        passwordInput.clear()
        passwordInput.send_keys(password)
        
        # El Botón de inicio de sesión
        driver.find_element_by_xpath('//section[@id="loginFormTercero"]/form//input[@type="submit"]').click()

    def localLogin(self, driver, base_url, username, password):
        #driver = self.driver
        driver.get(base_url)

        # Espera hasta que se muestre el botón Terceros
        TercerosButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'btnUserTercero')))
        TercerosButton.click()

        emailInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id="Email"]')))
        emailInput.clear()
        emailInput.send_keys(username)
        
        passwordInput = driver.find_element_by_xpath('//input[@id="Password"]')
        passwordInput.clear()
        passwordInput.send_keys(password)
        
        # El Botón de inicio de sesión
        driver.find_element_by_xpath('//input[@type="submit"]').click()

    def find_request(self, driver, tableCssSelector, requestId, nextButtonCssSelector, columnToSearch):
        driver = driver
        requestId = requestId

        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, tableCssSelector)))
        elements  = table.find_elements_by_css_selector('tbody tr')

        # Busca en la primer columna de cada fila el consecutivo de la solicitud a gestionar
        requestRow = None
        for row in elements:
            # Busca la columna en que está el consecutivo, extrae el consecutivo y lo limpia para comparar
            idCell = row.find_elements_by_css_selector('th')[columnToSearch]
            consecutive = idCell.get_attribute('innerHTML').strip()

            if consecutive == requestId: # Encuentra la solicitud
                requestRow = row
                break
        
        if requestRow is not None:
            return requestRow
        else:
            nextPageButton = driver.find_element_by_css_selector(nextButtonCssSelector)
            nextPageButton.click()
            return self.find_request(driver, tableCssSelector, requestId, nextButtonCssSelector, columnToSearch)

    def selectDate(self, driver, inputElement, dayToSelect, td = None):
        # Hace el scroll para enfocar el elemento al fondo de la página
        # Clic en el input
        driver.execute_script("arguments[0].scrollIntoView(0);", inputElement)
        inputElement.click()
        
        # Espera a que esté visible el selector
        divDateSelector = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR , '.bootstrap-datetimepicker-widget')))
        
        # Selecciona una fecha según el número visíble
        dateTable = WebDriverWait(divDateSelector, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        driver.execute_script("arguments[0].focus();", dateTable)

        #dateTable = divDateSelector.find_element_by_tag_name("table")
        options = WebDriverWait(dateTable, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "tbody")))
        #driver.execute_script("arguments[0].focus();", options)

        # Forza el foco sobre el selector de fecha 
        mouse = ActionChains(driver)
        mouse.move_to_element(options).perform()

        optionsList = divDateSelector.find_elements_by_css_selector('td')
        for o in optionsList:
            # Si coincide con el número de fecha, y no está desabilitado por ser fecha anterior
            if o.get_attribute('innerHTML') == dayToSelect and "disabled" not in o.get_attribute("class"):
                o.click()
                break

    def scrollToElement(self, driver, element):
        driver.execute_script("window.scrollTo("+ str(element.location['x']) + ", "+ str(element.location['y'] -200) +");")
        #driver.execute_script("arguments[0].scrollIntoView();", element)

    def get_rows(self, driver, tableId, rows = []):

        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#"+tableId)))
        rows  += table.find_elements_by_css_selector('tbody tr')

        nextPageButton = driver.find_element_by_css_selector("a#"+tableId+"_next")
        if self.has_class(nextPageButton, 'disabled') == False:
            nextPageButton.click()
            return self.get_rows(driver,tableId, rows)
        else:
            return rows

    def has_class(self, element, className):
        return className in element.get_attribute("class")

    def return_table_to_firstpage(self, driver, tableId):
        try:
            previousButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a#"+tableId+"_previous")))
            if self.has_class(previousButton, 'disabled') == False: # Se puede presionar
                previousButton.click()
                self.return_table_to_firstpage(driver, tableId)
        except:
            a = 1


