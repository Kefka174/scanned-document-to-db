# Image Recogniton / GUI:
- [x] Load and display image
  - [ ] Select file in explorer
- [x] Rotate image
  - [ ] Rotate relative to center view
- [x] Zoom in on image
  - [x] Focus zoom on cursor
- [x] Pan view
  - [ ] Limit pan to image borders
- [x] Scan Mode
  - [x] Drag-select portion of image to scan
  - [x] Convert text in selection box to strings
  - [x] Highlight converted strings in image
  - [ ] Maintain highlights through:
    - [x] panning
    - [ ] zooming
    - [ ] rotating
- [ ] Rotate and Scan Buttons recenter on window-size change
- [ ] "Ctrl+ / Ctrl-" Resize button and field text

# Database:
- [x] Set up database (external)
- [x] Set up database connector
- [ ] GUI panel to connect to database
  - [ ] Dynamically generate connection config fields
- [ ] Display database errors in GUI
- [x] GUI panel to manage schema
  - [ ] Dynamically generate table widgets
    - [ ] Order based on foreign keys
    - [ ] Close out unwanted tables
  - [x] Dynamically generate field widgets
    - [ ] Autosize and left-align fields
  - [ ] Dock panel to top or bottom of main window
- [x] Clear table, not clear all tables
- [x] Click image highlights to fill in fields
  - [x] Can manually edit field imput data
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

### Sailors
- ID
- ***First Name***
- ***Last Name***

### Sailor Participation
- **ResultID**
- **SailorID**
- Boat (optional)