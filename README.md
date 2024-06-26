# Collaborative Whiteboard Application

Welcome to the Interactive Whiteboard Application project! This application is designed to provide a collaborative environment for users to share ideas, drawings, and notes in real-time. This project is forked from [collabio](https://github.com/kriziu/collabio), an incredible project that laid the frontend foundation for real-time collaboration. We've built upon this frontend, enhancing the project with new features, technologies, and a streamlined user experience.

## Try it out
[Live demo!](https://ai.sacade.net)

## Technologies Used

Our project is built using a combination of powerful technologies to ensure a smooth, real-time experience:

- **Backend**:
  - **Flask**: A micro web framework written in Python, chosen for its simplicity and flexibility.
  - **Flask-SocketIO**: Enables real-time bidirectional event-based communication between the web clients and the server.
  - **OpenAI**: Allows the user to query about the app and tools or any other needs.
  
- **Frontend**:
  - **Next.js**: A React framework for production, providing features like server-side rendering and generating static websites for React-based web applications.
  - **Socket.IO**:Enables real-time bidirectional event-based communication between the web clients and the server.
  - **Recoil**: A state management library for React, used for managing global state across components in our Next.js application.
  - **TailwindCSS**: A utility-first CSS framework for creating custom designs without having to leave your HTML.
  - **Framer Motion**: A popular library for React used to easily add animations and interactive elements to our application.



## Getting Started

To get the application running, you'll need to set up both the backend and frontend. Below are the steps to do so:

### Clone the Repository

```bash
git clone https://github.com/KennyNova/Interactive-Whiteboard .
```

### Backend Setup

1. Open your terminal or command prompt.
2. Change directory to the backend folder:
   ```bash
   cd backend
3. Install the necessary Python dependencies by running:
    ```py
    pip install -r requirements.txt
    ```
4. Set up the environment and start the Flask application :
    ```bash
    Set-ExecutionPolicy Unrestricted -Scope Process (Windows)
    .\venv\Scripts\activate (Windows)
    source /venv/Scripts/activate (mac)
    cd app
    python main.py
    ```
### Frontend Setup
1. Open a new terminal or command prompt window.
2. Navigate to the frontend directory:
    ```bash
    cd frontend2.0
    ```
3. Install the dependencies:
    ```
    npm install
    ```
4. Start the development server:
    ```
    npm run dev
    ```
Now, your application should be running, and you can access the frontend through your web browser at the default URL(localhost:3000) provided by the Next.js development server.
