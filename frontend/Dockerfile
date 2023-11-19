
# Use a base image with Node.js installed
FROM node:14

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# Install the required modules
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the appropriate port
EXPOSE 3000

# Set the command to run the frontend application
CMD ["npm", "start"]
