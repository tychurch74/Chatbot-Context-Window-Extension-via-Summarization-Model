from elevenlabslib import *
import pydub
import pydub.playback
import io


def text_to_speech(text):
    user = ElevenLabsUser("81d8ddb9a21470a5c1f05da5d2964bf8")
    voice = user.get_voices_by_name("Rachel")[0]
    speech = voice.generate_audio_bytes(text)
    return speech


def play(bytesData):
    sound = pydub.AudioSegment.from_file_using_temporary_files(io.BytesIO(bytesData))
    pydub.playback.play(sound)
    return
