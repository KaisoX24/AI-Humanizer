import streamlit as st
from modules.humanizer import humanize_content
from modules.text_extractor import extract_text

st.set_page_config(page_title="AI Humanizer",layout='wide')
st.title(":yellow[AI Humanizer]")
st.sidebar.title(":green[File Upload:]")
uploaded_file=st.sidebar.file_uploader("Please Upload your file",type=['.txt','.pdf'])

if 'text' not in st.session_state:
    st.session_state.text=None

if not uploaded_file:
    st.info("Please Upload the File you want to Humanize",width=500)
else:
    file_name=uploaded_file.name
    file_type='txt' if file_name.endswith('.txt') else 'pdf'
    st.session_state.text=uploaded_file.read().decode('utf-8') if file_type=='txt' else extract_text(uploaded_file)
    col1,col2=st.columns([3,2])
    with col1:
        with st.container(border=True,height=500):
            st.write(":blue[**File contents:**]",)
            with st.expander("Extracted contents"): 
                st.write(st.session_state.text)
            st.write("Select the tone for Humanizing:")
            tones=st.selectbox(label='Tones',options=['Casual','Academic',],width=250)
            intensities=st.select_slider("Select Intensity",options=['Light','Medium','Heavy'],width=450)
            gen_btn=st.button(":red[**Humanize Content**]")
    if gen_btn:
        with col2:
            with st.container(border=True,height=300):
                with st.spinner("Generating Result's"):
                    result=humanize_content(text=st.session_state.text,tone=tones,intensity=intensities)
                    st.write(result)
            st.download_button(
                        label=":green[Download Humanized content]",
                        file_name="humanized_"+file_name,
                        data=result,
                        mime='text',
                    )