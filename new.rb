Given(/^I (click|unclick) the (.*)$/) do |action, obj|
  reset_window_perspective_if_needed(obj)

  xpath = @object_hash[obj]
  raise "Object '#{obj}' not found in @object_hash" if xpath.nil? || xpath.empty?

  smart_click(obj, xpath)

  # 原来的 sleep duration 不建议完全保留
  # 这里改成“短暂等页面稳定”，不是固定傻等
  wait_for_page_stable(timeout: duration)
end

def reset_window_perspective_if_needed(obj)
  perspective_objects = [
    "collateral_perspective",
    "treasury_perspective",
    "trading_perspective",
    "settlement_perspective",
    "referenceData_perspective",
    "risk_perspective",
    "positions_perspective",
    "reporting_perspective",
    "reportDesigner_perspective"
  ]

  return unless perspective_objects.include?(obj)

  @bigmap ||= {}
  @bigmap["visit_list"] ||= {}
  @bigmap["current_login_user"] ||= "default_user"
  @bigmap["visit_list"][@bigmap["current_login_user"]] ||= {}
  @bigmap["visit_list"][@bigmap["current_login_user"]]["perspectives"] ||= {}

  already_visited =
    @bigmap["visit_list"][@bigmap["current_login_user"]]["perspectives"][obj]

  return if already_visited

  puts "First visit of #{obj} for #{@bigmap['current_login_user']}, reset the window perspective"
  step "I reset the window perspective"

  @bigmap["visit_list"][@bigmap["current_login_user"]]["perspectives"][obj] = true
end

def smart_click(obj, xpath, timeout: 10)
  wait = Selenium::WebDriver::Wait.new(
    timeout: timeout,
    interval: 0.2,
    ignore: [
      Selenium::WebDriver::Error::NoSuchElementError,
      Selenium::WebDriver::Error::StaleElementReferenceError,
      Selenium::WebDriver::Error::ElementClickInterceptedError,
      Selenium::WebDriver::Error::ElementNotInteractableError
    ]
  )

  element = wait.until do
    el = @driver.find_element(:xpath, xpath)
    scroll_to_center(el)

    if el.displayed? && el.enabled?
      el
    else
      nil
    end
  end

  click_by_strategy(obj, element)

rescue Selenium::WebDriver::Error::StaleElementReferenceError,
       Selenium::WebDriver::Error::ElementClickInterceptedError,
       Selenium::WebDriver::Error::ElementNotInteractableError,
       Selenium::WebDriver::Error::NoSuchElementError => e

  puts "Normal click failed for #{obj}, retry with fresh element and JS click. Error: #{e.class}"

  element = @driver.find_element(:xpath, xpath)
  scroll_to_center(element)
  js_click(element)
end

def click_by_strategy(obj, element)
  if use_action_click?(obj)
    @driver.action.move_to(element).click.perform
  elsif use_native_click?(obj)
    element.click
  else
    begin
      element.click
    rescue Selenium::WebDriver::Error::ElementClickInterceptedError,
           Selenium::WebDriver::Error::ElementNotInteractableError
      js_click(element)
    end
  end
end

def use_action_click?(obj)
  action_click_objects = [
    "navBar_LMES",
    "tab_LodgeInstructionConfirmPrintedWarrants",
    "accept_button_LMES"
  ]

  action_click_objects.any? { |key| obj.include?(key) }
end

def use_native_click?(obj)
  native_click_objects = [
    "ExcludeSearchCriteria",
    "IncludesSearchCriteria",
    "view_file_navBar_LMES",
    "excludeSearchCriteria_option_warrantSearchCollapsiblePanel_LMES"
  ]

  native_click_objects.any? { |key| obj.include?(key) }
end

def scroll_to_center(element)
  @driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
    element
  )
end

def js_click(element)
  @driver.execute_script("arguments[0].click();", element)
end

def wait_for_page_stable(timeout: 5)
  wait = Selenium::WebDriver::Wait.new(timeout: timeout, interval: 0.2)

  wait.until do
    document_ready? && no_visible_loading_mask?
  end
rescue Selenium::WebDriver::Error::TimeoutError
  puts "Page stable wait timeout, continue execution"
end

def document_ready?
  @driver.execute_script("return document.readyState") == "complete"
rescue
  true
end

def no_visible_loading_mask?
  script = <<~JS
    const selectors = [
      '.loading',
      '.spinner',
      '.gwt-PopupPanelGlass',
      '.gwt-DialogBox',
      '.x-mask',
      '.modal-backdrop',
      '[aria-busy="true"]'
    ];

    return selectors.every(selector => {
      return Array.from(document.querySelectorAll(selector)).every(el => {
        const style = window.getComputedStyle(el);

        return style.display === 'none' ||
               style.visibility === 'hidden' ||
               style.opacity === '0' ||
               el.offsetParent === null;
      });
    });
  JS

  @driver.execute_script(script)
rescue
  true
end


Given(/^I click the (\w+) if exists$/) do |obj|
  xpath = object_xpath(obj)

  clicked = click_if_exists(obj, xpath, timeout: 2)

  if clicked
    puts "Clicked optional object: #{obj}"
    wait_for_page_stable(timeout: duration)
  else
    puts "Optional object not found or not clickable, continue: #{obj}"
  end
end


Given(/^I verify the (\w+) is displayed$/) do |obj|
  xpath = object_xpath(obj)

  element = nil

  begin
    element = wait_for_element_displayed(xpath, timeout: 6)
  rescue Selenium::WebDriver::Error::TimeoutError
    if ie_browser?
      puts "Object not displayed in IE mode, refresh page and retry: #{obj}"
      @driver.navigate.refresh
      wait_for_page_stable(timeout: 10)
      element = wait_for_element_displayed(xpath, timeout: 10)
    else
      raise
    end
  end

  scroll_to_center(element)

  puts "Verified object is displayed: #{obj}"
