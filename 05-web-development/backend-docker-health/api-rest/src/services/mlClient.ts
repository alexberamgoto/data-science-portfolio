import fetch from 'node-fetch';
import { config } from '../config';

export async function analyzeHealthData(input: any) {
  const res = await fetch(`${config.ml.baseUrl}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input)
  });
  if (!res.ok) throw new Error(`ML service error: ${res.status}`);
  return await res.json();
}
