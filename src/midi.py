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
def getMIDI(testJSON):
    #The following bytes make up the head of a MIDI file
    HEAD_CHUNK_ID   = bytearray([0x4D, 0x54, 0x68, 0x64])   #MIDI Magic Number "MThd"
    HEAD_CHUNK_SIZE = bytearray([0x00, 0x00, 0x00, 0x06])   #Head chunk is always 6 bytes in length
    MIDI_FORMAT     = bytearray([0x00, 0x00])               #We are using format 0
    MIDI_TRACKS     = bytearray([0x00, 0x01])               #Format 0 only uses 1 track
    TIME_DIV        = bytearray([0x00, 0x60])               #Use a constant of 96 divisions per quarter note

    #Build up the complete header chunk
    HEADER_CHUNK = HEAD_CHUNK_ID
    HEADER_CHUNK.extend(HEAD_CHUNK_SIZE)
    HEADER_CHUNK.extend(MIDI_FORMAT)
    HEADER_CHUNK.extend(MIDI_TRACKS)
    HEADER_CHUNK.extend(TIME_DIV)

    #The second chunk is the track itself
    TRACK_CHUNK_ID  = bytearray([0x4D, 0x54, 0x72, 0x6B])   #A track starts with the Magic Number "MTrk"
    #next comes the track size which we will work out as we go along
    trackSize = 0;
    #The first event sets the time signature (8 bytes). We use a standard 4 4
    TIME_SIG        = bytearray([0x00, 0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08])
    trackSize += len(TIME_SIG)
    trackEvents = TIME_SIG #build up the track events

    midi = json.loads(testJSON) #for now use a hard coded example but this will be changed to get from storage

    tempo = numberToByteArray(midi['tempo'], 3)
    tempoEvent = bytearray([0x00, 0xFF, 0x51, 0x03])
    tempoEvent.extend(tempo)
    trackSize += len(tempoEvent)
    trackEvents.extend(tempoEvent)

    #Now set the instruments
    for instrumentData in midi['instruments']:
        currentInstrument = bytearray([0, 192+instrumentData['channel'], instrumentData['instrumentID']])
        trackSize += len(currentInstrument)
        trackEvents.extend(currentInstrument)
        
    #Now it's time for the notes
    for notes in midi['notes']:
        delta = getVLQ(notes['delta'])
        offset = 0
        if notes['noteDown']:
            offset = 0x90
        else:
            offset = 0x80
        noteEvent = bytearray([offset + notes['channel'], notes['noteID'], notes['volume']])
        delta.extend(noteEvent)
        trackSize += len(delta)
        trackEvents.extend(delta)
        
    #Finally send the End event
    TRACK_END = bytearray([0x00, 0xFF, 0x2F, 0x00])
    trackSize += len(TRACK_END)
    trackEvents.extend(TRACK_END)

    #now build up the complete track chunk
    trackChunk = TRACK_CHUNK_ID
    trackChunk.extend(numberToByteArray(trackSize, 4))
    trackChunk.extend(trackEvents)

    #now combine the header chunk and track chunk to make the midi file
    midiFile = HEADER_CHUNK
    midiFile.extend(trackChunk)
    
    return midiFile