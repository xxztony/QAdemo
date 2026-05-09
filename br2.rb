Given(/^I (click|unclick) the (\w+)$/) do |_action, obj|
  smart_click(obj)
  wait_for_page_stable(timeout: duration)
end

Given(/^I click the (\w+) if exists$/) do |obj|
  clicked = click_if_exists(obj, timeout: 2)
  wait_for_page_stable(timeout: duration) if clicked
end

Given(/^I verify the (\w+) is displayed$/) do |obj|
  verify_object_displayed(obj)
end

Given(/^I verify the (\w+) is not displayed$/) do |obj|
  verify_object_not_displayed(obj)
end

Given(/^I verify the (\w+) is displayed br2$/) do |obj|
  verify_object_displayed_br2(obj)
end
