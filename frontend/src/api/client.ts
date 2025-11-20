import { Platform } from 'react-native';

const DEFAULT_BASE = Platform.select({
  android: 'http://10.0.2.2:8000',
  ios: 'http://localhost:8000',
  default: 'http://localhost:8000',
});

export const API_BASE_URL = DEFAULT_BASE!;

async function request<T>(path: string, options: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status} ${res.statusText}: ${text}`);
  }
  return (await res.json()) as T;
}

export const api = {
  startJourney: (body: unknown) =>
    request<{ journey_id: string; started_at: string }>(`/journey/start`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  trackJourney: (body: unknown) =>
    request<{ ok: boolean; eta_iso?: string }>(`/journey/track`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  stopJourney: (body: unknown) =>
    request<{ ok: boolean; ended_at: string }>(`/journey/stop`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  suggestBreak: (body: unknown) =>
    request<{ should_take_break: boolean; reason?: string }>(`/breaks/suggest`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  searchHotels: (body: unknown) =>
    request<{ hotels: any[] }>(`/hotels/nearby`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  triggerSOS: (body: unknown) =>
    request<{ ok: boolean; alert_id: string }>(`/sos/alert`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  submitReview: (body: unknown) =>
    request<{ id: string }>(`/reviews/`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),
};


