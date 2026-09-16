export interface StoryRequest {
  child_name: string | null
  age: number
  hero: string
  setting: string
  theme: string
  duration_minutes: 3 | 5 | 10
}

export interface StoryBook {
  title: string
  synopsis: string
  characters: { name: string; description: string; personality: string[] }[]
  scenes: { title: string; text: string }[]
  closing_sentence: string
}
