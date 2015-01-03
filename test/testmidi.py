from midi import getMIDI, MIDIError
from copy import copy

HEAD_CHUNK_ID   = bytearray([0x4D, 0x54, 0x68, 0x64])
HEAD_CHUNK_SIZE = bytearray([0x00, 0x00, 0x00, 0x06])
MIDI_FORMAT     = bytearray([0x00, 0x00])
MIDI_TRACKS     = bytearray([0x00, 0x01])
TIME_DIV        = bytearray([0x00, 0x60])

#Build up the complete header chunk
headerChunk = HEAD_CHUNK_ID
headerChunk.extend(HEAD_CHUNK_SIZE)
headerChunk.extend(MIDI_FORMAT)
headerChunk.extend(MIDI_TRACKS)
headerChunk.extend(TIME_DIV)

trackHeader = bytearray([0x4D, 0x54, 0x72, 0x6B])

#test the most basic midi file - a single note
def test_one_note_midi():
    testJSON = {
        "head": {"subDivisions":96, "tempo":120},
        "tracks": [
            {
                "instrument":0,
                "notes": [
                    {"id":1, "pos":0, "length":96, "pitch":69}
                ]
            }
        ]
    }
    
    trackEvents = bytearray([0x00, 0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08,
                             0x00, 0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20,
                             0x00, 0xC0, 0x00,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x45, 0x7F,
                             0x00, 0xFF, 0x2F, 0x00])
                             
    trackLength = bytearray([0x00, 0x00, 0x00, 0x1E])
    
    actualMIDI = copy(headerChunk)
    actualMIDI.extend(trackHeader)
    actualMIDI.extend(trackLength)
    actualMIDI.extend(trackEvents)
    
    midiObtained = getMIDI(testJSON)["midi"]
    assert actualMIDI == midiObtained, "One note MIDI file"
    
