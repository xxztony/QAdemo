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
