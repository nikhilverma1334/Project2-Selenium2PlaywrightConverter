## Overview
This SOP defines how the system converts specific Selenium/TestNG patterns into Playwright equivalent code using **Ollama (codellama)**.

## 1. LLM-First Strategy
- **Engine**: Ollama API (`/api/generate`)
- **Model**: `codellama`
- **Reasoning**: Instead of rigid regex mapping, we use a code-specialized LLM to handle diverse Java syntax and TestNG patterns.
- **Input**: Java Class with `@Test` annotations.
- **Output**: A `.test.ts` or `.test.js` file.
- **Rule**: Wrap `@Test` methods into `test('description', async ({ page }) => { ... })`.

## 2. Annotations Mapping
- `@BeforeMethod` -> `test.beforeEach(async ({ page }) => { ... })`
- `@AfterMethod` -> `test.afterEach(async ({ page }) => { ... })`
- `@BeforeClass` -> `test.beforeAll(async () => { ... })`

## 3. Selector and Action Mapping
- `driver.findElement(By.id("id"))` -> `page.locator('#id')`
- `driver.findElement(By.name("name"))` -> `page.locator('[name="name"]')`
- `element.sendKeys("text")` -> `await element.fill("text")`
- `element.click()` -> `await element.click()`

## 4. Assertions
- `Assert.assertEquals(actual, expected)` -> `expect(actual).toBe(expected)`
- `Assert.assertTrue(condition)` -> `expect(condition).toBeTruthy()`

## 5. Async Handling
- Since Java is synchronous, every browser action in Playwright must be prefixed with `await`.
