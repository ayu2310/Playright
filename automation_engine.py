import asyncio
import logging
from typing import Dict, List, Any, Optional
from playwright.async_api import async_playwright, Browser, Page
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrowserAutomationEngine:
    def __init__(self, browser_type: str = "playwright", headless: bool = False):
        self.browser_type = browser_type
        self.headless = headless
        self.playwright_browser = None
        self.playwright_page = None
        self.selenium_driver = None
        
    async def start_browser(self):
        """Start the browser based on the specified type"""
        if self.browser_type == "playwright":
            await self._start_playwright()
        else:
            await self._start_selenium()
    
    async def _start_playwright(self):
        """Start Playwright browser"""
        try:
            self.playwright = await async_playwright().start()
            self.playwright_browser = await self.playwright.chromium.launch(
                headless=self.headless
            )
            self.playwright_page = await self.playwright_browser.new_page()
            logger.info("Playwright browser started successfully")
        except Exception as e:
            logger.error(f"Failed to start Playwright browser: {e}")
            raise
    
    async def _start_selenium(self):
        """Start Selenium browser"""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            self.selenium_driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Selenium browser started successfully")
        except Exception as e:
            logger.error(f"Failed to start Selenium browser: {e}")
            raise
    
    async def navigate_to(self, url: str):
        """Navigate to a URL"""
        try:
            if self.browser_type == "playwright":
                await self.playwright_page.goto(url)
                await self.playwright_page.wait_for_load_state("networkidle")
            else:
                self.selenium_driver.get(url)
                WebDriverWait(self.selenium_driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            logger.info(f"Navigated to {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise
    
    async def click_element(self, selector: str, selector_type: str = "css"):
        """Click an element on the page"""
        try:
            if self.browser_type == "playwright":
                await self.playwright_page.click(selector)
            else:
                if selector_type == "css":
                    element = self.selenium_driver.find_element(By.CSS_SELECTOR, selector)
                elif selector_type == "xpath":
                    element = self.selenium_driver.find_element(By.XPATH, selector)
                elif selector_type == "id":
                    element = self.selenium_driver.find_element(By.ID, selector)
                else:
                    element = self.selenium_driver.find_element(By.CSS_SELECTOR, selector)
                element.click()
            logger.info(f"Clicked element: {selector}")
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {e}")
            raise
    
    async def type_text(self, selector: str, text: str, selector_type: str = "css"):
        """Type text into an input field"""
        try:
            if self.browser_type == "playwright":
                await self.playwright_page.fill(selector, text)
            else:
                if selector_type == "css":
                    element = self.selenium_driver.find_element(By.CSS_SELECTOR, selector)
                elif selector_type == "xpath":
                    element = self.selenium_driver.find_element(By.XPATH, selector)
                elif selector_type == "id":
                    element = self.selenium_driver.find_element(By.ID, selector)
                else:
                    element = self.selenium_driver.find_element(By.CSS_SELECTOR, selector)
                element.clear()
                element.send_keys(text)
            logger.info(f"Typed text into {selector}")
        except Exception as e:
            logger.error(f"Failed to type text into {selector}: {e}")
            raise
    
    async def wait_for_element(self, selector: str, timeout: int = 10, selector_type: str = "css"):
        """Wait for an element to be present"""
        try:
            if self.browser_type == "playwright":
                await self.playwright_page.wait_for_selector(selector, timeout=timeout * 1000)
            else:
                if selector_type == "css":
                    WebDriverWait(self.selenium_driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                elif selector_type == "xpath":
                    WebDriverWait(self.selenium_driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                elif selector_type == "id":
                    WebDriverWait(self.selenium_driver, timeout).until(
                        EC.presence_of_element_located((By.ID, selector))
                    )
            logger.info(f"Element {selector} is present")
        except Exception as e:
            logger.error(f"Failed to wait for element {selector}: {e}")
            raise
    
    async def get_text(self, selector: str, selector_type: str = "css") -> str:
        """Get text from an element"""
        try:
            if self.browser_type == "playwright":
                text = await self.playwright_page.text_content(selector)
            else:
                if selector_type == "css":
                    element = self.selenium_driver.find_element(By.CSS_SELECTOR, selector)
                elif selector_type == "xpath":
                    element = self.selenium_driver.find_element(By.XPATH, selector)
                elif selector_type == "id":
                    element = self.selenium_driver.find_element(By.ID, selector)
                else:
                    element = self.selenium_driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text
            logger.info(f"Got text from {selector}: {text[:50]}...")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from {selector}: {e}")
            raise
    
    async def take_screenshot(self, path: str = "screenshot.png"):
        """Take a screenshot"""
        try:
            if self.browser_type == "playwright":
                await self.playwright_page.screenshot(path=path)
            else:
                self.selenium_driver.save_screenshot(path)
            logger.info(f"Screenshot saved to {path}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            raise
    
    async def close_browser(self):
        """Close the browser"""
        try:
            if self.browser_type == "playwright":
                if self.playwright_page:
                    await self.playwright_page.close()
                if self.playwright_browser:
                    await self.playwright_browser.close()
                if self.playwright:
                    await self.playwright.stop()
            else:
                if self.selenium_driver:
                    self.selenium_driver.quit()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Failed to close browser: {e}")
            raise