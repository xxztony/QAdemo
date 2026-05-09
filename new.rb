module UiHelpers
  DEFAULT_WAIT_TIMEOUT = 7
  DEFAULT_WAIT_INTERVAL = 0.2

  RETRYABLE_FIND_ERRORS = [
    Selenium::WebDriver::Error::NoSuchElementError,
    Selenium::WebDriver::Error::StaleElementReferenceError
  ].freeze

  RETRYABLE_CLICK_ERRORS = [
    Selenium::WebDriver::Error::StaleElementReferenceError,
    Selenium::WebDriver::Error::ElementClickInterceptedError,
    Selenium::WebDriver::Error::ElementNotInteractableError
  ].freeze

  def smart_click(obj, timeout: DEFAULT_WAIT_TIMEOUT)
    reset_window_perspective_if_needed(obj)

    xpath = object_xpath(obj)

    element = wait_for_element_displayed(@driver, xpath, timeout: timeout)
    scroll_to_center(@driver, element)

    begin
      click_by_strategy(obj, element)
    rescue *RETRYABLE_CLICK_ERRORS => e
      puts "Click failed for #{obj}, retry with fresh element and JS click. Error: #{e.class}"

      element = wait_for_element_displayed(@driver, xpath, timeout: timeout)
      scroll_to_center(@driver, element)
      js_click(@driver, element)
    end

    true
  end

  def click_if_exists(obj, timeout: 2)
    xpath = object_xpath(obj)

    element = wait_for_element_displayed(
      @driver,
      xpath,
      timeout: timeout,
      raise_error: false
    )

    return false if element.nil?
    return false unless element.enabled?

    scroll_to_center(@driver, element)

    begin
      click_by_strategy(obj, element)
    rescue *RETRYABLE_CLICK_ERRORS => e
      puts "Optional click failed for #{obj}, retry with fresh element and JS click. Error: #{e.class}"

      element = wait_for_element_displayed(
        @driver,
        xpath,
        timeout: timeout,
        raise_error: false
      )

      return false if element.nil?

      scroll_to_center(@driver, element)
      js_click(@driver, element)
    end

    true
  end

  def verify_object_displayed(obj, timeout: DEFAULT_WAIT_TIMEOUT)
    xpath = object_xpath(obj)

    begin
      element = wait_for_element_displayed(@driver, xpath, timeout: timeout)
    rescue Selenium::WebDriver::Error::TimeoutError
      if ie_browser?
        puts "Object not displayed in IE mode, refresh page and retry: #{obj}"

        @driver.navigate.refresh
        wait_for_page_stable(timeout: 10)

        element = wait_for_element_displayed(@driver, xpath, timeout: 10)
      else
        raise
      end
    end

    scroll_to_center(@driver, element)

    true
  end

  def verify_object_not_displayed(obj, timeout: DEFAULT_WAIT_TIMEOUT)
    xpath = object_xpath(obj)

    hidden = wait_for_element_not_displayed(@driver, xpath, timeout: timeout)

    unless hidden
      step "I capture the screen"
      fail "The object <#{obj}> is visible on the page"
    end

    true
  end

  def verify_object_displayed_br2(obj, timeout: DEFAULT_WAIT_TIMEOUT)
    element = wait_for_browser2_object_displayed(obj, timeout: timeout)
    scroll_to_center(Browser2, element)

    true
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

    current_user =
      if @bigmap.key?("current_login_user") && !@bigmap["current_login_user"].nil?
        @bigmap["current_login_user"]
      else
        "default_user"
      end

    @bigmap["current_login_user"] ||= current_user
    @bigmap["visit_list"][current_user] ||= {}
    @bigmap["visit_list"][current_user]["perspectives"] ||= {}

    already_visited = @bigmap["visit_list"][current_user]["perspectives"][obj]

    return if already_visited

    puts "First visit of #{obj} for #{current_user}, reset the window perspective"

    step "I reset the window perspective"

    @bigmap["visit_list"][current_user]["perspectives"][obj] = true
  end

  def object_xpath(obj)
    xpath = @object_hash[obj]

    if xpath.nil? || xpath.to_s.strip.empty?
      fail "Object '#{obj}' not found in @object_hash"
    end

    xpath
  end

  def wait_for_element_displayed(driver, xpath, timeout: DEFAULT_WAIT_TIMEOUT, raise_error: true)
    wait = Selenium::WebDriver::Wait.new(
      timeout: timeout,
      interval: DEFAULT_WAIT_INTERVAL,
      ignore: RETRYABLE_FIND_ERRORS
    )

    wait.until do
      element = driver.find_element(:xpath, xpath)
      element.displayed? ? element : nil
    end
  rescue Selenium::WebDriver::Error::TimeoutError
    raise if raise_error

    nil
  end

  def wait_for_element_not_displayed(driver, xpath, timeout: DEFAULT_WAIT_TIMEOUT)
    wait = Selenium::WebDriver::Wait.new(
      timeout: timeout,
      interval: DEFAULT_WAIT_INTERVAL,
      ignore: [
        Selenium::WebDriver::Error::StaleElementReferenceError
      ]
    )

    wait.until do
      elements = driver.find_elements(:xpath, xpath)
      elements.empty? || elements.none?(&:displayed?)
    end
  rescue Selenium::WebDriver::Error::TimeoutError
    false
  end

  def wait_for_browser2_object_displayed(obj, timeout: DEFAULT_WAIT_TIMEOUT)
    wait = Selenium::WebDriver::Wait.new(
      timeout: timeout,
      interval: DEFAULT_WAIT_INTERVAL,
      ignore: RETRYABLE_FIND_ERRORS
    )

    wait.until do
      element = Browser2.find_element(object_hash, @object_acc, obj)
      element.displayed? ? element : nil
    end
  rescue Selenium::WebDriver::Error::TimeoutError
    puts object_hash[obj] rescue nil
    fail "The object <#{obj}> does not exist or is not displayed on Browser2 page"
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
        js_click(@driver, element)
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

  def scroll_to_center(driver, element)
    driver.execute_script(
      "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
      element
    )
  rescue
    # ignore scroll failure for old browser / IE mode
  end

  def js_click(driver, element)
    driver.execute_script("arguments[0].click();", element)
  end

  def wait_for_page_stable(timeout: 5)
    wait = Selenium::WebDriver::Wait.new(
      timeout: timeout,
      interval: DEFAULT_WAIT_INTERVAL
    )

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

  def ie_browser?
    ENV["BROWSER"] == "ie" || ENV["BROWSER"] == "edge_ie"
  end
end
