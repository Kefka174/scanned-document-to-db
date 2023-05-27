# Image Recogniton:
- [x] Load and display image
  - [ ] Select file in explorer
- [x] Rotate image
- [x] Zoom in on image
  - [ ] Focus zoom on cursor
- [x] Pan view
  - [ ] Limit pan to image borders
- [x] Scan Mode
  - [x] Drag-select portion of image to scan
  - [x] Convert text in selection box to strings
  - [ ] Highlight converted strings in image
  - [ ] Maintain highlights through panning, zooming, rotating

# Database:
- [ ] Set up database (external)
- [x] GUI panel to manage schema
  - [ ] Dynamically generate table widgets
    - [ ] Order based on foreign keys
  - [x] Dynamically generate feild widgets
  - [ ] Dock panel to top or bottom of main window
- [x] Clear table, not clear all tables
- [ ] Create schema
  - [ ] Make table
  - [ ] Add fields
  - [ ] Designate required fields
  - [ ] Designate foreign keys
  - [ ] Designate autoID
  - [ ] Save schema
- [ ] Load preset schema
- [ ] Click image highlights to fill in fields
  - [ ] Can manually edit field imput data
  - [ ] Drop-down for existing field value
- [ ] Add entry to database
  - [ ] Required fields filled
  - [ ] Foreign keys point properly
  - [ ] Sanitize
  - [ ] Not a duplicate entry


<br></br>
## Example schema: Yacht Club Races
### Race
- ID
- ***Year***
- ***Series***
- ***Class***

### Race Result
- ID
- ***RaceID***
- ***Placement***
- Trophy (optional)

### Sailor Participation
- **ResultID**
- **Name**
- Boat