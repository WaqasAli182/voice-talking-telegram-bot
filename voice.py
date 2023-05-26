# CHECKING OUT THE VOICE


from elevenlabs import generate, play, save
from elevenlabs import set_api_key
set_api_key("ELEVEN LABS API KEY")
from elevenlabs.api import Voices
voices = Voices.from_api()
voice_used=voices[9]
voice_used.settings.stability = 0.15
voice_used.settings.similarity_boost = 0.70


audio = generate(
  text="Hi how are you?",
  voice=voice_used,
  model="eleven_monolingual_v1"
)

play(audio)