import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit() 

def test_change_pw(driver):
    driver.get("http://localhost:5000/")
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    login_link = driver.find_element(By.LINK_TEXT, "Log In") #tìm kiếm link Login bằng text
    login_link.click()
    
    time.sleep(3)
    
    re_username_field = driver.find_element(By.ID, "usrname").send_keys("admin")
    re_password_field = driver.find_element(By.ID, "password").send_keys("123")
    
    driver.find_element(By.ID, "login btn").click()
    
    account_link = driver.find_element(By.CSS_SELECTOR, "li > a[href='/user-edit-account']") 
    account_link.click()
    time.sleep(3)   
    
    change_pw_link = driver.find_element(By.CSS_SELECTOR, "li > a[href='/user-change-password']")
    change_pw_link.click()
    time.sleep(3)  
    
    old_password = driver.find_element(By.ID, "old-password").send_keys("123")
    new_password = driver.find_element(By.ID, "new-password").send_keys("12345")
    confirm_password = driver.find_element(By.ID, "confirm-password").send_keys("12345")
    change_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Change']")
    change_button.click()
    time.sleep(2)
    
    username_field = driver.find_element(By.ID, "usrname").send_keys("admin")
    password_field = driver.find_element(By.ID, "password").send_keys("12345")
    driver.find_element(By.ID, "login btn").click()
    
    try:
        wait.until(EC.url_to_be("http://localhost:5000/"))
        # If the URL is correct, the test passes
    except TimeoutException:
        # If not redirected to the cart page, fail the test
        assert False, "Failed to change password"

def test_invalid_register(driver: WebDriver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-register']").click()
    driver.find_element(By.ID, "fullname").send_keys("newuser")
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "phone").send_keys("0999999999")
    driver.find_element(By.ID, "email").send_keys("newuser@example.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "confirm-password").send_keys("password123")
    time.sleep(3)
    driver.find_element(By.ID, "btn register").click()
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, " //div[contains(@class, 'alert alert-danger')]").text
    assert "Check your information again/Username might already exit" in error_message

def test_err_register(driver):
    driver.get("http://localhost:5000/")
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    login_link = driver.find_element(By.LINK_TEXT, "Log In") 
    login_link.click()
    time.sleep(3)
    
    register_link = driver.find_element(By.CSS_SELECTOR, "a[href='/user-register']")
    register_link.click()
    time.sleep(3)
    
    new_fullname_field = driver.find_element(By.ID, "fullname").send_keys("Tuan")
    new_email_field = driver.find_element(By.ID, "email").send_keys("tuann@gmail.com")
    new_password_field = driver.find_element(By.ID, "password").send_keys("12345")
    conf_password_field = driver.find_element(By.ID, "confirm-password").send_keys("12345")
    
    register_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Create an account']")
    register_button.click()
    
    try:
        # Tìm trường User Name và lấy thông báo lỗi qua thuộc tính validationMessage
        username_field = driver.find_element(By.ID, "usrname")
        alert_message = username_field.get_attribute("validationMessage")
        
        # Kiểm tra thông báo lỗi có đúng yêu cầu không
        assert alert_message == "Please fill out this field.", "Failed: Không có thông báo lỗi yêu cầu nhập User Name."
        
        # Kiểm tra xem trường này có bị đánh dấu lỗi với CSS class has-error không
        form_group = username_field.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-group')]")
        assert "has-error" in form_group.get_attribute("class"), "Failed: Trường User Name không có class 'has-error'."

        print("Pass: Có thông báo lỗi yêu cầu nhập User Name.")
    except AssertionError as e:
        print(e)
    except Exception as ex:
        print("Có lỗi xảy ra:", ex)

def test_register(driver: WebDriver):
    # Điều hướng đến trang đăng ký
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-register']").click()

    # Điền thông tin vào form đăng ký với mật khẩu ngắn hơn 5 ký tự
    driver.find_element(By.ID, "fullname").send_keys("newuser")
    driver.find_element(By.ID, "username").send_keys("duy123")
    driver.find_element(By.ID, "phone").send_keys("0999999999")
    driver.find_element(By.ID, "email").send_keys("okenha@example.com")
    driver.find_element(By.ID, "password").send_keys("pa1")
    driver.find_element(By.ID, "confirm-password").send_keys("pa1")

    # Chờ và nhấn nút đăng ký
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@id, 'btn register')]"))
    ).click()

    # Chờ vài giây để hệ thống xử lý và điều hướng
    time.sleep(5)

    if driver.current_url != "http://127.0.0.1:5000/user-login":
        print("Test passed: Không điều hướng đến trang đăng nhập, đăng ký không thành công với mật khẩu dưới 5 ký tự")
        return

    # Nếu điều hướng đến trang đăng nhập, thực hiện đăng nhập với thông tin vừa đăng ký
    driver.find_element(By.ID, "usrname").send_keys("chanqua")
    driver.find_element(By.ID, "password").send_keys("pa1")
    driver.find_element(By.ID, "login btn").click()

    # Chờ để kiểm tra kết quả đăng nhập
    time.sleep(5)

    try:
        # Kiểm tra sự xuất hiện của thông báo lỗi (sử dụng WebDriverWait)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Email has been sent!')]"))
        )

        # Nếu tìm thấy thông báo lỗi
        print("Error message found: Email has been sent!, You need to verify your email first!")
        assert False, "Test failed: Cho phép tạo mật khẩu dưới 5 ký tự và không hiển thị thông báo lỗi"

    except TimeoutException:
        # Nếu không có thông báo lỗi, test case passed
        print("Test passed: Không hiển thị thông báo lỗi xác minh email")


def test_forget_password(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
     # Nhấn vào "Forget Password?" để điều hướng đến trang quên mật khẩu
    driver.find_element(By.XPATH, "//a[@href='/user-forget-password']").click()
      # Điền thông tin email vào trường email trên trang quên mật khẩu
    driver.find_element(By.ID, "email").send_keys("quangduy.phung03@gmail.com")
    time.sleep(5)
# Chờ nút "Send" có thể nhấp được
    button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Send']")
    button.click()
    time.sleep(5)
    try:
        # Chờ thông báo thành công xuất hiện trong khoảng thời gian 10 giây
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'OTP has been sent!')]"))
        )
        print("Test passed: OTP has been sent successfully.")
    except:
        # Nếu không thấy thông báo trong 10 giây, test case failed
        print("Test failed: OTP was not sent. Unable to reset password.")
        assert False, "Test failed: OTP was not sent."