# Use an official Node runtime as a parent image
FROM node:20.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN npm install

# Build the project
RUN npm run build

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV NODE_ENV production

# Run npm start when the container launches
CMD ["npm", "start"]
