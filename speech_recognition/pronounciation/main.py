import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import time

# === Настройки ===
sample_rate = 44100
duration = 4  # секунд записи
max_errors = 3
score = 0
errors = 0

# === Слова по уровням ===
words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце", "луна", "почему"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение", "сосед"]
}

# === Выбор уровня сложности ===
print("🎮 Добро пожаловать в игру «Говори правильно»!")
print("Выбери уровень сложности: easy / medium / hard")
level = input(">>> ").strip().lower()

while level not in words_by_level:
    print("❗ Уровень не найден. Попробуй ещё раз.")
    level = input(">>> ").strip().lower()

word_list = words_by_level[level]
random.shuffle(word_list)

print(f"\n🟢 Уровень сложности: {level.capitalize()}")
print("🧠 Ты увидишь слово по-русски. Произнеси его перевод на английском.")
time.sleep(2)

# === Инициализация инструментов ===
recognizer = sr.Recognizer()
translator = Translator()

# === Основной игровой цикл ===
for word in word_list:
    print(f"\n📣 Слово: {word}")

    # 🎙 Запись речи
    print("🎙 Говори...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", sample_rate, recording)
    print("✅ Запись завершена, распознаём...")

    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        recognized = recognizer.recognize_google(audio, language="en-US").lower()
        print("📝 Ты сказал:", recognized)

        translation = translator.translate(word, src="ru", dest="en").text.lower()
        print("🔤 Перевод:", translation)

        # Сравнение ответа
        if recognized == translation:
            score += 1
            print("✅ Верно! +1 очко")
        else:
            errors += 1
            print(f"❌ Неверно. Ожидалось: {translation}. Ошибок: {errors}/{max_errors}")

        if errors >= max_errors:
            print("\n💀 Игра окончена. Ты допустил 3 ошибки.")
            break

    except sr.UnknownValueError:
        errors += 1
        print(f"😕 Не удалось распознать речь. Ошибок: {errors}/{max_errors}")
        if errors >= max_errors:
            print("\n💀 Игра окончена. Ты допустил 3 ошибки.")
            break

    except sr.RequestError as e:
        print(f"❗ Ошибка сервиса: {e}")
        break

# === Итоги ===
print(f"\n🏁 Конец игры. Твой счёт: {score}")