
import streamlit as st
from cryptography.fernet import Fernet, InvalidToken
from pathlib import Path

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="File Encryption & Decryption",
    page_icon="🔐",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #2563eb;
}
.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 17px;
}
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🔐 File Encryption & Decryption Tool</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Protect your text and documents with secure encryption.</div>',
    unsafe_allow_html=True
)
st.divider()

# ---------------- ENCRYPTION KEY ----------------
KEY_FILE = Path(__file__).parent / "secret.key"


def get_cipher():
    """Load the existing key or create one on first use."""
    if not KEY_FILE.exists():
        KEY_FILE.write_bytes(Fernet.generate_key())

    key = KEY_FILE.read_bytes()
    return Fernet(key)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("**Available features**")
    st.write("✅ Text encryption")
    st.write("✅ PDF encryption")
    st.write("✅ TXT and DOCX files")
    st.write("✅ Image and other file encryption")
    st.write("✅ File decryption")
    st.divider()
    st.warning(
        "Keep secret.key safe. You need the same key to decrypt "
        "files encrypted with it."
    )

# ---------------- OPERATION SELECTION ----------------
left, right = st.columns(2)

with left:
    operation = st.selectbox(
        "Choose operation",
        ["Encrypt", "Decrypt"]
    )

with right:
    input_type = st.selectbox(
        "Choose input type",
        ["File", "Text"]
    )

# ---------------- TEXT ENCRYPTION ----------------
if input_type == "Text":
    text_input = st.text_area(
        "Enter your text",
        height=180,
        placeholder="Type the text you want to encrypt or decrypt..."
    )

    if st.button("🔒 Process Text", type="primary"):
        if not text_input.strip():
            st.warning("Please enter some text.")
        else:
            try:
                cipher = get_cipher()

                if operation == "Encrypt":
                    result = cipher.encrypt(
                        text_input.encode("utf-8")
                    ).decode("utf-8")
                    st.success("Text encrypted successfully!")
                else:
                    result = cipher.decrypt(
                        text_input.strip().encode("utf-8")
                    ).decode("utf-8")
                    st.success("Text decrypted successfully!")

                st.text_area(
                    "Result",
                    value=result,
                    height=180
                )

                st.download_button(
                    "⬇️ Download Result",
                    data=result,
                    file_name=(
                        "encrypted_text.txt"
                        if operation == "Encrypt"
                        else "decrypted_text.txt"
                    ),
                    mime="text/plain"
                )

            except InvalidToken:
                st.error(
                    "Decryption failed. The text may be incorrect, "
                    "or it may have been encrypted using a different key."
                )
            except Exception as error:
                st.error(f"Operation failed: {error}")

# ---------------- FILE ENCRYPTION ----------------
else:
    st.subheader("📁 Upload Your File")

    uploaded_file = st.file_uploader(
        "Select a PDF, TXT, DOCX, image, or another file",
        type=None,
        accept_multiple_files=False,
        help="For decryption, upload the encrypted file produced by this tool."
    )

    if uploaded_file:
        st.info(f"Selected file: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")

        if uploaded_file.size == 0:
            st.warning("The selected file is empty.")

        elif st.button("🔐 Process File", type="primary"):
            try:
                cipher = get_cipher()
                file_data = uploaded_file.getvalue()

                if operation == "Encrypt":
                    result = cipher.encrypt(file_data)
                    output_filename = uploaded_file.name + ".encrypted"
                    st.success("File encrypted successfully!")

                else:
                    result = cipher.decrypt(file_data)

                    if uploaded_file.name.endswith(".encrypted"):
                        output_filename = uploaded_file.name[:-10]
                    else:
                        output_filename = "decrypted_" + uploaded_file.name

                    st.success("File decrypted successfully!")

                st.download_button(
                    "⬇️ Download Processed File",
                    data=result,
                    file_name=output_filename,
                    mime="application/octet-stream"
                )

                st.caption(
                    "Your processed file is ready to download. "
                    "The original uploaded file is not overwritten."
                )

            except InvalidToken:
                st.error(
                    "Decryption failed. Check that you uploaded the correct "
                    "encrypted file and that secret.key is the original key."
                )
            except Exception as error:
                st.error(f"File processing failed: {error}")

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "Academic project | Python • Streamlit • Fernet encryption"
)

