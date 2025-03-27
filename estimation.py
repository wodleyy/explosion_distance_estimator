def estimate_distance(flash_time: float, sound_time: float, temp_c: float) -> float:
    delay = sound_time - flash_time
    speed = 331 + 0.6 * temp_c
    distance = delay * speed
    print(f"\n🕒 Flash: {flash_time:.3f}s\n🔊 Sound: {sound_time:.3f}s\n🌡️ Temp: {temp_c}°C")
    print(f"📏 Distance: {distance:.2f} meters (~{distance/1000:.2f} km)")
    return distance
