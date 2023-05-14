# Image Recogniton:
- [ ] Load and display image
    - [ ] Rotate image
    - [ ] Crop image
- [ ] Scan Mode
  - [ ] Drag select portion of image to scan
- [ ] Select Mode
  - [ ] Convert text in selection box to strings
  - [ ] Highlight converted strings in image
  - [ ] Double click contour to break down further

# Database:
- [ ] Set up database (external)
- [ ] GUI panel to manage schema
  - [ ] Dynamically generate table widgets
    - [ ] Order based on foreign keys
  - [ ] Dynamically generate feild widgets
- [ ] Clear table, not clear all tables
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