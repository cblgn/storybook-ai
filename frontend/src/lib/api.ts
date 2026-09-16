export async function apiRequest<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    signal: options?.signal ?? AbortSignal.timeout(190_000),
  })
  if (!response.ok) {
    // Provider and server responses must never become user-facing error text.
    throw new Error('La requête a échoué.')
  }
  return response.json() as Promise<T>
}
