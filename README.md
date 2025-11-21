# ⚕️ Health Data Analytics AI Service

This repository contains the code for a custom GenAI solution designed for performing data analysis on health-related datasets. The application uses a LangGraph-based agent orchestrator (FastAPI backend) for complex query analysis and Streamlit for a user-friendly web interface (frontend).

The entire application is containerized using Docker and managed with Docker Compose for easy, consistent deployment.

## 🚀 Application Architecture

The application is structured into two main services communicating over a virtual Docker network:

1.  **Backend (`main.py`):** A FastAPI service housing the core LangGraph agent, security layers (PHI Redactor, Input Guardrail), and the data analysis logic. It serves API requests on port 8000.
2.  **Frontend (`frontend.py`):** A Streamlit application providing the user interface to interact with the backend service. It runs on port 8501.

***

## ⚙️ Prerequisites

Ensure you have the following tools installed on your system before starting:

1.  **Git:** For cloning the repository.
2.  **Docker:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine installed and running.
3.  **API Key:** An active **Groq API Key** for the Language Model (LLM) used by the backend agent.

***

## 💻 Setup and Installation

Follow these steps to set up the project locally and prepare the environment.

### 1. Clone the Repository

```bash
git clone [YOUR_REPOSITORY_URL]
cd health-data-analytics/
```

### 2. Configure Environment Variables
The backend service needs your API key to function. Create a file named `.env` in the root of your project directory `(health-data-analytics/)` and add your key:
```bash
GROQ_API_KEY="sk_your_groq_api_key_here"
```

### 3. Run the notebook in `data_generator/mock_data_generator.ipynb` to generate synthetic data and place it inside `health-data-analytics/data/` folder
It will create 2 datasets.

### 4. Build and start the container
```
docker compose up --build -d
```

### 5. Review Backend Logs (Troubleshooting)
```
docker compose logs backend
```

### 6. Access the application
<table>
  <thead>
    <tr>
      <th>Service</th>
      <th>Access URL</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Frontend (UI)</td>
      <td>http://localhost:8501</td>
      <td>The Streamlit web interface for submitting data analysis queries.</td>
    </tr>
    <tr>
      <td>Backend (API)</td>
      <td>http://localhost:8000/docs</td>
      <td>The FastAPI documentation (Swagger UI) for testing the /analyze endpoint directly.</td>
    </tr>
  </tbody>
</table>


