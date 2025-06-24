from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def main():
    # Настройка драйвера
    options = Options()
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Инициализация драйвера
    driver = webdriver.Chrome(options=options)
    
    try:
        # 1. Открытие сайта
        driver.get("https://www.saucedemo.com/")
        
        # 2. Авторизация
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # 3. Добавление товаров в корзину
        items_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]
        
        for item_name in items_to_add:
            item_xpath = f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
            driver.find_element(By.XPATH, item_xpath).click()
        
        # 4. Переход в корзину
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        
        # 5. Начало оформления заказа
        driver.find_element(By.ID, "checkout").click()
        
        # 6. Заполнение формы
        driver.find_element(By.ID, "first-name").send_keys("Павел")
        driver.find_element(By.ID, "last-name").send_keys("Лебедев")
        driver.find_element(By.ID, "postal-code").send_keys("196158")
        driver.find_element(By.ID, "continue").click()
        
        # 7. Проверка итоговой суммы
        total_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )
        total_text = total_element.text
        
        # Вывод результата
        if total_text == "Total: $58.29":
            print("Тест пройден успешно! Итоговая сумма: $58.29")
        else:
            print(f"Тест не пройден. Ожидалась сумма $58.29, получено {total_text}")
            
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        
    finally:
        input("Проверяем итог, нажмаем Enter для закрытия браузера")
        driver.quit()

if __name__ == "__main__":
    main()