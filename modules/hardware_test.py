# The GUIless Mac Tester
## by Jules David
import os
import sounddevice as sd
import numpy as np
import wavio
import tkinter as tk

RECORD_SECONDS = 2
SAMPLE_RATE = 44100
test_results = {}

# Fonction de réponses au rapport de tests
def ask_confirmation(component):
    response = input(f"Est-ce que {component} fonctionne ? O/n : ").strip()
    if response == '' or response.lower() == 'o':
        return "Fonctionnel"
    elif response.lower() == 'n':
        return "Défectueux"
    else:
        print("Réponse invalide, par défaut 'Oui' enregistré.")
        return "Fonctionnel"

# Test des composants

def test_microphone(output_dir):
    print("Enregistrement audio...")
    audio_data = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float64')
    sd.wait()
    # Save audio file in OUTPUT_DIR
    audio_file_path = os.path.join(output_dir, "test_microphone.wav")
    wavio.write(audio_file_path, audio_data, SAMPLE_RATE, sampwidth=3)
    print(f"Fichier audio enregistré dans : {audio_file_path}")
    test_results["Microphone"] = ask_confirmation("le microphone")

# Test des haut-parleurs
def test_speakers():
    print("Test des haut-parleurs...")
    frequency = 440
    duration = 2
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    left_channel = 0.5 * np.sin(2 * np.pi * frequency * t)
    right_channel = 0.5 * np.sin(2 * np.pi * frequency * t)
    stereo_sound = np.vstack((left_channel, right_channel)).T

    sd.play(np.array([left_channel, np.zeros_like(left_channel)]).T, samplerate=fs)
    sd.wait()
    test_results["Haut-parleur gauche"] = ask_confirmation("le haut-parleur gauche")
    
    sd.play(np.array([np.zeros_like(right_channel), right_channel]).T, samplerate=fs)
    sd.wait()
    test_results["Haut-parleur droit"] = ask_confirmation("le haut-parleur droit")
    
    sd.play(stereo_sound, samplerate=fs)
    sd.wait()
    test_results["Haut-parleurs (stéréo)"] = ask_confirmation("les deux haut-parleurs")

def run_tests(output_file, output_dir):
    # test_screen()
    test_speakers()
    test_microphone(output_dir)
    # test_camera()

    # Enregistrer les résultats dans le fichier spécifié
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write("=== RESULTATS TESTS MATERIELS ===\n")
        for component, status in test_results.items():
            file.write(f"{component}: {status}\n")
        file.write("\n")

    print(f"Les résultats matériels ont été exportés dans {output_file} avec succès.")
    return test_results
