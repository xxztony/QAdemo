Feature: 9th day's weather forecast
  Scenario: 检查第9天的天气预报信息
    Given 我在天气预报应用的九天预报页面
    When 查看从今天起9天后的天气预报
    Then 我应该看到的最后一个预报的日期是当前更新日期的九天后
    And 我可以获取到温度、湿度、紫外线信息和天气描述

