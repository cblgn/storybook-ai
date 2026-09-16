import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  use: { baseURL: 'http://127.0.0.1:5173', trace: 'retain-on-failure' },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'], defaultBrowserType: 'chromium' } },
  ],
  webServer: [
    {
      command: '../backend/.venv/bin/python -m uvicorn smoke_app:app --app-dir ../backend/tests --host 127.0.0.1 --port 8000',
      url: 'http://127.0.0.1:8000/api/health',
      reuseExistingServer: false,
    },
    { command: 'pnpm dev', url: 'http://127.0.0.1:5173', reuseExistingServer: false },
  ],
})
