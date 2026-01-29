package com.example.tests;
import { test, beforeEach } from '@playwright/test';
import { page, Locator } from '@playwright/test';

class LoginTest {
    @beforeEach
    async setup() {
        await page.goto('https://example.com/login');
    }

    @test
    async testSuccessfulLogin() {
        const username = Locator('#username');
        await username.type('standard_user');

        const password = Locator('#password');
        await password.type('secret_sauce');

        const loginButton = page.locator('#login-button');
        await loginButton.click();

        const welcomeText = page.locator('.title').textContent();
        expect(welcomeText).toBe('Products');
    }
}