-- Insert Kontakt 7 on a MIDI-ready track
function insertKontaktMidiReady()
  reaper.Undo_BeginBlock()

  -- Create new track
  reaper.InsertTrackAtIndex(reaper.CountTracks(0), true)
  local track = reaper.GetTrack(0, reaper.CountTracks(0)-1)
  reaper.GetSetMediaTrackInfo_String(track, 'P_NAME', 'Kontakt 7', true)

  -- Insert Kontakt 7 VSTi
  reaper.TrackFX_AddByName(track, "VSTi: Kontakt 7", false, 1)

  -- Set track to 64 channels (optional)
  reaper.SetMediaTrackInfo_Value(track, "I_NCHAN", 64)

  -- Arm for recording
  reaper.SetMediaTrackInfo_Value(track, "I_RECARM", 1)

  -- Set input to MIDI: All inputs, all channels
  reaper.SetMediaTrackInfo_Value(track, "I_RECINPUT", 4096) -- MIDI input
  reaper.SetMediaTrackInfo_Value(track, "I_RECMODE", 1)     -- Record input (MIDI)

  -- Enable monitoring
  reaper.SetMediaTrackInfo_Value(track, "I_AUTOMODE", 1)    -- Monitor on

  reaper.Undo_EndBlock("Insert Kontakt 7 (MIDI-ready)", -1)
end

insertKontaktMidiReady()
