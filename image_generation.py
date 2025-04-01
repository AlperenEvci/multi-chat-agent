import streamlit as st
# Use Google Cloud AI Platform SDK for Imagen
import google.cloud.aiplatform as aiplatform
# from google.cloud.aiplatform.gapic import PredictionServiceClient # Potentially needed
# from google.protobuf import json_format # Potentially needed
# from google.protobuf.struct_pb2 import Value # Potentially needed
import base64
from PIL import Image
import io
import os
from dotenv import load_dotenv
import logging
import time # Added for potential retries or delays

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Imagen Configuration ---
# These should be in your .env file or environment variables
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1") # Default location
IMAGEN_MODEL_NAME = "imagegeneration@006" # Using a specific stable Imagen model version

def setup_image_generator():
    """Initialize the Imagen model using Google Cloud AI Platform."""
    try:
        if not PROJECT_ID:
            raise ValueError("GOOGLE_CLOUD_PROJECT not found in environment variables.")
        
        aiplatform.init(project=PROJECT_ID, location=LOCATION)
        logger.info(f"Initialized AI Platform for project '{PROJECT_ID}' in location '{LOCATION}'")
        
        # Get the Imagen model endpoint (no need to load the model object directly)
        # The predict method uses the endpoint name structure.
        # model = aiplatform.Model(model_name=IMAGEN_MODEL_NAME) # This might not be needed
        logger.info(f"Using Imagen model endpoint: {IMAGEN_MODEL_NAME}")
        # Return something truthy to indicate success, actual generation uses aiplatform.predict
        return True # Indicate setup success

    except ImportError:
         logger.error("google-cloud-aiplatform library not found. Please install it: pip install google-cloud-aiplatform")
         st.error("Required library 'google-cloud-aiplatform' not found. Please install it.")
         return None
    except Exception as e:
        logger.error(f"Failed to initialize AI Platform for Imagen: {e}")
        st.error(f"Failed to initialize Imagen model: {e}")
        return None

def generate_images_with_imagen(prompt: str, num_images: int = 1, style: str = "Realistic"):
    """Generates images using the Imagen model via AI Platform Prediction."""
    try:
        # Map friendly style names to potential Imagen parameters if available,
        # or just include in the prompt. For now, include in prompt.
        enhanced_prompt = f"{prompt}, {style.lower()} style"

        # Imagen API parameters
        # Note: Parameter names might change based on the model version (e.g., @006)
        parameters = {
            "sampleCount": num_images, # Number of images to generate
            # "aspectRatio": "1:1", # Example: specify aspect ratio if needed
            # "guidanceScale": 7, # Example: control prompt adherence
            # Add other parameters as needed based on Imagen documentation for the model version
        }

        # Construct the instance payload
        instances = [{"prompt": enhanced_prompt}]

        # Get the regional endpoint based on the location
        client_options = {"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
        client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
        
        endpoint = (
            f"projects/{PROJECT_ID}/locations/{LOCATION}/"
            f"publishers/google/models/{IMAGEN_MODEL_NAME}"
        )

        logger.info(f"Sending prediction request to endpoint: {endpoint}")
        logger.info(f"Instance: {instances[0]}")
        logger.info(f"Parameters: {parameters}")

        # Make the prediction call
        response = client.predict(
            endpoint=endpoint, instances=instances, parameters=parameters
        )
        
        logger.info("Prediction request successful.")
        return response

    except Exception as e:
        logger.error(f"Error during Imagen prediction request: {e}")
        st.error(f"Error calling Imagen API: {e}")
        return None

def process_imagen_response(response):
    """Process the prediction response from the Imagen model."""
    generated_images = []
    try:
        if not response or not response.predictions:
            logger.warning("Received empty or invalid response from Imagen model.")
            return None

        # Imagen response structure might vary, check logs or documentation
        # Assuming predictions is a list and each prediction has a 'bytesBase64Encoded' field
        for prediction in response.predictions:
            # Prediction is often a protobuf struct, convert to dict
            prediction_dict = prediction # Assuming it behaves like a dict or access fields directly
            if hasattr(prediction_dict, 'items'): # Check if it's dict-like
                 prediction_dict = dict(prediction_dict.items())

            # Find the base64 encoded image data field (name might vary)
            # Common names: 'bytesBase64Encoded', 'imageBytes', 'content'
            b64_data = prediction_dict.get('bytesBase64Encoded') # Adjust key if necessary
            
            if not b64_data:
                 # Try other common keys if the first one fails
                 b64_data = prediction_dict.get('image_bytes') 
            
            if b64_data:
                 try:
                     image_data = base64.b64decode(b64_data)
                     image = Image.open(io.BytesIO(image_data))
                     generated_images.append(image)
                     logger.info("Successfully decoded and processed an image from Imagen response.")
                 except Exception as decode_err:
                     logger.error(f"Failed to decode base64 image data: {decode_err}")
            else:
                 logger.warning(f"Could not find image data in prediction: {prediction_dict}")


        return generated_images if generated_images else None

    except Exception as e:
        logger.error(f"Error processing Imagen response predictions: {e}")
        return None

# --- Streamlit App Interface (No changes needed below this line for the switch to Imagen, *if* app.py calls correctly) ---
# The setup_image_generator returns True/None now.
# The image generation logic is now encapsulated in generate_images_with_imagen.
# The process_imagen_response handles the new response format.
# app.py needs to be updated to call these new functions.

# --- Placeholder for app.py integration (app.py needs modification) ---
# This part is just illustrative of how app.py *should* call the new functions.
# DO NOT copy this directly into image_generation.py. It belongs in app.py's logic.
if __name__ == "__main__":
     # Example Usage (for testing, simulate app.py logic)
     st.title("🎨 AI Image Generator (Imagen Test)")
     
     if setup_image_generator(): # Check if setup was successful
          test_prompt = "A photorealistic cat wearing sunglasses"
          num_test_images = 1
          style_test = "Photographic"
          
          with st.spinner("Generating test image with Imagen..."):
                api_response = generate_images_with_imagen(test_prompt, num_test_images, style_test)
          
          if api_response:
                processed_images = process_imagen_response(api_response)
                if processed_images:
                     st.success("Imagen generation successful!")
                     st.image(processed_images[0], caption="Test Image from Imagen")
                else:
                     st.error("Failed to process Imagen response.")
          else:
                st.error("Imagen API call failed.")
     else:
          st.error("Imagen setup failed. Check Project ID/Location and ensure 'google-cloud-aiplatform' is installed.") 