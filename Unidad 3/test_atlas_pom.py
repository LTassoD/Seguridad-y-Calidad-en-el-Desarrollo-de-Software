# -*- coding: utf-8 -*-
"""
Subunidad 3.3 — Automatización Funcional y Normativa con Selenium WebDriver + Pytest + POM
Sistema evaluado: Plataforma Atlas (http://localhost:3350)
Ejecución en PyCharm:
  - Clic derecho en el archivo -> Run 'pytest in test_atlas_pom.py' (barra verde de pruebas)
  - O desde terminal: python -m pytest -v test_atlas_pom.py
"""
import os
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

BASE_URL = os.getenv("ATLAS_FRONTEND_URL", "http://localhost:3350")


# ==============================================================================
# 1. CAPA DE PAGE OBJECTS (PATRÓN PAGE OBJECT MODEL - GUÍA 3.3.1)
# ==============================================================================

class LoginPage:
    """Page Object para la pantalla de Inicio de Sesión (/login)."""

    INPUT_USUARIO = (By.ID, "nombre_usuario")
    INPUT_PASSWORD = (By.ID, "password")
    BTN_LOGIN = (By.CSS_SELECTOR, '[data-testid="button-login"]')
    TITULO_LOGIN = (By.CSS_SELECTOR, "h2")

    def __init__(self, driver: webdriver.Remote, timeout: int = 12):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def abrir(self):
        self.driver.get(f"{BASE_URL}/login")
        return self

    def obtener_titulo(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.TITULO_LOGIN)).text

    def iniciar_sesion(self, usuario: str, password: str):
        campo_usr = self.wait.until(EC.visibility_of_element_located(self.INPUT_USUARIO))
        campo_usr.clear()
        campo_usr.send_keys(usuario)

        campo_pwd = self.driver.find_element(*self.INPUT_PASSWORD)
        campo_pwd.clear()
        campo_pwd.send_keys(password)

        self.driver.find_element(*self.BTN_LOGIN).click()


class ClientesPage:
    """Page Object para el módulo de Gestión de Clientes (/clientes)."""

    NAV_CLIENTES = (By.CSS_SELECTOR, '[data-testid="link-nav-clientes"]')
    TITULO_MODULO = (By.CSS_SELECTOR, "h5")
    TAB_CREAR = (By.XPATH, "//button[contains(.,'Crear Cliente')]")
    INPUT_RUT = (By.ID, "rut-cliente-create")
    INPUT_NOMBRE = (By.ID, "nombre-cliente-create")
    INPUT_CORREO = (By.ID, "correo-cliente-create")
    INPUT_TELEFONO = (By.ID, "telefono-cliente-create")
    BTN_GUARDAR = (By.ID, "crear-cliente-create")
    ENCABEZADO_TABLA = (By.XPATH, "//h6[contains(.,'Clientes registrados')]")
    BTN_LOGOUT = (By.CSS_SELECTOR, '[data-testid="button-layout-logout"]')

    def __init__(self, driver: webdriver.Remote, timeout: int = 12):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def obtener_texto_menu_clientes(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.NAV_CLIENTES)).text

    def ir_a_clientes(self):
        enlace = self.wait.until(EC.element_to_be_clickable(self.NAV_CLIENTES))
        enlace.click()
        return self

    def crear_cliente(self, rut: str, nombre: str, correo: str, telefono: str):
        self.wait.until(EC.element_to_be_clickable(self.TAB_CREAR)).click()
        self.wait.until(EC.visibility_of_element_located(self.INPUT_RUT)).send_keys(rut)
        self.driver.find_element(*self.INPUT_NOMBRE).send_keys(nombre)
        self.driver.find_element(*self.INPUT_CORREO).send_keys(correo)
        self.driver.find_element(*self.INPUT_TELEFONO).send_keys(telefono)
        self.driver.find_element(*self.BTN_GUARDAR).click()

    def verificar_listado_visible(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.ENCABEZADO_TABLA)).text

    def cerrar_sesion(self):
        self.wait.until(EC.element_to_be_clickable(self.BTN_LOGOUT)).click()


# ==============================================================================
# 2. FIXTURE DE PYTEST PARA PYCHARM / CI-CD
# ==============================================================================

@pytest.fixture(scope="module")
def driver():
    """Inicializa Chrome WebDriver para la suite y garantiza su cierre al terminar."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,800")
    if os.getenv("HEADLESS", "0") == "1":
        options.add_argument("--headless=new")
    navegador = webdriver.Chrome(options=options)
    yield navegador
    navegador.quit()


# ==============================================================================
# 3. CASOS DE PRUEBA AUTOMATIZADOS CON ASERCIONES EXPLÍCITAS (GUÍA 3.3.2)
# ==============================================================================

def test_aut_01_login_exitoso(driver):
    """AUT-01: Verifica inicio de sesión válido y visibilidad del menú principal."""
    login_page = LoginPage(driver)
    clientes_page = ClientesPage(driver)

    login_page.abrir()
    assert "Iniciar Sesión" in login_page.obtener_titulo()

    login_page.iniciar_sesion("admin", "admin")
    # Aserción obligatoria (Guía 3.3.2: "Sin verificación, no hay prueba real")
    assert "Clientes" in clientes_page.obtener_texto_menu_clientes()


def test_aut_02_crear_cliente(driver):
    """AUT-02: Verifica la creación de un nuevo cliente y retorno al listado."""
    clientes_page = ClientesPage(driver)

    clientes_page.ir_a_clientes()
    clientes_page.crear_cliente(
        rut="76.543.210-K",
        nombre="Empresa Automatizada POM",
        correo="qa.pom@atlas.cl",
        telefono="+56988887777",
    )
    assert "Clientes registrados" in clientes_page.verificar_listado_visible()


def test_aut_03_verificar_listado_y_logout(driver):
    """AUT-03: Verifica el listado de clientes registrados y el cierre de sesión."""
    login_page = LoginPage(driver)
    clientes_page = ClientesPage(driver)

    assert "Clientes registrados" in clientes_page.verificar_listado_visible()
    clientes_page.cerrar_sesion()
    assert "Iniciar Sesión" in login_page.obtener_titulo()


if __name__ == "__main__":
    raise SystemExit(pytest.main(["-v", __file__]))
