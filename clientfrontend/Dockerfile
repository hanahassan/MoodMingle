# Use Node.js image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package files and install dependencies
COPY clientfrontend/package*.json ./
RUN npm install

# Copy the frontend code
COPY clientfrontend/ .

# Build the React app
RUN npm run build

# Serve the app using a lightweight web server
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]

# Expose the frontend port
EXPOSE 3000