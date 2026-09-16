import { useEffect, useState } from 'react'
import { BookOpen, LoaderCircle, Moon, Sparkles, Stars } from 'lucide-react'
import { apiRequest } from '@/lib/api'
import { StoryForm } from '@/features/story/components/story-form'
import { StoryResult } from '@/features/story/components/story-result'
import { generateStory } from '@/features/story/api'
import type { StoryBook, StoryRequest } from '@/features/story/types'

type GenerationState =
  | { status: 'initial' | 'loading' | 'error' }
  | { status: 'success'; story: StoryBook }

export default function App() {
  const [state, setState] = useState<GenerationState>({ status: 'initial' })
  const [health, setHealth] = useState<'checking' | 'ok' | 'error'>('checking')

  useEffect(() => {
    const controller = new AbortController()
    apiRequest<{ status: string }>('/health', {
      signal: AbortSignal.any([controller.signal, AbortSignal.timeout(5000)]),
    }).then(result => setHealth(result.status === 'ok' ? 'ok' : 'error'))
      .catch(() => { if (!controller.signal.aborted) setHealth('error') })
    return () => controller.abort()
  }, [])

  async function handleGenerate(request: StoryRequest) {
    setState({ status: 'loading' })
    try {
      const story = await generateStory(request)
      setState({ status: 'success', story })
      setHealth('ok')
    } catch {
      setState({ status: 'error' })
    }
  }

  return (
    <div className="min-h-screen px-5 py-7 sm:px-8 lg:px-12">
      <header className="mx-auto flex max-w-6xl items-center justify-between border-b border-border pb-6">
        <a href="/" className="flex items-center gap-3 text-lg font-bold tracking-tight">
          <span className="rounded-xl bg-primary p-2.5 text-primary-foreground"><BookOpen size={21} aria-hidden /></span>
          Storybook <span className="font-normal text-primary">AI</span>
        </a>
        <span className="flex items-center gap-2 text-xs text-muted-foreground"><Moon size={15} aria-hidden /> Le rendez-vous des petits rêveurs</span>
      </header>
      <main className="mx-auto max-w-6xl">
        <div className="py-10 text-center sm:py-14">
          <p className="mb-4 text-xs font-bold tracking-[0.22em] text-primary uppercase">Petites histoires, grands rêves</p>
          <h1 className="font-story text-4xl leading-tight tracking-tight sm:text-5xl">Une histoire rien que pour vous <span className="text-primary">✧</span></h1>
          <p className="mx-auto mt-4 max-w-xl leading-relaxed text-muted-foreground">Un héros, un peu d’imagination… et un moment à partager.<br className="hidden sm:block" /> Composez une aventure qui ressemble à votre enfant.</p>
        </div>
        <div className="grid items-start gap-7 lg:grid-cols-[370px_1fr]">
          <section aria-labelledby="form-title" className="rounded-3xl border border-border bg-card p-6 shadow-sm sm:p-7">
            <div className="mb-6 flex gap-3">
              <Sparkles className="mt-1 text-primary" size={21} aria-hidden />
              <div><h2 id="form-title" className="font-story text-2xl">À vous d’imaginer</h2><p className="mt-1 text-sm text-muted-foreground">Les ingrédients d’une belle histoire.</p></div>
            </div>
            <StoryForm loading={state.status === 'loading'} onGenerate={handleGenerate} />
          </section>
          <section aria-label="Votre histoire" aria-busy={state.status === 'loading'} className="min-h-[590px] rounded-3xl border border-border bg-card p-7 sm:p-10">
            {state.status === 'success' ? <StoryResult story={state.story} /> : (
              <div className="flex min-h-[500px] flex-col items-center justify-center text-center">
                <div className="mb-7 grid size-24 place-items-center rounded-full bg-accent text-primary">
                  {state.status === 'loading' ? <LoaderCircle size={38} className="animate-spin" aria-hidden /> : <Stars size={40} strokeWidth={1.2} aria-hidden />}
                </div>
                <div role={state.status === 'error' ? 'alert' : 'status'}>
                  <h2 className="font-story text-3xl">{state.status === 'loading' ? 'Création de votre histoire…' : state.status === 'error' ? 'Un petit contretemps…' : 'Tout commence par une idée'}</h2>
                  <p className="mx-auto mt-4 max-w-sm text-sm leading-7 text-muted-foreground">{state.status === 'loading'
                    ? 'Les mots prennent vie. Votre aventure sera prête dans quelques instants.'
                    : state.status === 'error'
                      ? "Impossible de créer l'histoire pour le moment. Vous pouvez réessayer : vos idées sont toujours dans le formulaire."
                      : 'Un dragon timide, une forêt lumineuse, une amitié inattendue… Votre prochaine histoire vous attend ici.'}</p>
                </div>
                {state.status === 'initial' && <span className="mt-8 rounded-full border border-border px-4 py-2 text-xs text-muted-foreground">À lire ensemble, à rêver longtemps</span>}
              </div>
            )}
          </section>
        </div>
        <footer className="flex flex-wrap items-center justify-between gap-3 py-8 text-xs text-muted-foreground">
          <p>Imaginé avec l’IA, partagé avec amour.</p>
          <p role="status">{health === 'checking' ? 'Connexion en cours…' : health === 'ok' ? 'Service connecté' : 'Service indisponible — vérifiez que le serveur est démarré.'}</p>
        </footer>
      </main>
    </div>
  )
}
