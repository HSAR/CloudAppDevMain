import logging
import json
import zlib
import operator

#defines the functions for updating a jingle.
#each function takes a jingle and an action
#it returns the updated jingle, and an updated action
#   updated actions contain the checksums

def add_note(jingle, action):
    
    action_note_id     = action['note']['id']
    action_note_pos    = action['note']['pos']
    action_note_track  = action['note']['track']
    action_note_pitch   = action['note']['pitch']
    action_note_length = action['note']['length']
    
    if type(action_note_id) is unicode:
        if type(action_note_pos) is int:
            if type(action_note_track) is int:
                if type(action_note_pitch) is int:
                    if type(action_note_length) is int:
                        
                        if action_note_pos >= 0:
                            if action_note_track >=0 and action_note_track <= 14:
                                if action_note_pitch >=0 and action_note_pitch <= 127:
                                    if action_note_length > 0:
                                    
                                        track = jingle['tracks'][action_note_track]
                                        if len(track) > 0:
                                            notes = track['notes']
                                            note_start = action_note_pos
                                            note_end = action_note_pos + action_note_length
                                            note_pitch = action_note_pitch
                                            
                                            note_unique = True
                                            
                                            for note in notes:
                                                if note['id'] == action_note_id:
                                                    note_unique = False
                                                    break
                                                
                                            if note_unique:
                                                
                                                new_note = {}
                                                new_note['id']     = action_note_id
                                                new_note['pos']    = action_note_pos
                                                new_note['length'] = action_note_length
                                                new_note['pitch']   = action_note_pitch
                                        
                                                for note in notes:
                                                    current_start = note['pos']
                                                    current_end = current_start + note['length']
                                                    current_pitch = note['pitch']
                                                    
                                                    if not (current_end <= note_start or current_start >= note_end or current_pitch != note_pitch):
                                                        notes.remove(note)
                                                    
                                                notes.append(new_note)
                                                track['notes'] = notes
                                                jingle['tracks'][action_note_track] = track
                                        
                                    else:
                                        logging.warning('A non positive length was provided: ' + str(action_note_length))
                                else:
                                    logging.warning('A note number was not in the valid range: ' + str(action_note_pitch))
                            else:
                                logging.warning('A track number was not in the valid range: ' + str(action_track))
                        else:
                            logging.warning('A negative position was provided: ' + str(action_note_pos))
                            
                    else:
                        logging.warning('A non int length was given: ' + str(action_note_length))
                else:
                    logging.warning('A non int note was given: ' + str(action_note_pitch))
            else:
                logging.warning('A non int track number was given: ' + str(action_note_track))
        else:
            logging.warning('A non int position was given: ' + str(action_note_pos))
    else:
        logging.warning('A non string (' + str(type(action_note_id)) + ') note id was given: ' + str(action_note_id))
    
    
    action['checksum'] = generate_checksum(jingle)
    
    return [jingle, action]


def remove_note(jingle, action):
    
    action_track = action['track']
    action_noteid = action['noteId']
    
    if type(action_track) is int:
        if action_track >= 0 and action_track <= 14:
            
            track = jingle['tracks'][action_track]
            if len(track) != 0:
                for note in track['notes']:
                    if note['id'] == action_noteid:
                        track['notes'].remove(note)
                        break
                jingle['tracks'][action_track] = track
    
        else:
            logging.warning('A track number was not in the valid range: ' + str(action_track))
    else:
        logging.warning('A non int track number was given: ' + str(action_track))
    
    action['checksum'] = generate_checksum(jingle)
    
    return [jingle, action]


def change_tempo(jingle, action):
    
    action_tempo = action['tempo']
    
    if type(action_tempo) is int:
        if action_tempo >= 4:
            jingle['head']['tempo'] = action_tempo
        else:
            logging.warning('A too small tempo was given: ' + str(action_tempo))
    else:
        logging.warning('A non int tempo was given: ' + str(action_tempo))
    
    action['checksum'] = generate_checksum(jingle)
    
    return [jingle, action]


def change_sub_divisions(jingle, action):
    
    action_sub = action['subDivisions']
    
    if type(action_sub) is int:
        if action_sub < 1 or action_sub > 65535:
            logging.warning('A sub division was not in the valid range: ' + str(action_sub))
        else:
            jingle['head']['subDivisions'] = action_sub
    else:
        logging.warning('A non int sub division was given: ' + str(action_sub))
    
    action['checksum'] = generate_checksum(jingle)
    
    return [jingle, action]


def add_instrument(jingle, action):
    
    action_track = action['instrument']['track']
    action_inst  = action['instrument']['inst']
    
    if type(action_track) is int:
        if type(action_inst) is int:
            if action_track >= 0 and action_track <= 14:
                if action_inst >= 0 and action_inst <= 127:
                    
                    track = jingle['tracks'][action_track]
                    if len(track) == 0:
                        track['instrument'] = action_inst
                        track['notes'] = []
                    else:
                        track['instrument'] = action_inst
                        
                    jingle['tracks'][action_track] = track
                        
                else:
                    logging.warning('An instrument was not in the valid range: ' + str(action_inst))
            else:
                logging.warning('A track number was not in the valid range: ' + str(action_track))
        else:
            logging.warning('A non int instrument was given: ' + str(action_inst))
    else:
        logging.warning('A non int track number was given: ' + str(action_track))
    
    action['checksum'] = generate_checksum(jingle)
    
    return [jingle, action]


def remove_instrument(jingle, action):
    
    action_track = action['instrumentTrack']
    
    if type(action_track) is int:
        if action_track >= 0 and action_track <= 14:
            jingle['tracks'][action_track] = {}
        else:
            logging.warning('A track number was not in the valid range: ' + str(action_track))
    else:
        logging.warning('A non int track number was given: ' + str(action_track))
    
    action['checksum'] = generate_checksum(jingle)
    
    return [jingle, action]
    
def edit_instrument(jingle, action):
    
    action_track = action['instrumentTrack']
    action_inst  = action['instrumentNumber']
    
    if type(action_track) is int:
        if type(action_inst) is int:
            if action_track >= 0 and action_track <= 14:
                if action_inst >= 0 and action_inst <= 127:
                    
                    track = jingle['tracks'][action_track]
                    if len(track) != 0:
                        track['instrument'] = action_inst
                    jingle['tracks'][action_track] = track
                        
                else:
                    logging.warning('An instrument was not in the valid range: ' + str(action_inst))
            else:
                logging.warning('A track number was not in the valid range: ' + str(action_track))
        else:
            logging.warning('A non int instrument was given: ' + str(action_inst))
    else:
        logging.warning('A non int track number was given: ' + str(action_track))
    
    action['checksum'] = generate_checksum(jingle)
    
    return [jingle, action]


# Calculates a checksum of an object, used for verifying integrity.
def generate_checksum(obj):
    obj['tracks'].sort(key=operator.itemgetter('instrument'))
    for t in obj['tracks']:
        t['notes'].sort(key=operator.itemgetter('id'))
    return zlib.adler32(
            json.dumps(obj, ensure_ascii=False, indent=None,
                separators=(',', ':'), sort_keys=True),
            1) & 0xffffffff # coerce to unsigned integer, as recommended by the
                            # documentation, because this part of the standard
                            # library made some poor life choices
