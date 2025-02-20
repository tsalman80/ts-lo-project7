import base64
import pandas as pd
import streamlit as st
from processors.image import ImageProcessor
from processors import ContentProcessor
from processors.transformations import ContentTransformer
from storage.db import ContentStore
import config
import os
import io
from PIL import Image


def initialize_session_state():
    if "content_store" not in st.session_state:
        st.session_state.content_store = ContentStore()

    if "content_transformer" not in st.session_state:
        st.session_state.transformer = ContentTransformer()


def show_upload_page():
    st.header("Upload Content")

    allowed_extensions = []
    for exts in config.ALLOWED_EXTENSIONS.values():
        allowed_extensions.extend([ext.strip(".") for ext in exts])

    uploaded_file = st.file_uploader("Choose a file", type=allowed_extensions)

    if uploaded_file is not None:
        if not ContentProcessor.validate_file_size(uploaded_file):
            st.error("File size is too large")
            return

        content_type = ContentProcessor.detect_content_type(uploaded_file)
        st.write(f"Detected content type: {content_type}")

        if content_type == "image":
            image = ImageProcessor.process(uploaded_file)
            st.image(image, caption="Uploaded Image")

            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")

            st.session_state.content_store.save_content(
                content_type=content_type,
                original_path=uploaded_file.name,
                data=image_bytes.getvalue(),
                metadata="Uploaded Image",
            )
        elif content_type == "text":
            string_data = uploaded_file.read().decode("utf-8")
            st.text_area("Uploaded Text", string_data, height=300)
            st.session_state.content_store.save_content(
                content_type=content_type,
                original_path=uploaded_file.name,
                data=string_data,
                metadata="Uploaded Text",
            )
        else:
            st.info("Preview not available for this file type")

        st.success("File uploaded and processed successfully")


def show_transform_page():
    st.header("Transform Content")
    transformer: ContentTransformer = st.session_state.get("transformer", None)

    if transformer is None:
        st.error("Content transformer not initialized")
        return

    transform_type = st.selectbox(
        "Select the transformation type", ["Text to Image", "Image to Text"]
    )

    if transform_type == "Text to Image":
        text_prompt = st.text_area("Enter a prompt for the image you want to generate")
        if st.button("Generate Image"):
            if text_prompt:
                msg = st.info("Generating image...")
                image = transformer.text_to_image(text_prompt)
                st.image(image, caption="Transformed Image")
                msg.empty()
                msg.info("Image generated successfully")
                image_bytes = io.BytesIO()
                image.save(image_bytes, format="PNG")
                st.session_state.content_store.save_content(
                    content_type="image",
                    original_path="Text to Image",
                    data=image_bytes.getvalue(),
                    metadata=text_prompt,
                )
    elif transform_type == "Image to Text":
        st.write("Upload an image to get description")
        uploaded_file = st.file_uploader(
            "Choose an image", type=config.ALLOWED_EXTENSIONS["image"], key="transform"
        )

        if uploaded_file is not None:
            image = ImageProcessor.process(uploaded_file)
            st.image(image, caption="Uploaded Image")
            if st.button("Generate Description"):
                msg = st.info("Generating description...")
                text = transformer.image_to_text(image)
                # text = "This a an AI generated description."
                msg.empty()
                msg.info("Description generated successfully")
                st.write(text)

                image_bytes = io.BytesIO()
                image.save(image_bytes, format="PNG")
                st.session_state.content_store.save_content(
                    content_type="image",
                    original_path=uploaded_file.name,
                    data=image_bytes.getvalue(),
                    metadata=text,
                )


def show_explore_page():
    st.header("Explore Content")
    st.write("Here you can explore the content you have uploaded and transformed")
    content = st.session_state.content_store.get_content()

    df = pd.DataFrame(
        content,
        columns=[
            "id",
            "content_type",
            "original_path",
            "data",
            "metadata",
            "created_at",
        ],
    )

    df["data"] = df["data"].apply(
        lambda x: f"data:image/png;base64,{base64.b64encode(x).decode('utf-8')}"
    )
    st.dataframe(
        df,
        column_config={
            "data": st.column_config.ImageColumn(),
        },
        hide_index=True,
    )


def main():
    st.title("AI Social Hub")
    initialize_session_state()
    page = st.sidebar.selectbox("Select a page", ["Upload", "Transform", "Explore"])

    if page == "Upload":
        show_upload_page()
    elif page == "Transform":
        show_transform_page()
    elif page == "Explore":
        show_explore_page()


if __name__ == "__main__":
    main()
