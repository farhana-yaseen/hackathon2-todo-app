# Multi-stage build
# Stage 1: Dependencies
FROM node:20-alpine AS installer
WORKDIR /app
COPY package.json yarn.lock* ./
RUN yarn install --frozen-lockfile

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
COPY --from=installer /app/node_modules ./node_modules
RUN yarn run build

# Stage 3: Runner
FROM node:20-alpine AS runner
WORKDIR /app

# Install dumb-init for graceful shutdown
RUN apk add --no-cache dumb-init

# Copy the built application from the builder stage
COPY --from=builder /app/package.json ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=installer /app/node_modules ./node_modules

# Expose port 3000
EXPOSE 3000

# Set production environment
ENV NODE_ENV=production

# Start the application
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]