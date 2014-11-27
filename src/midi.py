import json
import base64

class MIDIError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

#function to convert a decimal number to an array of bytes
#takes a number to convert and the number of bytes in the returned array
#raises MIDIError if the number is too big for the given number of bytes
def numberToByteArray(number, bytes):
    bits = 8 * bytes
    if number > 2**bits - 1:
        raise MIDIError("Not Enough Bytes")
    
    byteArr = bytearray(bytes)
    bytes -= 1
    count = 0
    currentTotal = 0
    while number != 0:
        if count == 8:
            count = 0
            byteArr[bytes] = currentTotal
            bytes -= 1
            currentTotal = 0
            
        if number%2:
            currentTotal += 2**count
            
        count += 1
        number = number / 2
        
    byteArr[bytes] = currentTotal
    return byteArr

#function takes a delta time value and returns an array of bytes in variable
#length quantity format. VLQ represents numbers with 7 bits where the 8th bit
#is set to 1 if there is a following byte or 0 if it's the last byte
#eg 480 normally looks like: 00000001 11100000
#but with VLQ it looks like: 10000011 01100000
def getVLQ(delta):
    count = 0
    currentTotal = 0
    VLQ = bytearray()
    while delta != 0:
        if count == 7:
            count = 0
            VLQ.insert(0, currentTotal + 128) #set the 8th bit on all bytes
            currentTotal = 0
            
        if delta%2:
            currentTotal += 2**count
            
        count += 1
        delta = delta / 2
    
    VLQ.insert(0, currentTotal + 128)
    VLQ[-1] -= 128 #unset the 8th bit for the last byte
    return VLQ

