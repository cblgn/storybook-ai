import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import type { StoryBook } from './features/story/types'

const story: StoryBook = {
  title: 'Le petit dragon courageux',
  synopsis: 'Un dragon découvre le courage.',
  characters: [{ name: 'Zéphyr', description: 'Un dragon bleu', personality: ['curieux'] }],
  scenes: [{ title: 'Dans la forêt', text: 'Zéphyr retrouve son ami dans la clairière.' }],
  closing_sentence: 'Il s’endort, rassuré et heureux.',
}

async function fillForm(user: ReturnType<typeof userEvent.setup>) {
  await user.type(screen.getByLabelText(/Prénom/), 'Léa')
  await user.type(screen.getByLabelText('Le héros de l’aventure'), '  un dragon  ')
  await user.type(screen.getByLabelText('Un endroit extraordinaire'), 'forêt enchantée')
  await user.type(screen.getByLabelText('Une idée à explorer'), 'le courage')
}

describe('story creation', () => {
  it('loads health, submits the typed request and renders the complete story', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(Response.json({ status: 'ok' }))
      .mockResolvedValueOnce(Response.json(story))
    vi.stubGlobal('fetch', fetchMock)
    const user = userEvent.setup()
    render(<App />)

    expect(screen.getByText('Tout commence par une idée')).toBeInTheDocument()
    expect(await screen.findByText('Service connecté')).toBeInTheDocument()
    await fillForm(user)
    await user.click(screen.getByRole('button', { name: "Créer l'histoire" }))

    expect(await screen.findByRole('heading', { name: story.title })).toBeInTheDocument()
    expect(screen.getByText(story.synopsis)).toBeInTheDocument()
    expect(screen.getByText(story.scenes[0].text)).toBeInTheDocument()
    expect(screen.getByText(story.closing_sentence)).toBeInTheDocument()
    const [url, options] = fetchMock.mock.calls[1] as [string, RequestInit]
    expect(url).toBe('/api/stories')
    expect(options.method).toBe('POST')
    expect(JSON.parse(options.body as string)).toEqual({
      child_name: 'Léa', age: 7, hero: 'un dragon', setting: 'forêt enchantée',
      theme: 'le courage', duration_minutes: 5,
    })
  })

  it('rejects whitespace-only ingredients before sending a story request', async () => {
    const fetchMock = vi.fn().mockResolvedValue(Response.json({ status: 'ok' }))
    vi.stubGlobal('fetch', fetchMock)
    const user = userEvent.setup()
    render(<App />)
    await screen.findByText('Service connecté')
    await fillForm(user)
    await user.clear(screen.getByLabelText('Le héros de l’aventure'))
    await user.type(screen.getByLabelText('Le héros de l’aventure'), '   ')
    await user.click(screen.getByRole('button', { name: "Créer l'histoire" }))
    expect(screen.getByRole('alert')).toHaveTextContent('Complétez les champs')
    expect(fetchMock).toHaveBeenCalledTimes(1)
  })

  it('blocks duplicate submissions while pending and lets the user retry after failure', async () => {
    let finish!: (response: Response) => void
    const pending = new Promise<Response>(resolve => { finish = resolve })
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(Response.json({ status: 'ok' }))
      .mockReturnValueOnce(pending)
      .mockResolvedValueOnce(Response.json(story))
    vi.stubGlobal('fetch', fetchMock)
    const user = userEvent.setup()
    render(<App />)
    await screen.findByText('Service connecté')
    await fillForm(user)
    await user.click(screen.getByRole('button', { name: "Créer l'histoire" }))
    const pendingButton = screen.getByRole('button', { name: 'Création en cours…' })
    expect(pendingButton).toBeDisabled()
    expect(screen.getByLabelText('Le héros de l’aventure')).toBeDisabled()
    await user.click(pendingButton)
    expect(fetchMock).toHaveBeenCalledTimes(2)

    finish(Response.json({ detail: 'private-provider-error' }, { status: 503 }))
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('Vous pouvez réessayer'))
    expect(screen.queryByText('private-provider-error')).not.toBeInTheDocument()
    expect(screen.getByLabelText('Le héros de l’aventure')).toHaveValue('  un dragon  ')
    await user.click(screen.getByRole('button', { name: "Créer l'histoire" }))
    expect(await screen.findByRole('heading', { name: story.title })).toBeInTheDocument()
    expect(fetchMock).toHaveBeenCalledTimes(3)
  })
})
