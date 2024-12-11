import streamlit as st
import random
import string

# Enigma encoding-related functions
def rand_plugboard_config(num_of_config=13):
    alphabet = list(string.ascii_uppercase)
    shuffled = alphabet.copy()
    random.shuffle(shuffled)

    while any(shuffled[i] == shuffled[i + 1] for i in range(0, len(shuffled), 2)):
        random.shuffle(shuffled)

    shuffled_pairs = shuffled[:num_of_config * 2]
    plugboard = {letter: letter for letter in alphabet}

    for i in range(0, len(shuffled_pairs), 2):
        plugboard[shuffled_pairs[i]], plugboard[shuffled_pairs[i + 1]] = shuffled_pairs[i + 1], shuffled_pairs[i]

    return plugboard

alphabet = list(string.ascii_uppercase)
possible_rotors_combos = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    "VZBRGITYUPSDNHLXAWMJQOFECK"
]

possible_reflector_combos = [
    "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "FVPJIAOYEDRZXWGCTKUQSBNMHL"
]

def create_rotors(num_rotors):
    rotors = []
    for _ in range(num_rotors):
        rotor = {}
        rand_rotor_combo = random.choice(possible_rotors_combos)
        for i, letter in enumerate(rand_rotor_combo):
            rotor[alphabet[i]] = letter
        rotors.append(rotor)
    return rotors

def create_reflector():
    reflector = {}
    rand_reflector_combo = random.choice(possible_reflector_combos)
    for i, letter in enumerate(rand_reflector_combo):
        reflector[alphabet[i]] = letter
    return reflector

def shift_values(rotor):
    keys = list(rotor.keys())
    values = list(rotor.values())
    shifted_values = values[1:] + values[:1]
    shifted_rotor = {keys[i]: shifted_values[i] for i in range(len(keys))}
    return shifted_rotor

def rotate_rotors(rotors, rotors_rotate):
    rotors_rotate[0] += 1
    rotors[0] = shift_values(rotors[0])

    for i in range(len(rotors_rotate)):
        if rotors_rotate[i] % len(alphabet) == 0 and rotors_rotate[i] != 0:
            rotors_rotate[i] = 0
            if i + 1 < len(rotors_rotate):
                rotors_rotate[i + 1] += 1
                rotors[i + 1] = shift_values(rotors[i + 1])

    return rotors, rotors_rotate

def use_rotors_and_reflector(letter, rotors, reflector, plugboard):
    letter = plugboard[letter]
    for rotor in rotors:
        letter = rotor[letter]
    letter = reflector[letter]
    for rotor in reversed(rotors):
        letter = list(rotor.keys())[list(rotor.values()).index(letter)]
    letter = plugboard[letter]
    return letter

def encode_message(message, num_rotors=3, num_plugboard_pairs=13):
    message = message.upper()
    plugboard = rand_plugboard_config(num_plugboard_pairs)
    rotors = create_rotors(num_rotors)
    reflector = create_reflector()
    rotors_rotate = [0] * num_rotors
    encoded_message = ""

    for letter in message:
        if letter == " ":
            encoded_message += " "
            continue

        rotors, rotors_rotate = rotate_rotors(rotors, rotors_rotate)
        encoded_letter = use_rotors_and_reflector(letter, rotors, reflector, plugboard)
        encoded_message += encoded_letter

    return encoded_message

# Initialize session state
if "encoded_messages" not in st.session_state:
    st.session_state["encoded_messages"] = {}

# Streamlit interface
st.title("Enigma Machine Encoder/Decoder")

mode = st.sidebar.selectbox("Choose Mode", ["Encode", "Decode"])

if mode == "Encode":
    user_message = st.text_input("Enter the message you wish to encode:")
    if st.button("Encode"):
        if user_message.strip():
            encoded_message = encode_message(user_message)
            # Store encoded message with original message
            st.session_state["encoded_messages"][encoded_message] = user_message
            st.write(f"**Encoded Message:** {encoded_message}")
        else:
            st.error("Please enter a valid message.")

elif mode == "Decode":
    encoded_message = st.text_input("Enter the encoded message to decode:")
    if st.button("Decode"):
        # Search for the encoded message in the dictionary
        original_message = st.session_state["encoded_messages"].get(encoded_message)
        if original_message:
            st.write(f"**Original Message:** {original_message}")
        else:
            st.error("Encoded message not found in the dictionary. Please encode a message first.")
