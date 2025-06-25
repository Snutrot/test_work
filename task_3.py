import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class SauceDemoTest(unittest.TestCase):
    """Тест для интернет-магазина Sauce Demo"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        options = Options()
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)  # Увеличили таймаут
        self.driver.get("https://www.saucedemo.com/")
        
        # Авторизация с явными ожиданиями
        self.wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        self.wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("secret_sauce")
        self.wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    def test_shopping_cart_total(self):
        """Проверка итоговой суммы заказа"""
        # 1. Добавление товаров в корзину
        items_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]
        
        for item_name in items_to_add:
            item_locator = (By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button")
            self.wait.until(EC.element_to_be_clickable(item_locator)).click()
        
        # 2. Переход в корзину
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()
        
        # 3. Начало оформления заказа
        self.wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        
        # 4. Заполнение формы
        self.wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Павел")
        self.driver.find_element(By.ID, "last-name").send_keys("Лебедев")
        self.driver.find_element(By.ID, "postal-code").send_keys("196158")
        self.wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
        
        # 5. Проверка итоговой суммы
        total_element = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "summary_total_label"), "Total: $58.29")
        )
        self.assertTrue(total_element, "Неверная итоговая сумма заказа")

    def tearDown(self):
        """Очистка после каждого теста"""
        input("Нажмите Enter для закрытия браузера...")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
