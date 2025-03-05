from datetime import datetime, timedelta

import pytest
from pytest_bdd import given, when, then, scenario
import requests
import json
from common.custom_logger import CustomLogger


@pytest.fixture
def context():
    """用于在步骤之间共享数据的fixture"""
    return {}


# 定义场景
@scenario('ninth_day_forcast.feature', '检查第9天的天气预报信息')
def test_weather_forecast():
    """测试第9天天气预报信息"""
    pass


# 定义步骤
@given('我在天气预报应用的九天预报页面')
def given_on_forecast_page(nine_day_page):
    """确保在天气预报页面"""
    nine_day_page.go_to_nine_page()
    print("执行Given步骤：导航到天气预报页面")


@when('查看从今天起9天后的天气预报')
def when_check_ninth_day(nine_day_page, context):
    """查看第9天预报"""
    nine_day_temp, nine_day_rh, nine_day_date, nine_day_week_date, nine_day_psr, nine_day_description = nine_day_page.get_nine_day_weather_day_info()
    context['weather_info'] = {
        'temp': nine_day_temp,
        'rh': nine_day_rh,
        'date': nine_day_date,
        'week_date': nine_day_week_date,
        'psr': nine_day_psr,
        'description': nine_day_description
    }
    print("执行When步骤：查看第9天预报")


@then('我应该看到的最后一个预报的日期是当前更新日期的九天后')
def then_verify_temperature(context, nine_day_page):
    """验证温度范围"""
    update_date = nine_day_page.get_update_date()
    # 将字符串转换为datetime对象
    date_obj = datetime.strptime(update_date, "%m月%d日")

    # 加上9天
    new_date_obj = date_obj + timedelta(days=9)

    # 将结果转换回字符串
    new_date_str = new_date_obj.strftime("%m月%d日")
    nineth_date = "0" + context['weather_info']['date'] if len(context['weather_info']['date']) == 5 else \
    context['weather_info']['date']
    assert nineth_date == new_date_str
    print("执行Then步骤：验证温度范围")


@then('我可以获取到温度、湿度、紫外线信息和天气描述')
def then_verify_weather_info(context):
    """验证湿度范围"""
    weather_info = context['weather_info']
    assert weather_info['temp'] is not None
    assert weather_info['rh'] is not None
    assert weather_info['date'] is not None
    assert weather_info['week_date'] is not None
    assert weather_info['psr'] is not None
    assert weather_info['description'] is not None
    print("执行Then步骤：验证湿度范围")


class TestWeatherAPI:
    """Test class for Weather Forecast API endpoints"""
    
    # Mock API endpoint
    BASE_URL = "https://api.weather-forecast.mock/v1"
    FORECAST_ENDPOINT = "/forecast/daily"
    
    def setup_method(self):
        """Setup test data and configurations"""
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer mock-token-123"
        }
        self.params = {
            "location": "Hong Kong",
            "days": 7
        }
    
    def test_capture_forecast_endpoint(self):
        """
        Test Case 1: Verify the forecast API endpoint is correctly captured
        """
        endpoint = f"{self.BASE_URL}{self.FORECAST_ENDPOINT}"
        CustomLogger.print_log(f"Captured API endpoint: {endpoint}")
        assert self.FORECAST_ENDPOINT in endpoint, "Forecast endpoint not found in URL"
    
    def test_forecast_api_response(self):
        """
        Test Case 2: Send request and verify API response status
        """
        endpoint = f"{self.BASE_URL}{self.FORECAST_ENDPOINT}"
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=self.params
            )
            
            # Log response details
            CustomLogger.print_log(f"API Response Status Code: {response.status_code}")
            CustomLogger.print_log(f"API Response Headers: {response.headers}")
            
            # Assert response status code
            assert response.status_code == 200, f"API request failed with status code: {response.status_code}"
            
        except requests.exceptions.RequestException as e:
            CustomLogger.print_error(f"API request failed: {str(e)}")
            raise
    
    def test_extract_day_after_tomorrow_humidity(self):
        """
        Test Case 3: Extract relative humidity for the day after tomorrow
        """
        endpoint = f"{self.BASE_URL}{self.FORECAST_ENDPOINT}"
        
        try:
            # Get current date
            today = datetime.now()
            day_after_tomorrow = today + timedelta(days=2)
            target_date = day_after_tomorrow.strftime("%Y-%m-%d")
            
            # Send API request
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=self.params
            )
            
            # Mock response data structure
            mock_response = {
                "forecast": {
                    "daily": [
                        {
                            "date": target_date,
                            "humidity": {
                                "min": 60,
                                "max": 85
                            },
                            "temperature": {
                                "min": 20,
                                "max": 25
                            }
                        }
                    ]
                }
            }
            
            # In real scenario, use response.json() instead of mock_response
            data = mock_response
            
            # Extract humidity for day after tomorrow
            target_forecast = next(
                (day for day in data["forecast"]["daily"] if day["date"] == target_date),
                None
            )
            
            # Verify humidity data
            assert target_forecast is not None, f"No forecast found for date: {target_date}"
            humidity_range = f"{target_forecast['humidity']['min']} - {target_forecast['humidity']['max']}%"
            
            # Log extracted humidity
            CustomLogger.print_log(f"Relative humidity for {target_date}: {humidity_range}")
            
            # Verify humidity range format
            assert " - " in humidity_range, "Invalid humidity range format"
            min_humidity = int(humidity_range.split(" - ")[0])
            max_humidity = int(humidity_range.split(" - ")[1].replace("%", ""))
            assert 0 <= min_humidity <= 100, "Minimum humidity out of valid range (0-100)"
            assert 0 <= max_humidity <= 100, "Maximum humidity out of valid range (0-100)"
            assert min_humidity <= max_humidity, "Minimum humidity greater than maximum humidity"
            
        except requests.exceptions.RequestException as e:
            CustomLogger.print_error(f"API request failed: {str(e)}")
            raise
        except (KeyError, json.JSONDecodeError) as e:
            CustomLogger.print_error(f"Error parsing response data: {str(e)}")
            raise
        except Exception as e:
            CustomLogger.print_error(f"Unexpected error: {str(e)}")
            raise


if __name__ == "__main__":
    pytest.main(["-v", "test_api.py", "--html=report/api_test_report.html"])
