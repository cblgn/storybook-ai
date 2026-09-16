import { expect, test, type Page } from '@playwright/test'

async function fillStory(page: Page) {
  await page.getByLabel('Prénom').fill('Léa')
  await page.getByLabel('Le héros').fill('un petit dragon timide')
  await page.getByLabel('Un endroit').fill('forêt enchantée')
  await page.getByLabel('Une idée').fill('prendre confiance en soi')
}

test('health, validation and story generation through FastAPI', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByText('Service connecté', { exact: true })).toBeVisible()
  await page.getByRole('button', { name: "Créer l'histoire" }).click()
  await expect(page.getByRole('alert')).toContainText('Complétez les champs')
  await fillStory(page)
  await expect(page.getByRole('radio', { name: '5 min', exact: true })).toBeChecked()
  await page.getByText('3 min', { exact: true }).click()
  await expect(page.getByRole('radio', { name: '3 min', exact: true })).toBeChecked()
  const requestPromise = page.waitForRequest(request => request.url().endsWith('/api/stories'))
  await page.getByRole('button', { name: "Créer l'histoire" }).click()
  expect((await requestPromise).postDataJSON()).toEqual({
    child_name: 'Léa', age: 7, hero: 'un petit dragon timide',
    setting: 'forêt enchantée', theme: 'prendre confiance en soi', duration_minutes: 3,
  })
  await expect(page.getByRole('heading', { name: 'Zéphyr et la lumière des bois' })).toBeVisible()
  await expect(page.getByText('Ce soir-là, Zéphyr')).toBeVisible()
  await expect(page.getByRole('button', { name: "Créer l'histoire" })).toBeEnabled()
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBeTruthy()
})

test('loading blocks duplicate requests, failure preserves inputs and allows retry', async ({ page }) => {
  let release: () => void = () => {}
  const pending = new Promise<void>(resolve => { release = resolve })
  let requests = 0
  await page.route('**/api/stories', async route => {
    requests++
    await pending
    await route.fulfill({ status: 503, json: { detail: 'private-provider-error' } })
  })
  await page.goto('/')
  await fillStory(page)
  await page.getByRole('button', { name: "Créer l'histoire" }).click()
  await expect(page.getByRole('button', { name: 'Création en cours' })).toBeDisabled()
  await expect(page.getByRole('heading', { name: 'Création de votre histoire' })).toBeVisible()
  await expect(page.getByLabel('Le héros')).toBeDisabled()
  expect(requests).toBe(1)
  release()
  await expect(page.getByRole('alert')).toContainText("Impossible de créer l'histoire")
  await expect(page.getByText('private-provider-error')).toHaveCount(0)
  await expect(page.getByLabel('Le héros')).toHaveValue('un petit dragon timide')
  await page.unroute('**/api/stories')
  await page.getByRole('button', { name: "Créer l'histoire" }).click()
  await expect(page.getByRole('heading', { name: 'Zéphyr et la lumière des bois' })).toBeVisible()
})
