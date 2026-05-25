def blank_page?

  body_text = @driver.execute_script("return document.body ? document.body.innerText.trim() : ''")

  body_html = @driver.execute_script("return document.body ? document.body.innerHTML.trim() : ''")

  ready_state = @driver.execute_script("return document.readyState")

  current_url = @driver.current_url

  puts "Blank page check: readyState=#{ready_state}, url=#{current_url}, body_text_length=#{body_text.length}, body_html_length=#{body_html.length}"

  return true if current_url.nil? || current_url.strip.empty?

  return true if current_url.start_with?("data:")

  return true if body_text.empty? && body_html.length < 100

  false

rescue => e

  puts "Blank page check failed: #{e.class} - #{e.message}"

  false

en
