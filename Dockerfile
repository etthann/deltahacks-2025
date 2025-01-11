FROM node:18-alpine

RUN adduser -D appuser

WORKDIR /app

COPY package*.json ./

RUN chown -R appuser:appuser /app
USER appuser

RUN npm install

COPY --chown=appuser:appuser . .

EXPOSE 3000

# Healthcheck to ensure the service is running
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:3000"] || exit 1

# Start the application
CMD ["npm", "run", "dev"]