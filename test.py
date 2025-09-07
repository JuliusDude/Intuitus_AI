import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import io
import openai

# Make sure you have: pip install streamlit-webrtc openai av

# Replace with your OpenAI key
openai.api_key = "YOUR_OPENAI_API_KEY"

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []

    def recv_audio_frame(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Collect audio
        self.audio_frames.append(frame.to_ndarray())
        return frame

st.write("🎤 Speak to record your message")

ctx = webrtc_streamer(
    key="speech-to-text",
    mode="sendonly",
    audio_receiver_size=256,
    media_stream_constraints={"audio": True, "video": False},
)

if ctx.audio_receiver:
    audio_frames = ctx.audio_receiver.get_frames(timeout=1)
    if audio_frames:
        # Convert audio frames into WAV file in memory
        with io.BytesIO() as wav_buffer:
            # Export audio as WAV using PyAV
            frames = [f.to_ndarray().tobytes() for f in audio_frames]
            wav_buffer.write(b"".join(frames))
            wav_buffer.seek(0)

            # Call Whisper for transcription
            transcript = openai.Audio.transcriptions.create(
                model="whisper-1",
                file=("speech.wav", wav_buffer, "audio/wav")
            )
            st.success(f"Transcribed: {transcript.text}")

            # Example: Add directly to chatbot state
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"type": "user", "content": transcript.text})
            st.session_state.messages.append({"type": "bot", "content": f"Echo: {transcript.text}"})
