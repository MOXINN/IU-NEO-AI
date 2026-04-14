# ============================================================================
# IU NWEO AI — Frontend Dockerfile (Next.js)
# Maintainer: Ops
# ============================================================================

FROM node:22-alpine AS base

WORKDIR /app

# Install dependencies first (layer caching)
COPY package.json package-lock.json* ./
RUN npm ci

# Copy app source
COPY . .

# Expose Next.js dev server port
EXPOSE 3000

# Dev mode — hot-reload via volume mount
CMD ["npm", "run", "dev"]
