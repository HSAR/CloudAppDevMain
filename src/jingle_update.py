#defines the functions for updating a jingle.
#each function takes a jingle and an action
#it returns the updated jingle, and an updated action
#   updated actions contain the checksums

def remove_note(jingle, action):
    
    action_track = action['track']
    action_noteid = action['noteId']
    
    track = jingle['tracks'][action_track]
    if len(track) != 0:
        noteRemoved = False
        for note in track['notes']:
            if note['id'] == action_noteid:
                track['notes'].remove(note)
                noteRemoved = True
                break
        if noteRemoved:
            jingle['tracks'][action_track] = track
            
    action["checksum"] = generate_checksum(jingle)
    
    return [jingle, action]

















def generate_checksum(jingle):
    return None