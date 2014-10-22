from midi import getMIDI
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
    testJSON = """
    {
        "tempo":500000,
        "instruments":[
                          {"channel":0, "instrumentID":0}
                      ],
        "notes":[
                     {"delta":0, "channel":0, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":0, "noteID":69, "volume":127, "noteDown":false}
                ]
    }"""
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
    
    midiObtained = getMIDI(testJSON)
    assert actualMIDI == midiObtained, "One note MIDI file"
    
def test_multi_channel():
    testJSON = """
    {
        "tempo":500000,
        "instruments":[
                          {"channel":0, "instrumentID":0},
                          {"channel":1, "instrumentID":4},
                          {"channel":2, "instrumentID":20},
                          {"channel":3, "instrumentID":28},
                          {"channel":4, "instrumentID":65},
                          {"channel":5, "instrumentID":70},
                          {"channel":6, "instrumentID":72},
                          {"channel":7, "instrumentID":77},
                          {"channel":8, "instrumentID":80},
                          {"channel":9, "instrumentID":57},
                          {"channel":10,"instrumentID":81},
                          {"channel":11,"instrumentID":18},
                          {"channel":12,"instrumentID":51},
                          {"channel":13,"instrumentID":58},
                          {"channel":14,"instrumentID":25},
                          {"channel":15,"instrumentID":68}
                      ],
        "notes":[
                     {"delta":0, "channel":0, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":0, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":1, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":1, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":2, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":2, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":3, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":3, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":4, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":4, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":5, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":5, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":6, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":6, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":7, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":7, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":8, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":8, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":9, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":9, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":10, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":10, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":11, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":11, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":12, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":12, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":13, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":13, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":14, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":14, "noteID":69, "volume":127, "noteDown":false},
                     {"delta":0, "channel":15, "noteID":69, "volume":127, "noteDown":true},
                     {"delta":96, "channel":15, "noteID":69, "volume":127, "noteDown":false}
                ]
    }"""
    
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
                             0x00, 0xC9, 0x39,
                             0x00, 0xCA, 0x51,
                             0x00, 0xCB, 0x12,
                             0x00, 0xCC, 0x33,
                             0x00, 0xCD, 0x3A,
                             0x00, 0xCE, 0x19,
                             0x00, 0xCF, 0x44,
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
                             0x00, 0x99, 0x45, 0x7F,
                             0x60, 0x89, 0x45, 0x7F,
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
                             
    trackLength = bytearray([0x00, 0x00, 0x00, 0xC3])
    
    actualMIDI = copy(headerChunk)
    actualMIDI.extend(trackHeader)
    actualMIDI.extend(trackLength)
    actualMIDI.extend(trackEvents)
    
    midiObtained = getMIDI(testJSON)
    assert actualMIDI == midiObtained, "Multi channel midi"
    
def test_many_notes():
    testJSON = """
    {
        "tempo":500000,
        "instruments":[
                          {"channel":0, "instrumentID":0}
                      ],
        "notes":[
                     {"delta":0, "channel":0, "noteID":57, "volume":127, "noteDown":true},
                     {"delta":0, "channel":0, "noteID":59, "volume":127, "noteDown":true},
                     {"delta":0, "channel":0, "noteID":60, "volume":127, "noteDown":true},
                     {"delta":0, "channel":0, "noteID":62, "volume":127, "noteDown":true},
                     {"delta":0, "channel":0, "noteID":64, "volume":127, "noteDown":true},
                     {"delta":0, "channel":0, "noteID":65, "volume":127, "noteDown":true},
                     {"delta":0, "channel":0, "noteID":67, "volume":127, "noteDown":true},
                     {"delta":96, "channel":0, "noteID":57, "volume":127, "noteDown":false},
                     {"delta":96, "channel":0, "noteID":59, "volume":127, "noteDown":false},
                     {"delta":96, "channel":0, "noteID":60, "volume":127, "noteDown":false},
                     {"delta":96, "channel":0, "noteID":62, "volume":127, "noteDown":false},
                     {"delta":96, "channel":0, "noteID":64, "volume":127, "noteDown":false},
                     {"delta":96, "channel":0, "noteID":65, "volume":127, "noteDown":false},
                     {"delta":96, "channel":0, "noteID":67, "volume":127, "noteDown":false}
                ]
    }"""
    
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
                             0x60, 0x80, 0x3B, 0x7F,
                             0x60, 0x80, 0x3C, 0x7F,
                             0x60, 0x80, 0x3E, 0x7F,
                             0x60, 0x80, 0x40, 0x7F,
                             0x60, 0x80, 0x41, 0x7F,
                             0x60, 0x80, 0x43, 0x7F,
                             0x00, 0xFF, 0x2F, 0x00])
                             
    trackLength = bytearray([0x00, 0x00, 0x00, 0x4E])
    
    actualMIDI = copy(headerChunk)
    actualMIDI.extend(trackHeader)
    actualMIDI.extend(trackLength)
    actualMIDI.extend(trackEvents)
    
    midiObtained = getMIDI(testJSON)
    assert actualMIDI == midiObtained, "Multi note MIDI file"
    
def test_delta_values():
    testJSON = """
    {
        "tempo":500000,
        "instruments":[
                          {"channel":0, "instrumentID":0}
                      ],
        "notes":[
                     {"delta":0, "channel":0, "noteID":57, "volume":127, "noteDown":true},
                     {"delta":1, "channel":0, "noteID":57, "volume":127, "noteDown":false},
                     {"delta":0, "channel":0, "noteID":57, "volume":127, "noteDown":true},
                     {"delta":48, "channel":0, "noteID":57, "volume":127, "noteDown":false},
                     {"delta":0, "channel":0, "noteID":57, "volume":127, "noteDown":true},
                     {"delta":96, "channel":0, "noteID":57, "volume":127, "noteDown":false},
                     {"delta":0, "channel":0, "noteID":57, "volume":127, "noteDown":true},
                     {"delta":127, "channel":0, "noteID":57, "volume":127, "noteDown":false},
                     {"delta":0, "channel":0, "noteID":57, "volume":127, "noteDown":true},
                     {"delta":128, "channel":0, "noteID":57, "volume":127, "noteDown":false},
                     {"delta":0, "channel":0, "noteID":57, "volume":127, "noteDown":true},
                     {"delta":137, "channel":0, "noteID":57, "volume":127, "noteDown":false},
                     {"delta":0, "channel":0, "noteID":57, "volume":127, "noteDown":true},
                     {"delta":1056118, "channel":0, "noteID":57, "volume":127, "noteDown":false},
                     {"delta":0, "channel":0, "noteID":57, "volume":127, "noteDown":true},
                     {"delta":34656598, "channel":0, "noteID":57, "volume":127, "noteDown":false}
                ]
    }"""
    
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
    
    midiObtained = getMIDI(testJSON)
    assert actualMIDI == midiObtained, "Different delta values"