# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, options
from firebase_admin import initialize_app
from firebase_admin import storage
import openai
import io

initialize_app()


@https_fn.on_request(
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"])
)
def transcribe(req: https_fn.Request) -> https_fn.Response:
    filename = req.args["filename"]
    bucket = storage.bucket()
    audio_blob = bucket.blob(filename)
    audio_bytes = audio_blob.download_as_bytes()
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = filename
    try:
        openai.api_key = "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"
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    except Exception as e:
        return https_fn.Response(str(e))
    return https_fn.Response(transcript.text)
