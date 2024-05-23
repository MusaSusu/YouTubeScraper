from seleniumbase import SB
from selenium.webdriver.common.keys import Keys
import time

youtube_history_url = 'https://www.youtube.com/feed/history'


def get_URLS() -> []:
    """
    :rtype: object
    """
    with SB(uc=True) as sb:
        sb.open(youtube_history_url)
        # Wait for manual login if necessary, or implement automated login
        input("Press Enter after logging in...")

        driver = sb.driver

        # Scroll to load videos. Increase range for more scrolling if needed.
        for _ in range(10):  # Adjust the range based on your history size
            driver.find_element('body').send_keys(Keys.END)
            time.sleep(2)  # Adjust timing based on your connection speed

        # Find all video links
        video_elements = driver.find_elements('a#thumbnail')
        video_urls = [elem.get_attribute('href') for elem in video_elements]
        print(f"Found {len(video_urls)} elements")

        # Extract video IDs from URLs
        video_ids = []
        for url in video_urls:
            if url and 'watch?v=' in url:
                video_id = url.split('watch?v=')[1]
                video_ids.append(video_id.split('&')[0])

        print(f"Found {len(video_ids)} video IDs.")
        for video_id in video_ids:
            print(video_id)

        # Clean up by closing the browser
        driver.quit()

        return video_ids[50:]
