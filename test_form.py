import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random 


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit() 

def test_upd_profile_fullname(driver):
    driver.get("http://localhost:5000/")
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    login_link = driver.find_element(By.LINK_TEXT, "Log In") #tìm kiếm link Login bằng text
    login_link.click()
    
    time.sleep(3)
    
    username_field = driver.find_element(By.ID, "usrname").send_keys("admin")
    password_field = driver.find_element(By.ID, "password").send_keys("12345")
    
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Login']")
    login_button.click()
    
    account_link = driver.find_element(By.CSS_SELECTOR, "li > a[href='/user-edit-account']") 
    account_link.click()
    time.sleep(3)
    
    fullname_field = driver.find_element(By.ID, "fullname")
    fullname_field.clear()  # Clear existing text
    fullname_field.send_keys("tuan")
    
    continue_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Continue']")
    continue_button.click()
    time.sleep(2)

    try:
        success_alert = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
        assert "Updated Successfully" in success_alert.text, "Success message not found after updating profile."
        # If the URL is correct, the test passes
        wait.until(EC.url_to_be("http://localhost:5000/user-edit-account"))
        
    except TimeoutException:
        # If not redirected to the cart page, fail the test
        assert False, "Failed to update"

def test_review_product(driver: webdriver.Chrome):
    driver.get("http://127.0.0.1:5000/")

    # Đăng nhập
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("12345")
    driver.find_element(By.ID, "login btn").click()  # Sửa lại ID nếu cần thiết
    time.sleep(5)
    driver.find_element(By.XPATH, "//a[@href='/product-list']").click()
    time.sleep(3)

    # Danh sách các XPATH của các sản phẩm
    products_xpath = [
        "//a[@href='/item-detail?product-id=1']",
        "//a[@href='/item-detail?product-id=2']",
        "//a[@href='/item-detail?product-id=7']",
        "//a[@href='/item-detail?product-id=8']",
        "//a[@href='/item-detail?product-id=9']",
        "//a[@href='/item-detail?product-id=3']"
    ]

# Chọn ngẫu nhiên một sản phẩm
    selected_product_xpath = random.choice(products_xpath)
    time.sleep(5)
    driver.find_element(By.XPATH, selected_product_xpath).click()
    time.sleep(5)
    # Tìm phần tử Reviews và nhấn vào nó
    reviews_link = driver.find_element(By.XPATH, "//a[@href='#Reviews' and @data-toggle='tab']")
    reviews_link.click()  # Nhấn vào liên kết Reviews

    time.sleep(5)  # Đợi một chút để trang tải lại (nếu cần)
    # Tìm trường input có id="name" và nhập thông tin vào
    name_input = driver.find_element(By.ID, "name")
    name_input.send_keys("duy")  # Thay "Tên của bạn" bằng thông tin muốn nhập

    time.sleep(5)  # Đợi một chút để xem kết quả nhập
    # Tìm trường input có id="email" và nhập thông tin vào
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("duy@gmail.com")  # Thay "Tên của bạn" bằng thông tin muốn nhập

    time.sleep(5)  # Đợi một chút để xem kết quả nhập
    # Tìm trường input có id="email" và nhập thông tin vào
    review_input = driver.find_element(By.ID, "review")
    review_input.send_keys("sản phẩm tốt")  # Thay "Tên của bạn" bằng thông tin muốn nhập

    time.sleep(5)  # Đợi một chút để xem kết quả nhập
# Wait for the button to be clickable
    button = driver.find_element(By.XPATH, "//button[@type='submit' and text(🙁'Send']")
    button.click()
    time.sleep(5)

# Kiểm tra xem nội dung của trang có chứa thông báo lỗi không
    page_source = driver.page_source

# Nếu có thông báo lỗi "Internal Server Error", test case sẽ thất bại
    if "Internal Server Error" in page_source:
      pytest.fail("Test failed. Internal Server Error encountered.")
    else:
    # Nếu không có thông báo lỗi, in ra thông báo pass
      print("Test passed. No internal server error.") 

