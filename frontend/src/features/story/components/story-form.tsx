import { useRef, useState, type FormEvent } from 'react'
import { LoaderCircle, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import type { StoryRequest } from '../types'

export function StoryForm({ loading, onGenerate }: {
  loading: boolean
  onGenerate: (request: StoryRequest) => Promise<void>
}) {
  const submitting = useRef(false)
  const [invalid, setInvalid] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (submitting.current || loading) return
    const data = new FormData(event.currentTarget)
    const text = (name: string) => String(data.get(name) ?? '').trim()
    const hero = text('hero')
    const setting = text('setting')
    const theme = text('theme')
    if (!hero || !setting || !theme) {
      setInvalid(true)
      return
    }
    setInvalid(false)
    submitting.current = true
    try {
      await onGenerate({
        child_name: text('child_name') || null,
        age: Number(data.get('age')),
        hero, setting, theme,
        duration_minutes: Number(data.get('duration_minutes')) as 3 | 5 | 10,
      })
    } finally {
      submitting.current = false
    }
  }

  return (
    <form onSubmit={handleSubmit} onInvalid={() => setInvalid(true)}>
      <fieldset disabled={loading} className="space-y-5">
        <legend className="sr-only">Les ingrédients de votre histoire</legend>
        <div className="grid grid-cols-[1fr_5.5rem] gap-4">
          <div className="space-y-2">
            <label htmlFor="child_name">Prénom <span className="font-normal text-muted-foreground">(facultatif)</span></label>
            <Input id="child_name" name="child_name" placeholder="Léa" maxLength={80} autoComplete="off" />
          </div>
          <div className="space-y-2">
            <label htmlFor="age">Âge</label>
            <Input id="age" name="age" type="number" min={3} max={12} step={1} defaultValue={7} required />
          </div>
        </div>
        <div className="space-y-2">
          <label htmlFor="hero">Le héros de l’aventure</label>
          <Input id="hero" name="hero" placeholder="Un petit dragon timide" maxLength={300} required />
        </div>
        <div className="space-y-2">
          <label htmlFor="setting">Un endroit extraordinaire</label>
          <Input id="setting" name="setting" list="settings" placeholder="Une forêt enchantée" maxLength={300} required />
          <datalist id="settings">
            {['Forêt enchantée', 'Espace', 'Île des pirates', 'Monde des dinosaures', 'Monde sous-marin', 'Château médiéval'].map(value => <option key={value} value={value} />)}
          </datalist>
        </div>
        <div className="space-y-2">
          <label htmlFor="theme">Une idée à explorer</label>
          <Input id="theme" name="theme" list="themes" placeholder="Apprendre à avoir confiance en soi" maxLength={300} required />
          <datalist id="themes">
            {['Le courage', 'L’amitié', 'Le partage', 'La patience', 'La peur du noir', 'La curiosité', 'La confiance en soi'].map(value => <option key={value} value={value} />)}
          </datalist>
        </div>
        <fieldset>
          <legend className="mb-2 text-sm font-semibold">Le temps d’un petit voyage</legend>
          <div className="grid grid-cols-3 gap-3">
            {[3, 5, 10].map(minutes => (
              <label key={minutes} className="cursor-pointer">
                <input className="peer sr-only" type="radio" name="duration_minutes" value={minutes} defaultChecked={minutes === 5} />
                <span className="block rounded-xl border border-input px-3 py-3 text-center font-medium text-muted-foreground peer-checked:border-primary peer-checked:bg-primary/5 peer-checked:text-primary peer-focus-visible:ring-2 peer-focus-visible:ring-ring">{minutes} min</span>
              </label>
            ))}
          </div>
          <p className="mt-2 text-xs text-muted-foreground">Durée de lecture approximative.</p>
        </fieldset>
        {invalid && <p role="alert" className="text-sm text-destructive">Complétez les champs obligatoires avec du texte et choisissez un âge entre 3 et 12 ans.</p>}
        <Button type="submit" size="lg" className="w-full" disabled={loading}>
          {loading ? <LoaderCircle className="animate-spin" aria-hidden /> : <Sparkles aria-hidden />}
          {loading ? 'Création en cours…' : "Créer l'histoire"}
        </Button>
      </fieldset>
    </form>
  )
}
