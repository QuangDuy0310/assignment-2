import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()  


#Test log in
def test_valid_login(driver):
    try:
        driver.get("http://127.0.0.1:5000/")
        driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
        driver.find_element(By.ID, "usrname").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("12345")
        driver.find_element(By.XPATH, "//button[@id='login btn']").click()
        WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:5000/"))
        assert driver.current_url == "http://127.0.0.1:5000/"
        print("Login successful")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error during login test: {e}")

def test_invalid_login(driver: WebDriver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("123")
    driver.find_element(By.ID, "login btn").click()
    error_message = driver.find_element(By.XPATH, " //div[contains(@class, 'alert alert-danger')]").text
    assert "Incorrect Username or Password" in error_message
    
def test_valid_logout(driver: WebDriver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("12345")
    driver.find_element(By.ID, "login btn").click()
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/user-logout']"))
    ).click()
    
    WebDriverWait(driver, 10).until(
        EC.url_contains("http://127.0.0.1:5000/user-login")
    )

    





    



  




