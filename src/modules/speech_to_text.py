import whisper

def speech_to_text(speech):
    model = whisper.load_model("base")
    result = model.transcribe(speech, verbose=False)
    return result["text"]

