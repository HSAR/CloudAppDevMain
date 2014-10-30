import json;

#function to convert a decimal number to an array of bytes
#takes a number to convert and the number of bytes in the returned array
def numberToByteArray(number, bytes):
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

#function converts a json into a midi. It will probably take some other arguments later to query for the json
def getMIDI(midiJSON):
    midi = json.loads(midiJSON) #for now we pass in the JSON string to the function
    
    #The following bytes make up the head of a MIDI file
    HEAD_CHUNK_ID   = bytearray([0x4D, 0x54, 0x68, 0x64])   #MIDI Magic Number "MThd"
    HEAD_CHUNK_SIZE = bytearray([0x00, 0x00, 0x00, 0x06])   #Head chunk is always 6 bytes in length
    MIDI_FORMAT     = bytearray([0x00, 0x00])               #We are using format 0
    MIDI_TRACKS     = bytearray([0x00, 0x01])               #Format 0 only uses 1 track
    #time division is stored as 2 bytes and is located under 'subDivisions' in the JSON
    TIME_DIV        = numberToByteArray(midi['subDivisions'], 2)

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

    #convert tempo from beats per minute to microseconds per quarter note
    tempoBPM = midi['tempo']
    tempoMPQN = 60000000 / tempoBPM

    tempo = numberToByteArray(tempoMPQN, 3)
    tempoEvent = bytearray([0x00, 0xFF, 0x51, 0x03])
    tempoEvent.extend(tempo)
    trackEvents.extend(tempoEvent)

    #Now set the instruments
    for instrumentData in midi['instruments']:
        currentInstrument = bytearray([0, 192+instrumentData['chan'], instrumentData['inst']])
        trackEvents.extend(currentInstrument)
        
    #Now it's time for the notes
    #first make sure the notes are sorted on position
    notes = sorted(midi['notes'], key=lambda k: k['pos'])
    currentPosition = 0
    for noteEvent in notes:
        position = noteEvent['pos']
        #need to get the relative position i.e. delta. This is how much the position
        #has changed since the lase note event
        relativePosition = position - currentPosition
        currentPosition = position
        delta = getVLQ(relativePosition)
        offset = 0
        if noteEvent['noteOn']:
            offset = 0x90
        else:
            offset = 0x80
        note = bytearray([offset + noteEvent['chan'], noteEvent['note'], noteEvent['vol']])
        delta.extend(note)
        trackEvents.extend(delta)
        
    #Finally send the End event
    TRACK_END = bytearray([0x00, 0xFF, 0x2F, 0x00])
    trackEvents.extend(TRACK_END)

    #now build up the complete track chunk
    trackChunk = TRACK_CHUNK_ID
    #track chunk contains the length of the trackEvents as 4 bytes
    trackChunk.extend(numberToByteArray(len(trackEvents), 4))
    trackChunk.extend(trackEvents)

    #now combine the header chunk and track chunk to make the midi file
    midiFile = HEADER_CHUNK
    midiFile.extend(trackChunk)
    
    return midiFile