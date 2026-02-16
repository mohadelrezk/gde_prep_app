# Google Data Engineering Prep App

A Streamlit web application designed to help users prepare for Google Data Engineering interviews.

## Prerequisites

- **Python 3.9+** (for local development)
- **Podman** (for containerized execution)
  - *Note: Docker can also be used, but instructions below focus on Podman.*

## Installation

### Local Setup

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Podman Setup

Ensure Podman is installed. If you are on macOS, you can install it using Homebrew:

```bash
brew install podman
podman machine init
podman machine start
```

## Running the Application

### Option 1: Using Podman (Recommended)

A helper script `run_podman.sh` is provided to build and run the container automatically.

1.  Make the script executable (if needed):
    ```bash
    chmod +x run_podman.sh
    ```

2.  Run the script:
    ```bash
    ./run_podman.sh
    ```

   This will:
   - Build the image `gde-prep-app`.
   - Run the container named `gde_app_instance`.
   - Expose the app on `http://localhost:8501`.

#### Manual Podman Commands

If you prefer to run commands manually:

**Build the image:**
```bash
podman build -t gde-prep-app -f Containerfile .
```

**Run the container:**
```bash
podman run -d -p 8501:8501 --name gde_app_instance --replace gde-prep-app
```

### Option 2: Running Locally

To run the app directly with Python/Streamlit:

```bash
streamlit run app.py
```

## Usage

Open your browser to [http://localhost:8501](http://localhost:8501) to verify the application is running.
