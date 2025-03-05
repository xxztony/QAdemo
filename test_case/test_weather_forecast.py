from datetime import datetime, timedelta

import pytest
from pytest_bdd import given, when, then, scenario


@pytest.fixture
def context():
    """Fixture for sharing data between BDD test steps"""
    return {}


# Define scenario
@scenario('ninth_day_forcast.feature', '检查第9天的天气预报信息')
def test_weather_forecast():
    """Test the completeness and accuracy of the 9th day weather forecast information"""
    pass


# Define steps
@given('我在天气预报应用的九天预报页面')
def given_on_forecast_page(nine_day_page, request):
    """
    Precondition: Ensure the application is on the nine-day forecast page
    Args:
        nine_day_page: Nine-day forecast page object
        request: pytest request object for logging
    """
    nine_day_page.go_to_nine_page()
    request.node.add_report_section(
        "call", "Given", "Navigate to nine-day forecast page"
    )


@when('查看从今天起9天后的天气预报')
def when_check_ninth_day(nine_day_page, context, request):
    """
    Action: Get detailed weather forecast information for the 9th day
    Args:
        nine_day_page: Nine-day forecast page object
        context: Test context object for storing weather information
        request: pytest request object for logging
    """
    nine_day_temp, nine_day_rh, nine_day_date, nine_day_week_date, nine_day_psr, nine_day_description = nine_day_page.get_nine_day_weather_day_info()
    context['weather_info'] = {
        'temp': nine_day_temp,
        'rh': nine_day_rh,
        'date': nine_day_date,
        'week_date': nine_day_week_date,
        'psr': nine_day_psr,
        'description': nine_day_description
    }
    
    # Add detailed information to the test report
    request.node.add_report_section(
        "call", "When", 
        f"Retrieved weather info:\n"
        f"- Temperature: {nine_day_temp}\n"
        f"- Humidity: {nine_day_rh}\n"
        f"- Date: {nine_day_date}\n"
        f"- Day: {nine_day_week_date}\n"
        f"- UV Index: {nine_day_psr}\n"
        f"- Description: {nine_day_description}"
    )


@then('我应该看到的最后一个预报的日期是当前更新日期的九天后')
def then_verify_temperature(context, nine_day_page, request):
    """
    Verification: Confirm the correctness of the 9th day forecast date
    Args:
        context: Test context object containing weather information
        nine_day_page: Nine-day forecast page object
        request: pytest request object for logging
    """
    update_date = nine_day_page.get_update_date()
    # Convert string to datetime object
    date_obj = datetime.strptime(update_date, "%m月%d日")
    # Add 9 days
    new_date_obj = date_obj + timedelta(days=9)
    # Convert back to string
    new_date_str = new_date_obj.strftime("%m月%d日")
    nineth_date = "0" + context['weather_info']['date'] if len(context['weather_info']['date']) == 5 else context['weather_info']['date']
    
    # Add verification details to the test report
    request.node.add_report_section(
        "call", "Then",
        f"Date verification:\n"
        f"- Update date: {update_date}\n"
        f"- Expected 9th day: {new_date_str}\n"
        f"- Actual 9th day: {nineth_date}"
    )
    
    assert nineth_date == new_date_str, f"Date mismatch. Expected: {new_date_str}, Got: {nineth_date}"


@then('我可以获取到温度、湿度、紫外线信息和天气描述')
def then_verify_weather_info(context, request):
    """
    Verification: Confirm the completeness of weather forecast information
    Args:
        context: Test context object containing weather information
        request: pytest request object for logging
    """
    weather_info = context['weather_info']
    
    # Prepare verification results
    verification_results = {
        'Temperature': weather_info['temp'] is not None,
        'Humidity': weather_info['rh'] is not None,
        'Date': weather_info['date'] is not None,
        'Day of Week': weather_info['week_date'] is not None,
        'UV Index': weather_info['psr'] is not None,
        'Weather Description': weather_info['description'] is not None
    }
    
    # Add verification details to the test report
    report_content = "Weather information verification:\n"
    for field, result in verification_results.items():
        report_content += f"- {field}: {'✓' if result else '✗'}\n"
    request.node.add_report_section("call", "Then", report_content)
    
    # Perform assertions with descriptive messages
    assert weather_info['temp'] is not None, "Temperature information is missing"
    assert weather_info['rh'] is not None, "Humidity information is missing"
    assert weather_info['date'] is not None, "Date information is missing"
    assert weather_info['week_date'] is not None, "Day of week information is missing"
    assert weather_info['psr'] is not None, "UV index information is missing"
    assert weather_info['description'] is not None, "Weather description is missing"
