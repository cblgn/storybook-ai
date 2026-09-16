import type { StoryBook } from '../types'

export function StoryResult({ story }: { story: StoryBook }) {
  return (
    <article aria-labelledby="story-title" className="mx-auto max-w-2xl">
      <p className="mb-4 text-xs font-bold tracking-[0.2em] text-primary uppercase">Il était une fois…</p>
      <h2 id="story-title" className="font-story text-3xl leading-tight sm:text-4xl">{story.title}</h2>
      <p className="mt-5 border-b border-border pb-8 text-base leading-relaxed text-muted-foreground">{story.synopsis}</p>
      {story.scenes.map((scene, index) => (
        <section key={index} className="mt-8">
          <h3 className="font-story text-2xl">{scene.title}</h3>
          <p className="mt-4 whitespace-pre-line font-story text-lg leading-[1.9]">{scene.text}</p>
        </section>
      ))}
      <p className="mt-10 rounded-2xl bg-accent p-6 font-story text-lg leading-relaxed italic">{story.closing_sentence}</p>
    </article>
  )
}
