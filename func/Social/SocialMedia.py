# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

chrome_options = Options()
chrome_options.add_argument('--headless')  # Use headless mode for invisible browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

media = {
    "Youtube bio": ["https://www.youtube.com/@Techiral", '//*[@id="meta"]'],
    "Instagram live details": ["https://www.instagram.com/techiral_the_future/",
                               '//section/main/div/header/section/ul']
}

def social_texter(website, xpath):
    driver.get(website)
    sleep(2)  # Allow time for the page to load
    try:
        element_text = driver.find_element(By.XPATH, xpath).text
        return element_text
    except Exception as e:
        print(f"Failed to fetch text from {website} using XPath {xpath}: {e}")
        return "Failed to retrieve text"

def social_media():
    data = ""
    for platform, details in media.items():
        data += f"\n--------------------\n{platform}\n"
        text = social_texter(details[0], details[1])
        if text:
            data += text + "\n"
        else:
            data += "No data found\n"
    driver.quit()
    return data

if __name__ == "__main__":
    result = social_media()
    print(result)