def test_multi_channel():
    testJSON = {
        "head": {"subDivisions":96, "tempo":120},
        "tracks": [
            {
                "instrument":0,
                "notes": [
                    {"pos":0, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":4,
                "notes": [
                    {"pos":96, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":20,
                "notes": [
                    {"pos":192, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":28,
                "notes": [
                    {"pos":288, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":65,
                "notes": [
                    {"pos":384, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":70,
                "notes": [
                    {"pos":480, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":72,
                "notes": [
                    {"pos":576, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":77,
                "notes": [
                    {"pos":672, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":80,
                "notes": [
                    {"pos":768, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":57,
                "notes": [
                    {"pos":864, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":81,
                "notes": [
                    {"pos":960, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":18,
                "notes": [
                    {"pos":1056, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":51,
                "notes": [
                    {"pos":1152, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":58,
                "notes": [
                    {"pos":1248, "length":96, "pitch":69}
                ]
            },
            {
                "instrument":25,
                "notes": [
                    {"pos":1344, "length":96, "pitch":69}
                ]
            }
        ]
    }
    
    trackEvents = bytearray([0x00, 0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08,
                             0x00, 0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20,
                             0x00, 0xC0, 0x00,
                             0x00, 0xC1, 0x04,
                             0x00, 0xC2, 0x14,
                             0x00, 0xC3, 0x1C,
                             0x00, 0xC4, 0x41,
                             0x00, 0xC5, 0x46,
                             0x00, 0xC6, 0x48,
                             0x00, 0xC7, 0x4D,
                             0x00, 0xC8, 0x50,
                             0x00, 0xCA, 0x39,
                             0x00, 0xCB, 0x51,
                             0x00, 0xCC, 0x12,
                             0x00, 0xCD, 0x33,
                             0x00, 0xCE, 0x3A,
                             0x00, 0xCF, 0x19,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x45, 0x7F,
                             0x00, 0x91, 0x45, 0x7F,
                             0x60, 0x81, 0x45, 0x7F,
                             0x00, 0x92, 0x45, 0x7F,
                             0x60, 0x82, 0x45, 0x7F,
                             0x00, 0x93, 0x45, 0x7F,
                             0x60, 0x83, 0x45, 0x7F,
                             0x00, 0x94, 0x45, 0x7F,
                             0x60, 0x84, 0x45, 0x7F,
                             0x00, 0x95, 0x45, 0x7F,
                             0x60, 0x85, 0x45, 0x7F,
                             0x00, 0x96, 0x45, 0x7F,
                             0x60, 0x86, 0x45, 0x7F,
                             0x00, 0x97, 0x45, 0x7F,
                             0x60, 0x87, 0x45, 0x7F,
                             0x00, 0x98, 0x45, 0x7F,
                             0x60, 0x88, 0x45, 0x7F,
                             0x00, 0x9A, 0x45, 0x7F,
                             0x60, 0x8A, 0x45, 0x7F,
                             0x00, 0x9B, 0x45, 0x7F,
                             0x60, 0x8B, 0x45, 0x7F,
                             0x00, 0x9C, 0x45, 0x7F,
                             0x60, 0x8C, 0x45, 0x7F,
                             0x00, 0x9D, 0x45, 0x7F,
                             0x60, 0x8D, 0x45, 0x7F,
                             0x00, 0x9E, 0x45, 0x7F,
                             0x60, 0x8E, 0x45, 0x7F,
                             0x00, 0x9F, 0x45, 0x7F,
                             0x60, 0x8F, 0x45, 0x7F,
                             0x00, 0xFF, 0x2F, 0x00])
                             
    trackLength = bytearray([0x00, 0x00, 0x00, 0xB8])
    
    actualMIDI = copy(headerChunk)
    actualMIDI.extend(trackHeader)
    actualMIDI.extend(trackLength)
    actualMIDI.extend(trackEvents)
    
    midiObtained = getMIDI(testJSON)["midi"]
    assert actualMIDI == midiObtained, "Multi channel midi"
    
def test_many_notes():
    testJSON = {
        "head": {"subDivisions":96, "tempo":120},
        "tracks": [
            {
                "instrument":0,
                "notes": [
                    {"pos":0, "length":96, "pitch":57},
                    {"pos":0, "length":96, "pitch":59},
                    {"pos":0, "length":96, "pitch":60},
                    {"pos":0, "length":96, "pitch":62},
                    {"pos":0, "length":96, "pitch":64},
                    {"pos":0, "length":96, "pitch":65},
                    {"pos":0, "length":96, "pitch":67}
                ]
            }
        ]
    }
    
    trackEvents = bytearray([0x00, 0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08,
                             0x00, 0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20,
                             0x00, 0xC0, 0x00,
                             0x00, 0x90, 0x39, 0x7F,
                             0x00, 0x90, 0x3B, 0x7F,
                             0x00, 0x90, 0x3C, 0x7F,
                             0x00, 0x90, 0x3E, 0x7F,
                             0x00, 0x90, 0x40, 0x7F,
                             0x00, 0x90, 0x41, 0x7F,
                             0x00, 0x90, 0x43, 0x7F,
                             0x60, 0x80, 0x39, 0x7F,
                             0x00, 0x80, 0x3B, 0x7F,
                             0x00, 0x80, 0x3C, 0x7F,
                             0x00, 0x80, 0x3E, 0x7F,
                             0x00, 0x80, 0x40, 0x7F,
                             0x00, 0x80, 0x41, 0x7F,
                             0x00, 0x80, 0x43, 0x7F,
                             0x00, 0xFF, 0x2F, 0x00])
                             
    trackLength = bytearray([0x00, 0x00, 0x00, 0x4E])
    
    actualMIDI = copy(headerChunk)
    actualMIDI.extend(trackHeader)
    actualMIDI.extend(trackLength)
    actualMIDI.extend(trackEvents)
    
    midiObtained = getMIDI(testJSON)["midi"]
    assert actualMIDI == midiObtained, "Multi note MIDI file"
    
def test_delta_values():
    testJSON = {
        "head": {"subDivisions":96, "tempo":120},
        "tracks": [
            {
                "instrument":0,
                "notes": [
                    {"pos":0, "length":1, "pitch":57},
                    {"pos":1, "length":48, "pitch":57},
                    {"pos":49, "length":96, "pitch":57},
                    {"pos":145, "length":127, "pitch":57},
                    {"pos":272, "length":128, "pitch":57},
                    {"pos":400, "length":137, "pitch":57},
                    {"pos":537, "length":1056118, "pitch":57},
                    {"pos":1056655, "length":34656598, "pitch":57}
                ]
            }
        ]
    }
    
    trackEvents = bytearray([0x00, 0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08,
                             0x00, 0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20,
                             0x00, 0xC0, 0x00,
                             0x00, 0x90, 0x39, 0x7F,
                             0x01, 0x80, 0x39, 0x7F,
                             0x00, 0x90, 0x39, 0x7F,
                             0x30, 0x80, 0x39, 0x7F,
                             0x00, 0x90, 0x39, 0x7F,
                             0x60, 0x80, 0x39, 0x7F,
                             0x00, 0x90, 0x39, 0x7F,
                             0x7F, 0x80, 0x39, 0x7F,
                             0x00, 0x90, 0x39, 0x7F,
                             0x81, 0x00, 0x80, 0x39, 0x7F,
                             0x00, 0x90, 0x39, 0x7F,
                             0x81, 0x09, 0x80, 0x39, 0x7F,
                             0x00, 0x90, 0x39, 0x7F,
                             0xC0, 0xBA, 0x76, 0x80, 0x39, 0x7F,
                             0x00, 0x90, 0x39, 0x7F,
                             0x90, 0xC3, 0xA2, 0x56, 0x80, 0x39, 0x7F,
                             0x00, 0xFF, 0x2F, 0x00])
                             
    trackLength = bytearray([0x00, 0x00, 0x00, 0x5D])
    
    actualMIDI = copy(headerChunk)
    actualMIDI.extend(trackHeader)
    actualMIDI.extend(trackLength)
    actualMIDI.extend(trackEvents)
    
    midiObtained = getMIDI(testJSON)["midi"]
    assert actualMIDI == midiObtained, "Different delta values"
    
#test when the JSON notes are out of order
def test_out_of_order():
    testJSON = {
        "head": {"subDivisions":96, "tempo":120},
        "tracks": [
            {
                "instrument":0,
                "notes": [
                    {"pos":288, "length":96, "pitch":69},
                    {"pos":0, "length":96, "pitch":69},
                    {"pos":192, "length":96, "pitch":69},
                    {"pos":96, "length":96, "pitch":69}
                ]
            }
        ]
    }
    
    trackEvents = bytearray([0x00, 0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08,
                             0x00, 0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20,
                             0x00, 0xC0, 0x00,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x45, 0x7F,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x45, 0x7F,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x45, 0x7F,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x45, 0x7F,
                             0x00, 0xFF, 0x2F, 0x00])
                             
    trackLength = bytearray([0x00, 0x00, 0x00, 0x36])
    
    actualMIDI = copy(headerChunk)
    actualMIDI.extend(trackHeader)
    actualMIDI.extend(trackLength)
    actualMIDI.extend(trackEvents)
    
    midiObtained = getMIDI(testJSON)["midi"]
    assert actualMIDI == midiObtained, "Out of order"
    
#test when the JSON notes are out of order
def test_out_of_order_2():
    testJSON = {
        "head": {"subDivisions":96, "tempo":120},
        "tracks": [
            {
                "instrument":0,
                "notes": [
                    {"pos":384, "length":96, "pitch":69},
                    {"pos":0, "length":384, "pitch":70},
                    {"pos":96, "length":96, "pitch":69},
                    {"pos":288, "length":96, "pitch":69},
                    {"pos":0, "length":96, "pitch":69},
                    {"pos":192, "length":96, "pitch":69}
                ]
            }
        ]
    }
    
    trackEvents = bytearray([0x00, 0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08,
                             0x00, 0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20,
                             0x00, 0xC0, 0x00,
                             0x00, 0x90, 0x46, 0x7F,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x45, 0x7F,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x45, 0x7F,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x45, 0x7F,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x46, 0x7F,
                             0x00, 0x80, 0x45, 0x7F,
                             0x00, 0x90, 0x45, 0x7F,
                             0x60, 0x80, 0x45, 0x7F,
                             0x00, 0xFF, 0x2F, 0x00])
                             
    trackLength = bytearray([0x00, 0x00, 0x00, 0x46])
    
    actualMIDI = copy(headerChunk)
    actualMIDI.extend(trackHeader)
    actualMIDI.extend(trackLength)
    actualMIDI.extend(trackEvents)
    
    midiObtained = getMIDI(testJSON)["midi"]
    assert actualMIDI == midiObtained, "Out of order"
    
def test_bad_json_formats():
    JSON = {}
    try:
        getMIDI(JSON)["midi"]
        assert False, "No Head"
    except MIDIError as exep:
        assert exep.message == "Invalid Jingle JSON format. Missing 'head'", "No Head"
        
    JSON = {"head": {"cats":2, "dogs":3}}
    try:
        getMIDI(JSON)["midi"]
        assert False, "No Subdivisions"
    except MIDIError as exep:
        assert exep.message == "Invalid Jingle JSON format. Missing 'subDivisions' from head", "No SubDivisions"
        
    JSON = {"head": {"subDivisions":2, "dogs":3}}
    try:
        getMIDI(JSON)["midi"]
        assert False, "No Tempo"
    except MIDIError as exep:
        assert exep.message == "Invalid Jingle JSON format. Missing 'tempo' from head", "No Tempo"
        
    JSON = {"head": {"subDivisions":65536, "tempo":120}}
    try:
        getMIDI(JSON)["midi"]
        assert False, "too many Subdivisions"
    except MIDIError as exep:
        assert exep.message == "subDivisions is too large. Maximum value is 65535", "too many SubDivisions"
        
    JSON = {"head": {"subDivisions":65535, "tempo":3}}
    try:
        getMIDI(JSON)["midi"]
        assert False, "tempo too small"
    except MIDIError as exep:
        assert exep.message == "tempo is too small. Minimum value is 4", "tempo too small"
        
    JSON = {"head": {"subDivisions":65535, "tempo":0}}
    try:
        getMIDI(JSON)["midi"]
        assert False, "tempo too small"
    except MIDIError as exep:
        assert exep.message == "tempo is too small. Minimum value is 4", "tempo too small"
        
    JSON = {"head": {"subDivisions":0, "tempo":4}}
    try:
        getMIDI(JSON)["midi"]
        assert False, "subdivisions too small"
    except MIDIError as exep:
        assert exep.message == "subDivisions is too small. Minimum value is 1", "subDivisions too small"
        
    JSON = {"head": {"subDivisions":1, "tempo":4}}
    try:
        getMIDI(JSON)["midi"]
        assert False, "no tracks"
    except MIDIError as exep:
        assert exep.message == "Invalid Jingle JSON format. Missing 'tracks'", "no tracks"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [{"notes":[{"pos":0, "length":0, "pitch":0}]}]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "no instrument"
    except MIDIError as exep:
        assert exep.message == "Invalid Jingle JSON format. Missing 'instrument' from track", "no instrument"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0}
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "no notes"
    except MIDIError as exep:
        assert exep.message == "Invalid Jingle JSON format. Missing 'notes' from track", "no notes"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":-1,
                 "notes": [
                 
                 ]}
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "bad instrument"
    except MIDIError as exep:
        assert exep.message == "Invalid instrument number. Must be in range of 0 to 127", "bad instrument"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":128,
                 "notes": [
                 
                 ]}
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "bad instrument"
    except MIDIError as exep:
        assert exep.message == "Invalid instrument number. Must be in range of 0 to 127", "bad instrument"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0,
                 "notes": [
                    {}
                 ]}
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "no position"
    except MIDIError as exep:
        assert exep.message == "Invalid Jingle JSON format. Missing 'pos' from notes", "no position"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0,
                 "notes": [
                    {"pos":0}
                 ]}
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "no length"
    except MIDIError as exep:
        assert exep.message == "Invalid Jingle JSON format. Missing 'length' from notes", "no length"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":96}
                 ]}
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "no note"
    except MIDIError as exep:
        assert exep.message == "Invalid Jingle JSON format. Missing 'pitch' from notes", "no note"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":96, "pitch":-1}
                 ]}
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "bad note"
    except MIDIError as exep:
        assert exep.message == "Invalid note number. Must be in range of 0 to 127", "bad note"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":96, "pitch":128}
                 ]}
            ]}
    try:
        getMIDI(JSON)
        assert False, "bad note"["midi"]
    except MIDIError as exep:
        assert exep.message == "Invalid note number. Must be in range of 0 to 127", "bad note"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0,
                 "notes": [
                    {"pos":-1, "length":96, "pitch":0}
                 ]}
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "bad position"
    except MIDIError as exep:
        assert exep.message == "Invalid pos. Must not be negative", "bad position"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":-1, "pitch":0}
                 ]}
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "bad length"
    except MIDIError as exep:
        assert exep.message == "Invalid length. Must not be negative", "bad length"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":1, "pitch":127}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                }
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "too many tracks"
    except MIDIError as exep:
        assert exep.message == "Too many tracks. Maximum number of tracks is 15", "too many tracks"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":127}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":268435456, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                },
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":0, "pitch":0}
                 ]
                }
            ]}
    try:
        getMIDI(JSON)["midi"]
        assert False, "just bad"
    except MIDIError as exep:
        assert exep.message == "A delta value was too big. The maximum difference in position values is 268,435,455 subdivisions", "just bad"
        
    JSON = {"head": {"subDivisions":1, "tempo":4},
     "tracks": [
                {"instrument":0,
                 "notes": [
                    {"pos":0, "length":268435455, "pitch":0}
                 ]}
            ]}
    try:
        midi = getMIDI(JSON)["midi"]
        assert True, "pass test"
    except MIDIError as exep:
        assert False, "pass test"