#function takes a jingle JSON and returns an array of bytes which make up the
#MIDI file for that jingle.
#raises MIDIError if there is a problem creating the MIDI file
def getMIDI(midiJSON):
    midi = json.loads(midiJSON) #load the JSON as a python dictionary
    
    #The following bytes make up the head of a MIDI file
    HEAD_CHUNK_ID   = bytearray([0x4D, 0x54, 0x68, 0x64])   #MIDI Magic Number "MThd"
    HEAD_CHUNK_SIZE = bytearray([0x00, 0x00, 0x00, 0x06])   #Head chunk is always 6 bytes in length
    MIDI_FORMAT     = bytearray([0x00, 0x00])               #We are using format 0
    MIDI_TRACKS     = bytearray([0x00, 0x01])               #Format 0 only uses 1 track
    
    if not 'head' in midi:
        raise MIDIError("Invalid Jingle JSON format. Missing 'head'")
    
    midiHead = midi['head']
    
    if not 'subdivisions' in midiHead:
        raise MIDIError("Invalid Jingle JSON format. Missing 'subdivisions' from head")
    
    if midiHead['subdivisions'] < 1:
        raise MIDIError("subdivisions is too small. Minimum value is 1")
    
    TIME_DIV = None;
    try:
        #time division is stored as 2 bytes
        TIME_DIV = numberToByteArray(midiHead['subdivisions'], 2)
    except MIDIError as exep:
        raise MIDIError("subdivisions is too large. Maximum value is 65535")

    #Build up the complete header chunk
    HEADER_CHUNK = HEAD_CHUNK_ID
    HEADER_CHUNK.extend(HEAD_CHUNK_SIZE)
    HEADER_CHUNK.extend(MIDI_FORMAT)
    HEADER_CHUNK.extend(MIDI_TRACKS)
    HEADER_CHUNK.extend(TIME_DIV)

    #The second chunk is the track itself
    TRACK_CHUNK_ID  = bytearray([0x4D, 0x54, 0x72, 0x6B])   #A track starts with the Magic Number "MTrk"
    #The first event sets the time signature (8 bytes). We use a standard 4 4
    TIME_SIG        = bytearray([0x00, 0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08])
    trackEvents = TIME_SIG #build up the track events

    if not 'tempo' in midiHead:
        raise MIDIError("Invalid Jingle JSON format. Missing 'tempo' from head")
    
    if midiHead['tempo'] < 4:
        raise MIDIError("tempo is too small. Minimum value is 4")
    
    #convert tempo from beats per minute to microseconds per quarter note
    tempoBPM = midiHead['tempo']
    tempoMPQN = 60000000 / tempoBPM

    tempo = numberToByteArray(tempoMPQN, 3)
    tempoEvent = bytearray([0x00, 0xFF, 0x51, 0x03])
    tempoEvent.extend(tempo)
    trackEvents.extend(tempoEvent)

    if not 'tracks' in midi:
        raise MIDIError("Invalid Jingle JSON format. Missing 'tracks'")
    
    midiChannels = midi['tracks']
    #Now set the instruments and collect note events in a list
    currentChannel = 0
    allNoteEvents = []
    for channel in midiChannels:
        if currentChannel == 9:
            #channel 10 (index 9) is for percussion only so skip it
            currentChannel = 10
            
        if currentChannel > 15:
            raise MIDIError("Too many tracks. Maximum number of tracks is 15")
            
        if len(channel) > 0: #need to ignore the empty tracks
            
            if not 'instrument' in channel:
                raise MIDIError("Invalid Jingle JSON format. Missing 'instrument' from track")
            if not 'notes' in channel:
                raise MIDIError("Invalid Jingle JSON format. Missing 'notes' from track")
            
            instrument = channel['instrument']
            notes = channel['notes']
            
            if instrument < 0 or instrument > 127:
                raise MIDIError("Invalid instrument number. Must be in range of 0 to 127")
            
            #here we actually set an instrument to the current channel
            setInstrumentEvent = bytearray([0, 192+currentChannel, instrument])
            trackEvents.extend(setInstrumentEvent)
            
            for noteData in notes:
                if not 'position' in noteData:
                    raise MIDIError("Invalid Jingle JSON format. Missing 'position' from notes")
            
            for noteData in sorted(notes, key=lambda k: k['position']):
                if not 'length' in noteData:
                    raise MIDIError("Invalid Jingle JSON format. Missing 'length' from notes")
                if not 'pitch' in noteData:
                    raise MIDIError("Invalid Jingle JSON format. Missing 'pitch' from notes")
                if noteData['pitch'] < 0 or noteData['pitch'] > 127:
                    raise MIDIError("Invalid pitch number. Must be in range of 0 to 127")
                if noteData['position'] < 0:
                    raise MIDIError("Invalid position. Must not be negative")
                if noteData['length'] < 0:
                    raise MIDIError("Invalid length. Must not be negative")
                    
                noteOnEvent = {
                    "position": noteData['position'],
                    "chan":     currentChannel,
                    "pitch":    noteData['pitch'],
                    "noteOn":   True
                }
                
                noteOffEvent = {
                    "position": noteData['position'] + noteData['length'],
                    "chan":     currentChannel,
                    "pitch":    noteData['pitch'],
                    "noteOn":   False
                }
                
                allNoteEvents.append(noteOnEvent)
                allNoteEvents.append(noteOffEvent)
            
        currentChannel += 1
    
    
    #Now it's time for the notes
    #first make sure the notes are sorted on position
    noteEventsSorted = sorted(allNoteEvents, key=lambda k: k['position'])
    currentPosition = 0
    for noteEvent in noteEventsSorted:
        position = noteEvent['position']
        #need to get the relative position i.e. delta. This is how much the position
        #has changed since the last note event
        relativePosition = position - currentPosition
        currentPosition = position
        delta = getVLQ(relativePosition)
        
        if len(delta) > 4:
            raise MIDIError("A delta value was too big. The maximum difference in position values is 268,435,455 subdivisions")
        
        offset = 0
        if noteEvent['noteOn']:
            offset = 0x90
        else:
            offset = 0x80
        note = bytearray([offset + noteEvent['chan'], noteEvent['pitch'], 127]) #use a hard coded volume. 127 is max
        delta.extend(note)
        trackEvents.extend(delta)
        
    #Finally send the End event
    TRACK_END = bytearray([0x00, 0xFF, 0x2F, 0x00])
    trackEvents.extend(TRACK_END)

    #now build up the complete track chunk
    trackChunk = TRACK_CHUNK_ID
    
    try:
        #track chunk contains the length of the trackEvents as 4 bytes
        trackChunk.extend(numberToByteArray(len(trackEvents), 4))
    except MIDIError as exep:
        raise MIDIError("MIDI file too large. Maximum size is 4,294,967,295 bytes. (4 GB)")
        
    trackChunk.extend(trackEvents)

    #now combine the header chunk and track chunk to make the midi file
    midiFile = HEADER_CHUNK
    midiFile.extend(trackChunk)
    
    return midiFile
    
#function converts a jingle JSON to a midi file encoded in base64
#raises MIDIError if there is a problem creating the MIDI file
def getMIDIBase64(midiJSON):
    midiFile = getMIDI(midiJSON)
    midiEncoded = base64.b64encode(midiFile)
    return midiEncoded
