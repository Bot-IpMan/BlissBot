#!/usr/bin/env python3
"""
Робочий приклад підключення до BlissOS через Appium
"""

import requests
import json
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BlissBotController:
    def __init__(self, appium_url="http://localhost:4723", emulator_host="172.26.209.4"):
        self.appium_url = appium_url
        self.emulator_host = emulator_host
        self.driver = None
        
    def setup_driver(self):
        """Налаштування підключення до емулятора"""
        
        # Опції для підключення до BlissOS
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "BlissOS_Emulator"
        
        # Важливо: вказуємо IP емулятора
        options.udid = f"{self.emulator_host}:5555"
        
        # Налаштування для BlissOS
        options.automation_name = "UiAutomator2"
        options.new_command_timeout = 300
        options.no_reset = True  # Не скидати стан додатків
        
        try:
            print(f"🔄 Підключення до емулятора {self.emulator_host}...")
            self.driver = webdriver.Remote(
                command_executor=f"{self.appium_url}",
                options=options
            )
            print("✅ Успішно підключено до емулятора!")
            return True
            
        except Exception as e:
            print(f"❌ Помилка підключення: {e}")
            return False
    
    def test_connection(self):
        """Перевірка підключення"""
        if not self.driver:
            return False
            
        try:
            # Отримуємо інформацію про пристрій
            print("📱 Інформація про пристрій:")
            print(f"   Платформа: {self.driver.capabilities.get('platformName')}")
            print(f"   Версія: {self.driver.capabilities.get('platformVersion')}")
            print(f"   Пристрій: {self.driver.capabilities.get('deviceName')}")
            
            # Робимо скріншот для перевірки
            screenshot_path = "/opt/appium/screenshots/test_connection.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Скріншот збережено: {screenshot_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Помилка тестування: {e}")
            return False
    
    def open_settings(self):
        """Відкриття налаштувань Android"""
        try:
            print("🔧 Відкриваю налаштування...")
            
            # Метод 1: Через intent
            self.driver.start_activity("com.android.settings", ".Settings")
            time.sleep(3)
            
            print("✅ Налаштування відкрито!")
            return True
            
        except Exception as e:
            print(f"❌ Помилка відкриття налаштувань: {e}")
            
            # Метод 2: Через пошук по тексту
            try:
                print("🔄 Пробую альтернативний метод...")
                
                # Свайп вниз для відкриття панелі повідомлень
                self.driver.swipe(500, 100, 500, 600, 1000)
                time.sleep(1)
                
                # Пошук іконки налаштувань
                settings_button = self.driver.find_element(
                    By.XPATH, 
                    "//*[@content-desc='Settings' or contains(@text,'Settings') or contains(@text,'Налаштування')]"
                )
                settings_button.click()
                
                print("✅ Налаштування відкрито альтернативним методом!")
                return True
                
            except Exception as e2:
                print(f"❌ Альтернативний метод також не спрацював: {e2}")
                return False
    
    def open_calculator(self):
        """Відкриття калькулятора та обчислення 15 + 25"""
        try:
            print("🧮 Відкриваю калькулятор...")
            
            # Спробуємо різні пакети калькулятора
            calculator_packages = [
                ("com.android.calculator2", ".Calculator"),
                ("com.google.android.calculator", ".Calculator"),
                ("com.sec.android.app.popupcalculator", ".Calculator"),
            ]
            
            for package, activity in calculator_packages:
                try:
                    self.driver.start_activity(package, activity)
                    time.sleep(2)
                    print(f"✅ Калькулятор відкрито: {package}")
                    break
                except:
                    continue
            else:
                # Якщо не вдалося відкрити через activity, шукаємо на робочому столі
                print("🔍 Шукаю калькулятор на робочому столі...")
                calc_icon = self.driver.find_element(
                    By.XPATH,
                    "//*[contains(@text,'Calculator') or contains(@text,'Калькулятор') or @content-desc='Calculator']"
                )
                calc_icon.click()
                time.sleep(2)
            
            # Обчислення 15 + 25
            print("🔢 Виконую обчислення 15 + 25...")
            
            # Натискаємо цифри та операції
            buttons_to_press = ['1', '5', '+', '2', '5', '=']
            
            for button in buttons_to_press:
                try:
                    # Шукаємо кнопку по тексту або content-desc
                    calc_button = self.driver.find_element(
                        By.XPATH,
                        f"//*[@text='{button}' or @content-desc='{button}']"
                    )
                    calc_button.click()
                    time.sleep(0.5)
                    print(f"   Натиснуто: {button}")
                    
                except Exception as e:
                    print(f"   ⚠️ Не вдалося натиснути {button}: {e}")
            
            # Отримуємо результат
            try:
                result_element = self.driver.find_element(
                    By.XPATH,
                    "//*[contains(@resource-id,'result') or contains(@resource-id,'display')]"
                )
                result = result_element.text
                print(f"🎯 Результат: {result}")
                
            except:
                print("⚠️ Не вдалося отримати результат")
            
            return True
            
        except Exception as e:
            print(f"❌ Помилка з калькулятором: {e}")
            return False
    
    def take_screenshot(self, name="screenshot"):
        """Робить скріншот"""
        if self.driver:
            screenshot_path = f"/opt/appium/screenshots/{name}_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Скріншот збережено: {screenshot_path}")
            return screenshot_path
        return None
    
    def cleanup(self):
        """Закриття з'єднання"""
        if self.driver:
            self.driver.quit()
            print("🔚 З'єднання закрито")

def main():
    print("🤖 BlissBot - Тестування підключення до Android")
    print("=" * 50)
    
    # Ініціалізація контролера
    bot = BlissBotController()
    
    try:
        # 1. Налаштування підключення
        if not bot.setup_driver():
            print("❌ Не вдалося підключитися до емулятора")
            return
        
        # 2. Тестування підключення
        if not bot.test_connection():
            print("❌ Проблеми з тестуванням підключення")
            return
        
        # 3. Робимо скріншот поточного стану
        bot.take_screenshot("initial_state")
        
        # 4. Тестуємо відкриття налаштувань
        print("\n" + "="*30)
        if bot.open_settings():
            bot.take_screenshot("settings_opened")
            time.sleep(2)
        
        # 5. Тестуємо калькулятор
        print("\n" + "="*30)
        if bot.open_calculator():
            bot.take_screenshot("calculator_result")
        
        print("\n✅ Тестування завершено!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Зупинено користувачем")
        
    finally:
        bot.cleanup()

if __name__ == "__main__":
    main()
