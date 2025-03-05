import time
from datetime import datetime

from common.custom_logger import CustomLogger
from page.android.home_page import HomePage
from page.common.base_page import BasePage


class NineDayPage(HomePage):
    """
    Nine-day Weather Forecast Page Class

    Inherits from HomePage class, implements specific functionality for the nine-day
    weather forecast page. Includes methods for retrieving weather forecast information
    and page navigation.
    """

    def __init__(self, driver):
        """
        Initialize the Nine-day Forecast page

        Args:
            driver: WebDriver instance for UI automation
        """
        super().__init__(driver)
        self.drawer_layout = {'xpath': rf'//*[@resource-id="hko.MyObservatory_v1_0:id/drawer_layout"]'}
        self.quote_page_xpath = {
            'xpath': '//*[@resource-id="com.tdx.AndroidNewXN:id/main_tab"]/android.widget.LinearLayout[2]'}
        self.update_time = {'xpath': '//*[@resource-id="hko.MyObservatory_v1_0:id/mainAppSevenDayUpdateTime"]'}

    def go_to_nine_page(self):
        """
        Navigate to the nine-day forecast page

        Opens the drawer layout and navigates to the nine-day forecast section
        """
        CustomLogger.print_step("Navigating to Nine-day Forecast")
        self.navigate_to_drawer_layout()
        self.click(self.expand_forcast_and_alarm)
        time.sleep(5)
        self.click(self.nine_day_forcast_in_drawer_layout)

    def get_nine_day_weather_day_info(self):
        """
        Retrieve weather information for the ninth day

        Returns:
            tuple: Contains the following weather information:
                - nine_day_temp (str): Temperature
                - nine_day_rh (str): Relative humidity
                - nine_day_date (str): Forecast date
                - nine_day_week_date (str): Day of the week
                - nine_day_psr (str): UV index
                - nine_day_description (str): Weather description
        """
        CustomLogger.print_step("Retrieving ninth day weather information")

        # Scroll to the bottom to ensure all elements are visible
        self.scroll_to_end()

        # Get temperature information
        self.temp_xpath = {'xpath': '//*[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_temp"]'}
        temp_list = self.find_element(self.temp_xpath).all()
        nine_day_temp = temp_list[-1].text if temp_list is not None else None

        # Get humidity information
        self.rh_xpath = {
            'xpath': '//*[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_rh"]'}
        rh_list = self.find_element(self.rh_xpath).all()
        nine_day_rh = rh_list[-1].text if rh_list is not None else None

        # Get date information
        self.date_xpath = {
            'xpath': '//*[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_date"]'}
        date_list = self.find_element(self.date_xpath).all()
        nine_day_date = date_list[-1].text if date_list is not None else None

        # Get day of week information
        self.day_of_week_xpath = {
            'xpath': '//*[@resource-id="hko.MyObservatory_v1_0:id/sevenday_forecast_day_of_week"]'}
        day_of_week_list = self.find_element(self.day_of_week_xpath).all()
        nine_day_week_date = day_of_week_list[-1].text if day_of_week_list is not None else None

        # Get UV index information
        self.psr_xpath = {
            'xpath': '//*[@resource-id="hko.MyObservatory_v1_0:id/psrText"]'}
        psr_list = self.find_element(self.psr_xpath).all()
        nine_day_psr = psr_list[-1].text if psr_list is not None else None

        # Get weather description
        self.description_xpath = {
            'xpath': f'//android.widget.LinearLayout'}
        weather_description = self.find_element(self.description_xpath).xpath(
            f'//*[contains(@content-desc, "{nine_day_date}")]').all()
        nine_day_description = weather_description[-1].info.get('contentDescription') if weather_description is not None else None

        return nine_day_temp, nine_day_rh, nine_day_date, nine_day_week_date, nine_day_psr, nine_day_description

    def scroll_to_end(self):
        """
        Scroll to the bottom of the page

        Uses screen hierarchy comparison to determine when the bottom is reached.
        Implements smooth scrolling using relative screen dimensions.
        """
        while True:
            # Get page layout before scrolling
            before_scroll = self.driver.driver.dump_hierarchy()
            width, height = self.driver.driver.window_size()
            
            # Perform scroll action
            self.swipe(
                start_x=0.5 * width, 
                start_y=0.8 * height,
                end_x=0.5 * width, 
                end_y=0.5 * height, 
                duration=0.1
            )
            
            # Get page layout after scrolling
            after_scroll = self.driver.driver.dump_hierarchy()
            
            # Check if bottom is reached
            if before_scroll == after_scroll:
                break

    def get_update_date(self):
        """
        Get the last update date of the weather forecast

        Returns:
            str: Formatted date string in "MM月DD日" format
        """
        update_time = self.find_element(self.update_time).text
        date_part = update_time.split(":")[1].strip()
        
        # Convert date string to datetime object
        date_obj = datetime.strptime(date_part, "%Y年%m月%d日%H时%M分")
        
        # Format date as required
        formatted_date = date_obj.strftime("%m月%d日")
        return formatted_date
