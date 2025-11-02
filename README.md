# Hey Whisper

Command-line tool for audio transcription using OpenAI Whisper AI. It records your voice and copies the transcription to the clipboard,
nothing else.

Useful when used along with a keyboard shortcut. There are other tools that do
the same such as [Blurt](https://github.com/QuantiusBenignus/blurt) or [Whispering](https://whispering.bradenwong.com/), but:
- Blurt is meant to be used with an instance of whisper.cpp, not with the Whisper API hosted by OpenAI. 
This is nice but a bit more complex
- Whispering on Linux (desktop version) is buggy and I could not make it work with a global shortcut.

## Installation
Just pip install it and make sure you have set the environment variable `OPENAI_API_KEY` with your API key.  
Alternatively, you can pass it when invoking the command:

```sh
hey_whisper --api-key sk-...
```

I recommend setting a global shortcut to call the script. In GNOME this would be:
```sh
gnome-terminal -- bash -c "hey_whisper; exit"
```

If you are a mouse heavy user, you can also map the keyboard shortcut to a mouse button combination 
using [InputRemapper](https://github.com/sezanzeb/input-remapper)
