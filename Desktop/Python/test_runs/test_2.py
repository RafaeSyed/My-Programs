import sounddevice as sd
speaker = sd.query_devices(device=None, kind='input')
speaker = speaker["name"]
print(speaker)