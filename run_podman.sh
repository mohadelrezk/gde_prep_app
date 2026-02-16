#!/bin/bash

# Definition of image name
IMAGE_NAME="gde-prep-app"

echo "🔨 Building the container image: $IMAGE_NAME..."
podman build -t $IMAGE_NAME -f Containerfile .

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "🚀 Running the container on port 8501..."
    podman run -d -p 8501:8501 --name gde_app_instance --replace $IMAGE_NAME
    
    echo "🌐 App is running at http://localhost:8501"
    echo "📝 To stop: podman stop gde_app_instance"
else
    echo "❌ Build failed. Please check the logs."
fi
