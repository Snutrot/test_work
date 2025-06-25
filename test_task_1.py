import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from faker import Faker


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


@pytest.fixture
def fake():
    """Фикстура для генерации тестовых данных"""
    return Faker('ru_RU')  # Русская локализация


def test_form_validation(browser, fake):
    """Тест заполнения формы и проверки валидации"""
    # 1. Открытие страницы
    browser.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
    wait = WebDriverWait(browser, 10)

    # 2. Генерация тестовых данных
    form_data = {
        "first-name": fake.first_name(),
        "last-name": fake.last_name(),
        "address": fake.street_address(),
        "e-mail": fake.email(),
        "phone": fake.phone_number(),
        "zip-code": "",  # Оставляем пустым для теста валидации
        "city": fake.city(),
        "country": "Россия",
        "job-position": fake.job(),
        "company": fake.company()
    }

    # 3. Заполнение формы
    for field, value in form_data.items():
        browser.find_element(By.NAME, field).send_keys(value)

    # 4. Отправка формы
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # 5. Проверка подсветки полей
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert.py-2")))

    # Проверка, что Zip code подсвечен красным
    zip_code_field = browser.find_element(By.ID, "zip-code")
    assert "alert-danger" in zip_code_field.get_attribute("class")

    # Проверка, что остальные поля подсвечены зеленым
    valid_fields = [
        "first-name", "last-name", "address", "e-mail",
        "phone", "city", "country", "job-position", "company"
    ]

    for field_id in valid_fields:
        field = browser.find_element(By.ID, field_id)
        assert "alert-success" in field.get_attribute("class")
