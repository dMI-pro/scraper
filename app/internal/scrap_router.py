from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import UploadFile, File, status
from pydantic import BaseModel
import logging
import uuid
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Input(BaseModel):
    url: str


class Output(BaseModel):
    html: str


scrap_router = APIRouter(prefix="/v1")


@scrap_router.post('/scrap',
             description='Scrap endpoint',
             tags=['Process endpoints'],
             status_code=status.HTTP_200_OK,
             response_model=Output)
def process_image(input_: Input) -> Output:
    logger.info(f"Received request to scrape URL: {input_.url}")
    scraper = Scraper()
    return Output(html=scraper.scrap(input_.url))


class Scraper:
    def __init__(self):
        logger.info("Initializing Scraper with Chrome options")
        # configure webdriver
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        # Используем предварительно созданную директорию с правильными правами
        session_id = str(uuid.uuid4())
        self.user_data_dir = f"/chrome-data/session-{session_id}"
        os.makedirs(self.user_data_dir, exist_ok=True)
        self.options.add_argument(f'--user-data-dir={self.user_data_dir}')
        
        logger.info(f"Chrome options configured successfully, using directory: {self.user_data_dir}")

    def scrap(self, url):
        try:
            logger.info("Starting Chrome WebDriver")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
            logger.info("WebDriver started successfully")
            
            logger.info(f"Navigating to URL: {url}")
            driver.get(url)
            
            # Явное ожидание для элемента с itemprop="name"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h3[itemprop="name"]'))
            )
            
            logger.info("Page loaded successfully")
            
            html = driver.page_source
            logger.info("Retrieved page source")
            
            driver.quit()
            logger.info("WebDriver closed")
            
            # Очищаем директорию после использования
            os.system(f"rm -rf {self.user_data_dir}")
            logger.info(f"Cleaned up Chrome data directory: {self.user_data_dir}")
            
            return html
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}", exc_info=True)
            if os.path.exists(self.user_data_dir):
                os.system(f"rm -rf {self.user_data_dir}")
                logger.info(f"Cleaned up Chrome data directory after error: {self.user_data_dir}")
            raise HTTPException(status_code=500, detail=str(e))


