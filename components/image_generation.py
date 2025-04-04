import streamlit as st
import time
from config.constants import SESSION_KEYS, DEFAULTS
from image_generation import (
    setup_image_generator,
    generate_images_with_imagen,
    process_imagen_response
)

def render_image_generation_interface():
    """Render the image generation interface."""
    # Header
    st.markdown("""
        <div class="header">
            <h2 style="color: #2196f3;">🎨 Image Generation</h2>
            <p style="color: #666;">Create amazing images with AI</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for image history
    if SESSION_KEYS["image_history"] not in st.session_state:
        st.session_state[SESSION_KEYS["image_history"]] = []
    
    # Setup the image generator
    imagen_ready = setup_image_generator()
    
    if not imagen_ready:
        pass  # Error messages are handled within setup_image_generator
    else:
        # Image generation form
        with st.form("image_generation_form"):
            st.markdown("### 🎯 Image Description")
            prompt = st.text_area(
                "Describe the image you want to generate",
                placeholder="A photorealistic cat wearing sunglasses...",
                height=100
            )
            
            st.markdown("### ⚙️ Generation Settings")
            col1, col2 = st.columns(2)
            with col1:
                num_images = st.number_input(
                    "Number of images",
                    min_value=1,
                    max_value=8,
                    value=DEFAULTS["num_images"],
                    help="How many variations to generate"
                )
            with col2:
                style = st.selectbox(
                    "Image Style",
                    ["Realistic", "Photographic", "Artistic", "Cartoon", "Abstract", "Watercolor", "Oil Painting"],
                    help="The artistic style of the generated images"
                )
            
            submitted = st.form_submit_button("✨ Generate Images")
        
        if submitted and prompt:
            handle_image_generation(prompt, num_images, style)
        
        # Display image generation history
        display_image_history()

def handle_image_generation(prompt, num_images, style):
    """Handle the image generation process."""
    with st.spinner("🎨 Creating your images..."):
        try:
            api_response = generate_images_with_imagen(
                prompt=prompt,
                num_images=num_images,
                style=style
            )
            
            if api_response:
                processed_images = process_imagen_response(api_response)
            else:
                processed_images = None
            
            if processed_images:
                st.session_state[SESSION_KEYS["image_history"]].append({
                    "prompt": prompt,
                    "style": style,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
                st.success(f"✨ Successfully generated {len(processed_images)} image(s)!")
                
                # Display images in a grid
                cols = st.columns(len(processed_images))
                for idx, (col, img) in enumerate(zip(cols, processed_images)):
                    with col:
                        st.image(img, caption=f"Image {idx + 1}")
            else:
                st.warning("Failed to generate or process images. Check the logs for details.")
        
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            logging.exception("Error in image generation:")

def display_image_history():
    """Display the image generation history."""
    if st.session_state.get(SESSION_KEYS["image_history"]):
        st.markdown("### 📜 Generation History")
        for entry in reversed(st.session_state[SESSION_KEYS["image_history"]]):
            with st.expander(f"🎨 {entry['prompt']} ({entry['style']})"):
                st.write(f"⏰ Generated at: {entry['timestamp']}") 