end

Given(/^I verify the (\w+) is not displayed$/) do |obj|
  xpath = object_xpath(obj)

  hidden = wait_for_element_not_displayed(xpath, timeout: 6)

  unless hidden
    step "I capture the screen"
    raise "The object <#{obj}> is visible on the page"
  end

  puts "Verified object is not displayed: #{obj}"
end

def object_xpath(obj)
  xpath = @object_hash[obj]

  if xpath.nil? || xpath.to_s.strip.empty?
    raise "Object '#{obj}' not found in @object_hash"
  end

  xpath
end


def wait_for_element_displayed(xpath, timeout: 6, raise_error: true)
  wait = Selenium::WebDriver::Wait.new(
    timeout: timeout,
    interval: 0.2,
    ignore: [
      Selenium::WebDriver::Error::NoSuchElementError,
      Selenium::WebDriver::Error::StaleElementReferenceError
    ]
  )

  wait.until do
    element = @driver.find_element(:xpath, xpath)

    if element.displayed?
      element
    else
      nil
    end
  end

rescue Selenium::WebDriver::Error::TimeoutError
  raise if raise_error

  nil
end

def wait_for_element_not_displayed(xpath, timeout: 6)
  wait = Selenium::WebDriver::Wait.new(
    timeout: timeout,
    interval: 0.2,
    ignore: [
      Selenium::WebDriver::Error::StaleElementReferenceError
    ]
  )

  wait.until do
    elements = @driver.find_elements(:xpath, xpath)

    if elements.empty?
      true
    else
      elements.none? { |element| element.displayed? }
    end
  end

rescue Selenium::WebDriver::Error::TimeoutError
  false
end

def scroll_to_center(element)
  @driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
    element
  )
rescue
  # Some old IE / edge_ie pages may not support this well. Ignore scroll failure.
end


def click_by_strategy(obj, element)
  if use_action_click?(obj)
    @driver.action.move_to(element).click.perform
  elsif use_native_click?(obj)
    element.click
  else
    begin
      element.click
    rescue Selenium::WebDriver::Error::ElementClickInterceptedError,
           Selenium::WebDriver::Error::ElementNotInteractableError
      js_click(element)
    end
  end
end

def use_action_click?(obj)
  action_click_objects = [
    "navBar_LMES",
    "tab_LodgeInstructionConfirmPrintedWarrants",
    "accept_button_LMES"
  ]

  action_click_objects.any? { |key| obj.include?(key) }
end

def use_native_click?(obj)
  native_click_objects = [
    "ExcludeSearchCriteria",
    "IncludesSearchCriteria",
    "view_file_navBar_LMES",
    "excludeSearchCriteria_option_warrantSearchCollapsiblePanel_LMES"
  ]

  native_click_objects.any? { |key| obj.include?(key) }
end

def js_click(element)
  @driver.execute_script("arguments[0].click();", element)
end

def ie_browser?
  ENV["BROWSER"] == "ie" || ENV["BROWSER"] == "edge_ie"
end


def wait_for_page_stable(timeout: 5)
  wait = Selenium::WebDriver::Wait.new(timeout: timeout, interval: 0.2)

  wait.until do
    document_ready? && no_visible_loading_mask?
  end
rescue Selenium::WebDriver::Error::TimeoutError
  puts "Page stable wait timeout, continue execution"
end

def document_ready?
  @driver.execute_script("return document.readyState") == "complete"
rescue
  true
end

def no_visible_loading_mask?
  script = <<~JS
    const selectors = [
      '.loading',
      '.spinner',
      '.gwt-PopupPanelGlass',
      '.gwt-DialogBox',
      '.x-mask',
      '.modal-backdrop',
      '[aria-busy="true"]'
    ];

    return selectors.every(selector => {
      return Array.from(document.querySelectorAll(selector)).every(el => {
        const style = window.getComputedStyle(el);

        return style.display === 'none' ||
               style.visibility === 'hidden' ||
               style.opacity === '0' ||
               el.offsetParent === null;
      });
    });
  JS

  @driver.execute_script(script)
rescue
  true
end




Given(/^I click the (\w+) if exists$/) do |obj|
  xpath = object_xpath(obj)

  clicked = click_if_exists(obj, xpath, timeout: 2)

  if clicked
    puts "Clicked optional object: #{obj}"
    wait_for_page_stable(timeout: duration)
  else
    puts "Optional object not found or not clickable, continue: #{obj}"
  end
end


Given(/^I verify the (\w+) is displayed$/) do |obj|
  xpath = object_xpath(obj)

  element = nil

  begin
    element = wait_for_element_displayed(xpath, timeout: 6)
  rescue Selenium::WebDriver::Error::TimeoutError
    if ie_browser?
      puts "Object not displayed in IE mode, refresh page and retry: #{obj}"
      @driver.navigate.refresh
      wait_for_page_stable(timeout: 10)
      element = wait_for_element_displayed(xpath, timeout: 10)
    else
      raise
    end
  end

  scroll_to_center(element)

  puts "Verified object is displayed: #{obj}"
end


Given(/^I verify the (\w+) is not displayed$/) do |obj|
  xpath = object_xpath(obj)

  hidden = wait_for_element_not_displayed(xpath, timeout: 6)

  unless hidden
    step "I capture the screen"
    raise "The object <#{obj}> is visible on the page"
  end

  puts "Verified object is not displayed: #{obj}"
end
