describe('Login', () => {
  // Base test case for logging into the web application
  const Login = () => async() => {
    await page.goto(`http://localhost:8000/user/login`);
    await page.waitForSelector('#username', {timeout: 60000})
    await page.type('#username', 'admin');
    await page.type('#password', 'ant.design');
    await page.waitForNavigation();
    await page.click('button[type="button"]');
  }

  // Test Case for Posture AI page
  it('Posture_AI', async() => {
    Login();

    await page.goto(`http://localhost:8000/Posture_AI`);
    await page.waitForSelector('#page_title', {
      timeout: 2000
    });

    // Check Page Title
    const haveText = await page.evaluate(
      () => document.getElementById('page_title').textContent.includes("List of Videos"));
    expect(haveText).toBeTruthy();
  })
});