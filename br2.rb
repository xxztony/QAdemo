Given(/^I verify the (\w+) is displayed br2$/) do |obj|
  wait = Selenium::WebDriver::Wait.new(
    timeout: 7,
    interval: 0.2,
    ignore: [
      Selenium::WebDriver::Error::NoSuchElementError,
      Selenium::WebDriver::Error::StaleElementReferenceError
    ]
  )

  begin
    element = wait.until do
      el = Browser2.find_element(object_hash, @object_acc, obj)
      el.displayed? ? el : nil
    end

    begin
      Browser2.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
        element
      )
    rescue
      # ignore scroll failure
    end

    puts "Verified object is displayed in Browser2: #{obj}"

  rescue Selenium::WebDriver::Error::TimeoutError
    puts object_hash[obj] rescue nil
    fail "The object <#{obj}> does not exist or is not displayed on Browser2 page"
  end
end


module UiHelpers
  def wait_for_object_displayed_in_browser2(obj, timeout: 7)
    wait = Selenium::WebDriver::Wait.new(
      timeout: timeout,
      interval: 0.2,
      ignore: [
        Selenium::WebDriver::Error::NoSuchElementError,
        Selenium::WebDriver::Error::StaleElementReferenceError
      ]
    )

    wait.until do
      element = Browser2.find_element(object_hash, @object_acc, obj)
      element.displayed? ? element : nil
    end
  rescue Selenium::WebDriver::Error::TimeoutError
    puts object_hash[obj] rescue nil
    fail "The object <#{obj}> does not exist or is not displayed on Browser2 page"
  end

  def scroll_to_center(driver, element)
    driver.execute_script(
      "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
      element
    )
  rescue
    # ignore scroll failure
  end
end


require_relative "ui_helpers"

World(UiHelpers)

Given(/^I verify the (\w+) is displayed br2$/) do |obj|
  element = wait_for_object_displayed_in_browser2(obj, timeout: 7)
  scroll_to_center(Browser2, element)

  puts "Verified object is displayed in Browser2: #{obj}"
end
