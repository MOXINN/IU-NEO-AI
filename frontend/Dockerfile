# ============================================================================
# IU NWEO AI — Frontend Dockerfile (Development)
# Maintainer: DevOps Lead
# ============================================================================

FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies first (for better caching)
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Expose Next.js default port
EXPOSE 3000

# Next.js 15/16 Telemetry disabled for dev speed
ENV NEXT_TELEMETRY_DISABLED 1

# Start the development server with hot-reloading support
CMD ["npm", "run", "dev"]
