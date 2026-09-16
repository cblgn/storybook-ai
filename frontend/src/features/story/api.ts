import { apiRequest } from '@/lib/api'
import type { StoryBook, StoryRequest } from './types'

export function generateStory(request: StoryRequest) {
  return apiRequest<StoryBook>('/stories', { method: 'POST', body: JSON.stringify(request) })
}
