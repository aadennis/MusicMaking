"""
General MIDI (GM) drum map definitions with ergonomic codes.

This module provides a mapping between readable drum codes and their corresponding
MIDI note numbers according to the GM Level 1 Percussion Key Map.

Example codes:
    "BD1": 36  # Bass Drum 1
    "ASN": 38  # Acoustic Snare
    "LFT": 41  # Low Floor Tom
    "CHH": 42  # Closed Hi-Hat

Full GM Drum Map Reference:
    35: Acoustic Bass Drum    41: Low Floor Tom    47: Low-Mid Tom
    36: Bass Drum 1          42: Closed Hi-Hat    48: Hi-Mid Tom
    37: Side Stick          43: High Floor Tom    49: Crash Cymbal 1
    38: Acoustic Snare      44: Pedal Hi-Hat     50: High Tom
    39: Hand Clap          45: Low Tom          51: Ride Cymbal 1
    40: Electric Snare     46: Open Hi-Hat      52: Chinese Cymbal
"""

# GM drum map with ergonomic codes - maps readable codes to MIDI note numbers
GM_DRUMS = {
    # Kick and Snare Family
    "ABD": 35,  # Acoustic Bass Drum
    "BD1": 36,  # Bass Drum 1
    "SSK": 37,  # Side Stick
    "ASN": 38,  # Acoustic Snare
    "HCP": 39,  # Hand Clap
    "ESN": 40,  # Electric Snare
    
    # Tom Family
    "LFT": 41,  # Low Floor Tom
    "HFT": 43,  # High Floor Tom
    "LTM": 45,  # Low Tom
    "LMT": 47,  # Low-Mid Tom
    "HMT": 48,  # Hi-Mid Tom
    "HTM": 50,  # High Tom
    
    # Hi-Hat Family
    "CHH": 42,  # Closed Hi-Hat
    "PHH": 44,  # Pedal Hi-Hat
    "OHH": 46,  # Open Hi-Hat
    
    # Cymbal Family
    "CC1": 49,  # Crash Cymbal 1
    "RC1": 51,  # Ride Cymbal 1
    "CHC": 52,  # Chinese Cymbal
    "RBL": 53,  # Ride Bell
    "TMB": 54,  # Tambourine
    "SPC": 55,  # Splash Cymbal
    "CC2": 57,  # Crash Cymbal 2
    "RC2": 59,  # Ride Cymbal 2
    
    # Latin Percussion
    "CWB": 56,  # Cowbell
    "VBS": 58,  # Vibraslap
    "HBO": 60,  # High Bongo
    "LBO": 61,  # Low Bongo
    "MHC": 62,  # Mute High Conga
    "OHC": 63,  # Open High Conga
    "LCO": 64,  # Low Conga
    "HTI": 65,  # High Timbale
    "LTI": 66,  # Low Timbale
    "HAG": 67,  # High Agogo
    "LAG": 68,  # Low Agogo
    "CAB": 69,  # Cabasa
    "MAR": 70,  # Maracas
    
    # Whistles and Guiros
    "SWH": 71,  # Short Whistle
    "LWH": 72,  # Long Whistle
    "SGU": 73,  # Short Guiro
    "LGU": 74,  # Long Guiro
    
    # Wooden and Miscellaneous
    "CLV": 75,  # Claves
    "HWB": 76,  # High Woodblock
    "LWB": 77,  # Low Woodblock
    "MCU": 78,  # Mute Cuica
    "OCU": 79,  # Open Cuica
    "MTG": 80,  # Mute Triangle
    "OTG": 81,  # Open Triangle
}

# Common drum groups for easy reference
BASIC_KIT = ["BD1", "ASN", "CHH", "OHH"]  # Basic rock kit
TOMS = ["LFT", "HFT", "LTM", "LMT", "HMT", "HTM"]  # All toms
CYMBALS = ["CC1", "RC1", "CHC", "CC2", "RC2"]  # Main cymbals
LATIN = ["CWB", "HBO", "LBO", "MHC", "OHC", "LCO", "HTI", "LTI"]  # Latin percussion