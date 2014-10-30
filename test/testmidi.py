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
        "subDivisions":96,
        "tempo":120,
        "instruments":[
                          {"chan":0, "inst":0}
                      ],
        "notes":[
                     {"id":1, "pos":0, "chan":0, "note":69, "vol":127, "noteOn":true},
                     {"id":1, "pos":96, "chan":0, "note":69, "vol":127, "noteOn":false}
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
        "subDivisions":96,
        "tempo":120,
        "instruments":[
                          {"chan":0, "inst":0},
                          {"chan":1, "inst":4},
                          {"chan":2, "inst":20},
                          {"chan":3, "inst":28},
                          {"chan":4, "inst":65},
                          {"chan":5, "inst":70},
                          {"chan":6, "inst":72},
                          {"chan":7, "inst":77},
                          {"chan":8, "inst":80},
                          {"chan":9, "inst":57},
                          {"chan":10,"inst":81},
                          {"chan":11,"inst":18},
                          {"chan":12,"inst":51},
                          {"chan":13,"inst":58},
                          {"chan":14,"inst":25},
                          {"chan":15,"inst":68}
                      ],
        "notes":[
                     {"pos":0, "chan":0, "note":69, "vol":127, "noteOn":true},
                     {"pos":96, "chan":0, "note":69, "vol":127, "noteOn":false},
                     {"pos":96, "chan":1, "note":69, "vol":127, "noteOn":true},
                     {"pos":192, "chan":1, "note":69, "vol":127, "noteOn":false},
                     {"pos":192, "chan":2, "note":69, "vol":127, "noteOn":true},
                     {"pos":288, "chan":2, "note":69, "vol":127, "noteOn":false},
                     {"pos":288, "chan":3, "note":69, "vol":127, "noteOn":true},
                     {"pos":384, "chan":3, "note":69, "vol":127, "noteOn":false},
                     {"pos":384, "chan":4, "note":69, "vol":127, "noteOn":true},
                     {"pos":480, "chan":4, "note":69, "vol":127, "noteOn":false},
                     {"pos":480, "chan":5, "note":69, "vol":127, "noteOn":true},
                     {"pos":576, "chan":5, "note":69, "vol":127, "noteOn":false},
                     {"pos":576, "chan":6, "note":69, "vol":127, "noteOn":true},
                     {"pos":672, "chan":6, "note":69, "vol":127, "noteOn":false},
                     {"pos":672, "chan":7, "note":69, "vol":127, "noteOn":true},
                     {"pos":768, "chan":7, "note":69, "vol":127, "noteOn":false},
                     {"pos":768, "chan":8, "note":69, "vol":127, "noteOn":true},
                     {"pos":864, "chan":8, "note":69, "vol":127, "noteOn":false},
                     {"pos":864, "chan":9, "note":69, "vol":127, "noteOn":true},
                     {"pos":960, "chan":9, "note":69, "vol":127, "noteOn":false},
                     {"pos":960, "chan":10, "note":69, "vol":127, "noteOn":true},
                     {"pos":1056, "chan":10, "note":69, "vol":127, "noteOn":false},
                     {"pos":1056, "chan":11, "note":69, "vol":127, "noteOn":true},
                     {"pos":1152, "chan":11, "note":69, "vol":127, "noteOn":false},
                     {"pos":1152, "chan":12, "note":69, "vol":127, "noteOn":true},
                     {"pos":1248, "chan":12, "note":69, "vol":127, "noteOn":false},
                     {"pos":1248, "chan":13, "note":69, "vol":127, "noteOn":true},
                     {"pos":1344, "chan":13, "note":69, "vol":127, "noteOn":false},
                     {"pos":1344, "chan":14, "note":69, "vol":127, "noteOn":true},
                     {"pos":1440, "chan":14, "note":69, "vol":127, "noteOn":false},
                     {"pos":1440, "chan":15, "note":69, "vol":127, "noteOn":true},
                     {"pos":1536, "chan":15, "note":69, "vol":127, "noteOn":false}
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
        "subDivisions":96,
        "tempo":120,
        "instruments":[
                          {"chan":0, "inst":0}
                      ],
        "notes":[
                     {"pos":0, "chan":0, "note":57, "vol":127, "noteOn":true},
                     {"pos":0, "chan":0, "note":59, "vol":127, "noteOn":true},
                     {"pos":0, "chan":0, "note":60, "vol":127, "noteOn":true},
                     {"pos":0, "chan":0, "note":62, "vol":127, "noteOn":true},
                     {"pos":0, "chan":0, "note":64, "vol":127, "noteOn":true},
                     {"pos":0, "chan":0, "note":65, "vol":127, "noteOn":true},
                     {"pos":0, "chan":0, "note":67, "vol":127, "noteOn":true},
                     {"pos":96, "chan":0, "note":57, "vol":127, "noteOn":false},
                     {"pos":96, "chan":0, "note":59, "vol":127, "noteOn":false},
                     {"pos":96, "chan":0, "note":60, "vol":127, "noteOn":false},
                     {"pos":96, "chan":0, "note":62, "vol":127, "noteOn":false},
                     {"pos":96, "chan":0, "note":64, "vol":127, "noteOn":false},
                     {"pos":96, "chan":0, "note":65, "vol":127, "noteOn":false},
                     {"pos":96, "chan":0, "note":67, "vol":127, "noteOn":false}
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
    
    midiObtained = getMIDI(testJSON)
    assert actualMIDI == midiObtained, "Multi note MIDI file"
    
def test_delta_values():
    testJSON = """
    {
        "subDivisions":96,
        "tempo":120,
        "instruments":[
                          {"chan":0, "inst":0}
                      ],
        "notes":[
                     {"pos":0, "chan":0, "note":57, "vol":127, "noteOn":true},
                     {"pos":1, "chan":0, "note":57, "vol":127, "noteOn":false},
                     {"pos":1, "chan":0, "note":57, "vol":127, "noteOn":true},
                     {"pos":49, "chan":0, "note":57, "vol":127, "noteOn":false},
                     {"pos":49, "chan":0, "note":57, "vol":127, "noteOn":true},
                     {"pos":145, "chan":0, "note":57, "vol":127, "noteOn":false},
                     {"pos":145, "chan":0, "note":57, "vol":127, "noteOn":true},
                     {"pos":272, "chan":0, "note":57, "vol":127, "noteOn":false},
                     {"pos":272, "chan":0, "note":57, "vol":127, "noteOn":true},
                     {"pos":400, "chan":0, "note":57, "vol":127, "noteOn":false},
                     {"pos":400, "chan":0, "note":57, "vol":127, "noteOn":true},
                     {"pos":537, "chan":0, "note":57, "vol":127, "noteOn":false},
                     {"pos":537, "chan":0, "note":57, "vol":127, "noteOn":true},
                     {"pos":1056655, "chan":0, "note":57, "vol":127, "noteOn":false},
                     {"pos":1056655, "chan":0, "note":57, "vol":127, "noteOn":true},
                     {"pos":35713253, "chan":0, "note":57, "vol":127, "noteOn":false}
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
    
#test when the JSON notes are out of order
def test_out_of_order():
    testJSON = """
    {
        "subDivisions":96,
        "tempo":120,
        "instruments":[
                          {"chan":0, "inst":0}
                      ],
        "notes":[
                     {"id":3, "pos":288, "chan":0, "note":69, "vol":127, "noteOn":false},
                     {"id":4, "pos":288, "chan":0, "note":69, "vol":127, "noteOn":true},
                     {"id":1, "pos":0, "chan":0, "note":69, "vol":127, "noteOn":true},
                     {"id":4, "pos":384, "chan":0, "note":69, "vol":127, "noteOn":false},
                     {"id":2, "pos":192, "chan":0, "note":69, "vol":127, "noteOn":false},
                     {"id":3, "pos":192, "chan":0, "note":69, "vol":127, "noteOn":true},
                     {"id":1, "pos":96, "chan":0, "note":69, "vol":127, "noteOn":false},
                     {"id":2, "pos":96, "chan":0, "note":69, "vol":127, "noteOn":true}
                ]
    }"""
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
    
    midiObtained = getMIDI(testJSON)
    assert actualMIDI == midiObtained, "Out of order"