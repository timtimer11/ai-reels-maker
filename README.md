# AI Reels Maker

AI-powered application for generating short video reels, using Next.js for frontend and FastAPI for backend. Integration with AI services and video/audio processing is provided.

## Features

- Video reels are generated from Reddit posts
- Audio transcription and AI captioning are supported
- Reddit, OpenAI and Deepgram clients are used for content fetching and processing
- Frontend is built with Next.js
- Backend is built with FastAPI

## Technologies

- Frontend: Next.js 14, React, TailwindCSS
- Backend: FastAPI (Python)
- AI/ML: OpenAI, Deepgram
- Other: Boto3, Reddit API, Upstash

## Getting Started

1. Dependencies are installed:
   ```bash
   npm install
   pip3 install -r requirements.txt
   ```
2. Development servers are started:
   ```bash
   npm run dev
   ```
   (Both Next.js and FastAPI will be started together if running locally)

3. Environment variables are configured in `.env` files (not included).

## Project Structure

- `/app` — Next.js frontend core application
- `/backend` — FastAPI backend, with clients for Reddit, OpenAI, Deepgram, and media processing
- `/components` — React UI components
- `/lib` — Shared libraries
- `/public` — Static assets

## Usage

- Video reels are created by navigating to the generate-content page.
- Content is fetched and processed automatically on-click.
- Resulting video can be downloaded from web browser.

## Deploy to Production

You can clone & deploy it to Railway by deploying Frontend and Backend on separate services. 
The app will likely fail if deployed on Vercel.app due to usage of "ffmpeg" library.
