import logging

#defines the functions for updating a jingle.
#each function takes a jingle and an action
#it returns the updated jingle, and an updated action
#   updated actions contain the checksums

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
            logging.warning('A too small tempo was given: ' = str(action_tempo))
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


def generate_checksum(jingle):
    return None