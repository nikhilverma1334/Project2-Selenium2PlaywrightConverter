const javaInput = document.getElementById('java-input');
const tsOutput = document.getElementById('ts-output');
const convertBtn = document.getElementById('convert-btn');
const btnText = convertBtn.querySelector('.btn-text');
const spinner = convertBtn.querySelector('.spinner');
const copyBtn = document.getElementById('copy-btn');
const clearBtn = document.getElementById('clear-btn');
const modelSelect = document.getElementById('model-select');

// Load default sample
javaInput.value = `package tests;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import java.time.Duration;
import java.util.List;

public class InstagramLoginTest {
    WebDriver driver;
    WebDriverWait wait;

    @BeforeClass
    public void setup() {
        driver = new ChromeDriver();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @Test
    public void testLogin() {
        driver.get("https://www.instagram.com/accounts/login/");
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.name("username"))).sendKeys("my_username");
        driver.findElement(By.name("password")).sendKeys("my_password");
        driver.findElement(By.cssSelector("button[type='submit']")).click();
    }

    @AfterClass
    public void teardown() {
        driver.quit();
    }
}`;

async function fetchModels() {
    try {
        const response = await fetch('/api/models');
        const data = await response.json();
        if (data.models) {
            modelSelect.innerHTML = data.models.map(m =>
                `<option value="${m.name}" ${m.name.includes('codellama') ? 'selected' : ''}>${m.name}</option>`
            ).join('');
        }
    } catch (e) {
        console.error("Failed to fetch models", e);
    }
}

async function convert() {
    const code = javaInput.value.trim();
    if (!code) return;

    // UI Loading State
    convertBtn.disabled = true;
    btnText.classList.add('hidden');
    spinner.classList.remove('hidden');
    tsOutput.textContent = "// Initializing stream...\n";
    tsOutput.style.color = "#9ca3af";

    try {
        const response = await fetch('/api/convert/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                source_code: code,
                model: modelSelect.value
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        tsOutput.textContent = ""; // Clear initial message
        tsOutput.style.color = "#e5e7eb";

        let fullContent = "";
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            fullContent += chunk;
            tsOutput.textContent = fullContent;

            // Auto-scroll to bottom
            const wrapper = tsOutput.parentElement.parentElement;
            wrapper.scrollTop = wrapper.scrollHeight;
        }

        // Clean up markdown if present
        if (fullContent.includes("```")) {
            const parts = fullContent.split("```");
            for (const part of parts) {
                if (part.includes("await") || part.includes("test") || part.includes("page.")) {
                    let cleaned = part.trim();
                    if (cleaned.startsWith("typescript")) cleaned = cleaned.replace(/^typescript\n?/, "");
                    if (cleaned.startsWith("javascript")) cleaned = cleaned.replace(/^javascript\n?/, "");
                    tsOutput.textContent = cleaned;
                    break;
                }
            }
        }

        if (window.Prism) {
            Prism.highlightElement(tsOutput);
        }

    } catch (error) {
        console.error("Conversion Error:", error);
        tsOutput.textContent = "// Error: " + error.message;
        tsOutput.style.color = "#ef4444";
    } finally {
        convertBtn.disabled = false;
        btnText.classList.remove('hidden');
        spinner.classList.add('hidden');
    }
}

// Event Listeners
convertBtn.addEventListener('click', (e) => {
    e.preventDefault();
    convert();
});

copyBtn.addEventListener('click', () => {
    const text = tsOutput.textContent;
    navigator.clipboard.writeText(text).then(() => {
        const originalText = copyBtn.textContent;
        copyBtn.textContent = "Copied!";
        setTimeout(() => copyBtn.textContent = originalText, 2000);
    });
});

clearBtn.addEventListener('click', () => {
    javaInput.value = "";
    javaInput.focus();
});

// Init
fetchModels();
