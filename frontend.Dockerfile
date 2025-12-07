FROM node:18-alpine

WORKDIR /app

COPY shaders-landing-page/package.json shaders-landing-page/package-lock.json* ./
# Install dependencies
RUN npm install

# Copy source
COPY shaders-landing-page/ .

# Build
RUN npm run build

# Start
CMD ["npm", "start"]
