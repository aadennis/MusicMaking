-- Insert Kontakt 7 on a new track with no extra routing
function insertKontaktSolo()
  reaper.Undo_BeginBlock()

  -- Create new track
  reaper.InsertTrackAtIndex(reaper.CountTracks(0), true)
  local track = reaper.GetTrack(0, reaper.CountTracks(0)-1)
  reaper.GetSetMediaTrackInfo_String(track, 'P_NAME', 'Kontakt 7', true)

  -- Insert Kontakt 7 VSTi
  reaper.TrackFX_AddByName(track, "VSTi: Kontakt 7", false, 1)

  -- Optional: set track to 64 channels for internal routing flexibility
  reaper.SetMediaTrackInfo_Value(track, "I_NCHAN", 64)

  reaper.Undo_EndBlock("Insert Kontakt 7 (solo track)", -1)
end

insertKontaktSolo()
