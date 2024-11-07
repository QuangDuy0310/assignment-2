1. Install WebDriver
Selenium requires browser-specific drivers:
Chrome: Download ChromeDriver
Link: https://developer.chrome.com/docs/chromedriver/downloads
Firefox: Download GeckoDriver
2. Install Selenium in your Python/Java Project
If using Python: pip install selenium

If using Maven for Java, add the following to your pom.xml:
<dependency>
<groupId>org.seleniumhq.selenium</groupId>
<artifactId>selenium-java</artifactId>
<version>4.0.0</version>
</dependency>

Add the WebDriver to your system path or specify its location in the test script.

For a more visual representation of the test results, you can generate HTML reports using the
pytest-html plugin.
1. Install pytest-html
pip install pytest-html
2. Run tests with HTML report generation
pytest --html=report.html
3. Open the HTML report
After the tests finish running, a report.html file will be generated.
Open it in any web browser to see a detailed, color-coded report of your test results.