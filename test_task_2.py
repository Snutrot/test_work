import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import time

def configure_driver():
    """Настройка драйвера Chrome"""
    options = Options()
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options

@pytest.fixture
def browser():
    """Фикстура для инициализации и закрытия браузера"""
    driver = webdriver.Chrome(options=configure_driver())
    yield driver
    driver.quit()

def test_slow_calculator(browser):
    """Тест медленного калькулятора с задержкой"""
    # 1. Открытие страницы
    browser.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
    
    # 2. Установка задержки 45 секунд
    delay_input = browser.find_element(By.CSS_SELECTOR, "#delay")
    delay_input.clear()
    delay_input.send_keys("45")
    
    # 3. Нажатие кнопок 7 + 8 =
    browser.find_element(By.XPATH, "//span[text()='7']").click()
    browser.find_element(By.XPATH, "//span[text()='+']").click()
    browser.find_element(By.XPATH, "//span[text()='8']").click()
    browser.find_element(By.XPATH, "//span[text()='=']").click()
    
    # 4. Проверка результата через 45 секунд
    start_time = time()
    result = WebDriverWait(browser, 46).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), "15")
    )
    end_time = time()
    
    # Проверка что результат появился через ~45 секунд
    elapsed_time = end_time - start_time
    assert 45 <= elapsed_time <= 47, f"Результат появился через {elapsed_time:.1f} секунд, ожидалось ~45 секунд"
    
    # Дополнительная проверка точного результата
    result_text = browser.find_element(By.CSS_SELECTOR, ".screen").text
    assert result_text == "15", f"Ожидался результат 15, получено {result_text}"