from common.locate_type import LocateBy
from page.common.base_page import BasePage


class HomePage(BasePage):
    """
    Weather Forecast App Home Page

    This class contains all page elements and operations for the weather forecast app's home page.
    Inherits from BasePage class and implements home page specific functionality.
    """

    def __init__(self, driver):
        """
        Initialize the home page object

        Args:
            driver: UI automation driver instance
        """
        super().__init__(driver)

    # Page element locators
    DRAWER_LAYOUT = {'xpath': '//android.widget.ImageButton'}  # Drawer menu button
    expand_forcast_and_alarm = {'xpath': '//*[@resource-id="hko.MyObservatory_v1_0:id/header_layout"]'}  # Expand forecast and alarm panel
    nine_day_forcast_in_drawer_layout = {
        'xpath': '/hierarchy/android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.ScrollView[1]/androidx.drawerlayout.widget.DrawerLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]/androidx.appcompat.widget.LinearLayoutCompat[1]/androidx.recyclerview.widget.RecyclerView[1]/android.widget.LinearLayout[1]/androidx.recyclerview.widget.RecyclerView[1]/android.widget.FrameLayout[4]'
    }  # Nine-day forecast option in drawer menu

    def navigate_to_drawer_layout(self):
        """
        Open the drawer menu

        Clicks the drawer menu button to expand the navigation menu
        """
        self.click(self.DRAWER_LAYOUT)

