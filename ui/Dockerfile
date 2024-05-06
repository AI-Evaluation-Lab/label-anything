# Use official Node.js image as the base image
FROM node:21-alpine AS BUILDER

# Declaring env
ENV NODE_ENV production

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY ./package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .


# Build the React app for production
RUN npm run build

# Fetching the latest nginx image
FROM nginx


# Copying built assets from builder
COPY --from=builder /app/build /usr/share/nginx/html

# Copying our nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf