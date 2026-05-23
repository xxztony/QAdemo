def right_click_text_under_object_br2(value_key, obj, timeout: 10)
  expected_text = @bigmap[value_key]

  if expected_text.nil? || expected_text.to_s.strip.empty?
    fail "Cannot find value key in @bigmap: #{value_key}"
  end

  view = wait_for_browser2_object_displayed(obj, timeout: timeout)

  element = wait_for_child_displayed(
    view,
    ".//div[normalize-space(.)='#{expected_text}']",
    timeout: timeout
  )

  scroll_to_center(@driver2, element)

  @driver2.action
          .move_to(element)
          .pause(0.2)
          .context_click(element)
          .perform

  puts "Right clicked element text: #{element.text}"

  true
end

def wait_for_child_displayed(parent_element, child_xpath, timeout: DEFAULT_WAIT_TIMEOUT)
  wait = Selenium::WebDriver::Wait.new(
    timeout: timeout,
    interval: DEFAULT_WAIT_INTERVAL,
    ignore: RETRYABLE_FIND_ERRORS
  )

  wait.until do
    elements = parent_element.find_elements(:xpath, child_xpath)

    elements.find do |element|
      element.displayed? && element.enabled?
    rescue Selenium::WebDriver::Error::StaleElementReferenceError
      false
    end
  end
end

Given(/^I right click the element with text is (\w+) under (\w+) br2$/) do |value, obj|
  right_click_text_under_object_br2(value, obj)
end
