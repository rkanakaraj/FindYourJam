# FindYourJam
Music Recommendation system using Conjoint analysis, an advanced analytic technique. which gives importance to features.  

## INSTRUCTIONS

### Step 1

Update data/config.json as follows:
*   update client_id, client_secret by using https://developer.spotify.com/dashboard/applications
*   update your liked songs in "songs" attribute, and also rate each songs on a scale to 10.
*   update keys required for processing (optional. If updated, then max, min values of the keys also has to be updated)

### Step 2

Use run function under runner.Runner module to realise your music taste.

### Step 3

Use run_tests function under runner.Runner module to find worth of playlists.
args: previously computed partworths, list of playlists (playlist - list of track names)

Check ***#usage*** in runner.Runner module for further instructions.
