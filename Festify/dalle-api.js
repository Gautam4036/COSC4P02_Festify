// DALL-E API Integration
import { config } from './config.js';

const OPENAI_API_KEY = config.OPENAI_API_KEY;
const API_URL = 'https://api.openai.com/v1/images/generations';

export async function generateEventPoster(eventTitle, eventDescription) {
  try {
    const prompt = `Create a professional event poster for: ${eventTitle}. Description: ${eventDescription}. 
    The poster should be modern, visually appealing, and suitable for social media sharing. 
    Include elements that represent the event theme and make it stand out.`;

    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: "dall-e-3",
        prompt: prompt,
        n: 1,
        size: "1024x1024",
        quality: "standard",
        style: "vivid"
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.data[0].url;
  } catch (error) {
    console.error('Error generating poster:', error);
    throw error;
  }
}