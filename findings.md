# Findings

## Research & Discoveries
- **Project Goal**: Selenium Java (TestNG) to Playwright (JS/TS) Converter.
- **Input Method**: UI-based code entry (Selenium Java).
- **Output Method**: Local directory file creation + UI display.
- **Conversion focus**: TestNG Selenium Java -> Playwright JS/TS.
- **Strategy**: Prioritize readability over strict 1:1 mapping.

### Mapping Patterns Found:
| Selenium/TestNG | Playwright (JS/TS) |
| :--- | :--- |
| `@Test` | `test('name', async ({ page }) => { ... })` |
| `@BeforeMethod` | `test.beforeEach(async ({ page }) => { ... })` |
| `driver.get(url)` | `await page.goto(url)` |
| `findElement(By.id("x"))` | `page.locator('#x')` |
| `element.sendKeys("val")` | `await element.fill('val')` |
| `element.click()` | `await element.click()` |
| `WebDriverWait` | Auto-waiting / `expect(..).toBeVisible()` |
| `Assert.assertEquals` | `expect(..).toBe(..)` |

## Constraints
- Must handle TestNG annotations (@Test, @BeforeMethod, etc.).
- Must handle Selenium WebDriver commands (find_element, click, send_keys, etc.).
- UI is required for input and output display.
- **Language Shift**: Java (Synchronous) to JS/TS (Asynchronous/Await).
