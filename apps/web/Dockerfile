# Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install --frozen-lockfile

# Copy source files
COPY . .

# Build for production
RUN npm run build

# Final stage
FROM nginx:stable-alpine

# Copy build output to nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
