## 0.26.3 (2025-03-19)

### Refactor

- :recycle: remove original extension and `.gz` from batch file names (#1147)

## 0.26.2 (2025-03-18)

### Refactor

- 🚚 rename `raw` to `batch` within Python code (#1145)

## 0.26.1 (2025-03-17)

### Refactor

- :recycle: major refactor of path functions to be local-first (#1114)

## 0.26.0 (2025-03-17)

### Feat

- :sparkles: add `check_data_header()` (#1130)

## 0.25.0 (2025-03-17)

### Feat

- :sparkles: add `set_missing_values_to_null()` (#1131)

## 0.24.0 (2025-03-12)

### Feat

- :sparkles: add `read_csv()` to load CSV as DataFrames (#1129)

## 0.23.0 (2025-03-10)

### Feat

- :sparkles: make `build_readme_text()` and `write_file()` public (#1119)

## 0.22.0 (2025-03-06)

### Feat

- :sparkles: add mapping from Frictionless data types to Polars data types (#1106)

## 0.21.1 (2025-03-05)

### Fix

- :bug: only remove qmd files in reference post render to fix md formatting issues (#1107)

## 0.21.0 (2025-03-04)

### Feat

- :sparkles: add `path_readme()` (#1100)

## 0.20.1 (2025-03-04)

### Refactor

- 🚚 rename `create_readme_text()` to `build_readme_text()` (#1099)

## 0.20.0 (2025-02-26)

### Feat

- ✨ extract resource properties from `.json`, `.ndjson`, and `.jsonl` files (#1085)

## 0.19.0 (2025-02-24)

### Feat

- :sparkles: add conversion from resource properties to Pandera schema (#1051)

## 0.18.2 (2025-02-24)

### Refactor

- :recycle: switch `create_package_structure()` to make properties only (#1047)

## 0.18.1 (2025-02-24)

### Refactor

- :recycle: convert `example_package_properties` to function (#1046)

## 0.18.0 (2025-02-21)

### Feat

- ✨ add initial `extract_resource_properties()` (csv, tsv, and parquet files) (#1067)

## 0.17.0 (2025-02-19)

### Feat

- :sparkles: add Pandera checks on the data (#1050)

## 0.16.0 (2025-02-12)

### Feat

- :sparkles: add an `example_package_properties` object (#1044)

## 0.15.0 (2025-02-12)

### Feat

- :sparkles: add `get_nested_attr()` (#1039)

## 0.14.3 (2025-01-28)

### Refactor

- :recycle: use jinja template for README (#1011)

## 0.14.2 (2025-01-28)

### Refactor

- :recycle: commonise Sprout checks (#998)

## 0.14.1 (2025-01-27)

### Refactor

- :recycle: make schema path resolve when working directory different (#1000)

## 0.14.0 (2025-01-27)

### Feat

- :sparkles: add `write_package_properties()` (#984)

## 0.13.3 (2025-01-27)

### Refactor

- :recycle: use checks in `write_resource_properties()` (#990)

## 0.13.2 (2025-01-27)

### Refactor

- :recycle: use new checks in `create_resource_properties()` (#988)

## 0.13.1 (2025-01-27)

### Refactor

- :recycle: use check functions in `edit_package_properties` (#974)

## 0.13.0 (2025-01-24)

### Feat

- ✨ output everything from code cells in Reference docs (#997)

## 0.12.2 (2025-01-24)

### Refactor

- :recycle: `path_package_properties()` -> `path_properties()` (#996)

## 0.12.1 (2025-01-23)

### Refactor

- :recycle: use `CheckErrorMatcher` in Sprout checks (#973)

## 0.12.0 (2025-01-23)

### Feat

- :sparkles: add `CheckErrorMatcher` object (#972)

## 0.11.1 (2025-01-22)

### Refactor

- ♻️  user `Properties` classes in user facing functions (#976)

## 0.11.0 (2025-01-21)

### Feat

- :sparkles: add `check_properties()` (#967)

## 0.10.0 (2025-01-21)

### Feat

- :sparkles: add `check_package_properties()` (#966)

## 0.9.0 (2025-01-21)

### Feat

- :sparkles: add `check_resource_properties()` (#965)

## 0.8.0 (2025-01-21)

### Feat

- :sparkles: collect all Sprout-specific property errors (#964)

## 0.7.0 (2025-01-21)

### Feat

- :sparkles: add functions to check required and blank fields (#963)

## 0.6.0 (2025-01-21)

### Feat

- :sparkles: add simple helper functions (#962)

## 0.5.0 (2025-01-20)

### Feat

- :sparkles: put required fields into constants (#961)

## 0.4.0 (2025-01-20)

### Feat

- :sparkles: Add custom `CheckError` for check functions (#924)

## 0.3.0 (2025-01-20)

### Feat

- :sparkles: add custom renderer to remove floating `:` (#959)

## 0.2.4 (2025-01-10)

### Refactor

- :recycle: can't use the word global on it's own, so renamed to path
- :truck: rename sprout root to sprout global

## 0.2.3 (2025-01-10)

### Refactor

- :truck: rename `SPROUT_ROOT` to `SPROUT_GLOBAL` (#935)

## 0.2.2 (2024-12-18)

### Refactor

- ♻️ rename `verify_` functions to `check_` (#918)

## 0.2.1 (2024-12-18)

### Refactor

- :recycle: move `check_` tests to `checks` folder (#915)

## 0.2.0 (2024-12-16)

### Feat

- :sparkles: check properties against standard (#905)

## 0.1.1 (2024-11-21)

### Fix

- :bug: compact form of nested properties (#887)

## 0.1.0 (2024-11-13)

### Feat

- ✨ add `create_raw_file_name()` (#841)
- ✨  update `Properties` classes with default method and change behaviour of `compact_dict` (#808)
- :sparkles: add `write_resource_properties()` (#784)
- :sparkles: add `edit_package_properties()` (#790)
- ✨ update `verify_resource_properties()` (#773)
- ✨ add that `path_packages()` creates dir if it doesn't exist (#783)
- :sparkles: add `verify_package_properties()` (#744)
- :sparkles: add default values to `ResourceProperties` (#769)
- ✨ add `create_package_structure()` (#754)
- ✨ add `create_readme_text()` (#669)
- ✨ add `path_*()` functions (with their `verify_*()`'ers) (#730)
- :sparkles: add sensible default values for package properties (#743)
- :sparkles: add computed property `asdict` (#745)
- :sparkles: add `read_json()` (#746)
- :sparkles: add `create_default_package_properties()` (#731)
- :sparkles: add `FieldProperties` and `ConstraintsProperties` (#717)
- :sparkles: auto-generate property dataclasses based on spec (#692)
- ✨ add `path_sprout_root()` (#705)
- ✨ add `create_root_path()` (#689)
- ✨ add `get_root_envvar()` (#688)
- :sparkles: add `create_resource_properties()` (#633)
- ✨ add `scrape_json_from_url()` (#628)
- ✨ add `write_file()` (#631)
- :sparkles: add `create_readme_path()` (#630)
- :sparkles: add `create_properties_path()` (#632)
- :sparkles: add `drop_property_fields()` (#629)
- :sparkles: add `verify_resource_properties()` (#613)
- ✨ add `edit_resource_properties_field()` (#621)
- ✨ add `create_resource_structure()` (#610)
- :sparkles: add `extract_properties_from_file()` (#594)
- ✨ add `create_dir()` and `create_dirs()` with tests (#586)
- ✨ add `verify_is_file()` (#597)
- :sparkles: add `create_relative_resource_data_path()` (#596)
- :sparkles: add `verify_format_supported()` (#592)
- ✨ add `get_ids()` function (#582)
- :sparkles: add `create_id_path()` (#591)
- ✨ add `create_resource_raw_path()` (#587)
- :sparkles: add `create_next_id()` (#585)
- ✨ add `verify_is_dir()` (#578)
- add seedcase theme
- add puml name
- format text
- regenerate pumls as svgs instead of pngs
- :sparkles: add seedcase theme to pumls
- :sparkles: add aria labels to icons in navabr
- :sparkles: add sprout logo with alt label to navbar
- **dependabot**: :sparkles: add dependabot for updating Python dependencies
- ✨ single page for metadata creation steps (#415)
- confirmation page
- confirmation page
- making it work with existing links and deleting old stuff
- rename refactor
- small fixes
- view divided in steps
- first draft
- small change
- update with comments by Philip
- update to run psycopg2-binary
- remove linting issues
- update yml file to persist data in postgres
- update dockerfile - remove 22 and 25
- first upload of docker compose file
- authentication and password reset is created (#347)
- :sparkles: add column descriptions
- :lipstick: add mirrored background to use in navbar
- :lipstick: add menu icon and enlargen navbar icons
- :lipstick: add logo to navbar and head
- :lipstick: add logo svg
- add expand_less/expand_more icons when metadata row is selected and unselected (#386)
- with js, add that icon changes to expand_more when row is selected
- add expand_less icon to metadata table rows
- ✨ existing metadata view expanded to show first 5 cols (#359)
- add shown class to rows that should are unhidden to hide them again later
- add button to show five more cols
- load dict tags and utilise it to show only first five cols
- add dictionary filter by key to be used in view
- parse existing_metadata_columns as a dict to view to be able to filter on table_id
- add multiple outline colours and a shadow var
- :sparkles: add last upload to `Tables` and update it when data_rows are not 0
- :sparkles: populate and update last upload at data upload
- :sparkles: add data_rows to tables model to populate and update field at file upload
- add info text to metadata-id-create
- changing the font to Rajdhani
- add data for user test
- :sparkles: update data to an existing table (but still incomplete)
- :construction: synching to switch computers
- :sparkles: new page for uploading data files, finally
- :sparkles: added Django view for uploading data
- :construction: working on adding upload page
- human friendly names to hint the difference between extracted_name and display_name
- :sparkles: add dialog to view and html
- Name change
- Values preserved between view switches
- :sparkles: column metadata is only shown when metadata row is selected
- :sparkles: column metadata is shown underneath each metadata row
- only show first 10 columns to avoid cluttering the view too much
- add column metadata expands on select
- template is moved
- authentication and password reset is created
- Removed print statement
- Support for decimals with comma is added
- added equals sign <=5
- Preview data sample is added
- Exclude column checkbox
- :alembic: change dialog to disabled for button edit and upload
- ruff adjustments
- Disable when running unit tests
- Adding to description that this is test data
- Automatically add test data when DEBUG=TRUE
- :sparkles: add error dialog when user clicks edit or upload without selecting a row
- redirect to data-import when create btn is clicked
- add that clicking row again will deselect the row
- :lipstick: button to switch between table vs grid view for metadata editing
- add paragraph when there is not data to view
- show tooltips for headers
- tabindex on all
- add tabindex with a custom templatetag
- adding style to Kris' work
- handles more invalid csv files
- Validates columns
- Validates columns
- Files are displayed in a table
- Show files as tables
- Simple file download example
- read_csv uses file path and ColumnMetaData created
- add autocomplete="off" for form
- create review list view
- change from ID to Original name
- add existing tables view to view init
- add view-existing-tables to urls
- :sparkles: init view existing table template
- :sparkles: init existing tables view
- use _convert_to_snake_case for column names
- :sparkles: add util function to convert string to snake case
- Disable migrations by not committing migrations into git. Furthermore, the database is not in the persistent storage
- create test scripts for views of column data
- Description as Text input and __str__ added on ColumnDataType
- adding polars_types to ColumnDataType
- created_by is added
- add file size
- keep markdown files to preserve folder structure
- delete method is added
- upload file to persistent storage
- testing preview environment
- persistent storage
- Small adjustments
- read csv file with polars
- add original name as name
- add original name to columnmetadata
- Adjusting docstrings
- central location for ColumnDataTypes
- wait two seconds after click on submit to show progress bar
- show progress bar dialog at click on submit button
- add progress bar dialog
- add cursor pointer to card-button-size buttons
- :sparkles: add tests for data_import view
- add error code to validate_table_name_does_not_exist
- update special characters validator to include field_name in error msg
- include val of table already existing directly in the modelform
- add help button with dialog overlay
- add icon to align with wireframes
- center align dialog header
- show validation errors for name field
- add validator to prevent creating tables with name that already exists
- add validator to prevent special characters in the table name field
- add table id to file-upload url
- update html to utilise modelform fields
- hotfix - created_at defaults to none until we implement users
- update data_import view to use and validate tablemetadataform
- change tablecreation form to modelform
- init/wip
- Matching details with wireframe
- added dropzone and file information box
- Simple file upload is created
- commit before merging from main
- draft
- add command to generate png from specific puml
- add "all" to generate-puml command
- Fixing tests
- PR review adjustments
- Models added for table and column meta data
- Adding of migrations
- add user confirmation of validated row to add in upload
- add "system displays the number of validated rows to the user for agreement"
- add initial version of user flow post
- split up user flow diagram into separate diagrams for user flow post
- :sparkles: initial flow chart of entire user flow
- add flow diagram of preparing schema for upload
- add title to login sequence diagram
- create png of login sequence and remove todo item on that

### Fix

- 🐛  Add UTC timezone to tests using timemachine (#851)
- :bug: sort ids before returning them (#767)
- :pencil2: broken link to guide index file (#764)
- :bug: add missing brackets (#750)
- :bug: remove unnecessary id from `ResourceProperties` (#735)
- :bug: remove space from filename (#687)
- :bug: fix import using old name (#670)
- :bug: fix warnings from deprecated arguments
- :bug: rename own csv folder to avoid clash with built-in csv (#593)
- :fire: remove font colour and name from state diagrams (#583)
- image links and theme (#543)
- use seedcase puml theme
- path to svg
- update c4 image links to svg (#542)
- update c4 image links to svg
- 🐛 debug code depended on old unittest, updated for pytest (#529)
- :bug: fix check for whether tests are running
- :bug: Polars changed the name PolarsDataType to DataType
- use url shortcode instead of urls inside a tags
- remove old png
- remove blank line
- elaborate on alt texts
- remove title from nacbar - not needed when sprout is in the navbar icon
- minor adjustments to step 3 of metadata creation for editing the metadata columns (#419)
- update helper dialog text and remove "machine-readable name"
- minor changes to wording in paragraphs
- "headers" -> "columns" to fit current naming
- :bug: make --surface-container-high white so it's not purple
- format python
- is_draft=False when button is clicked
- step file upload is added
- small adjustments
- small adjustments
- tests and linting is fixed
- Changing existing table
- merge-conflict
- a bit of clean up
- a bit of styling is added
- .venv is added to .dockerignore as it seems to break the docker build
- :building_construction: Update C4 Context diagram to include only Sprout.
- :building_construction: Update UI component diagram to be only about Sprout
- :building_construction: Update C4 container diagram
- :bug: make --surface-container-high white so it's not purple (#416)
- :bug: make --surface-container-high white so it's not purple
- solve merge conflict
- comments added
- expand icon and show more button is fixed
- use columns_set
- merge conflict
- "gender" -> "sex"
- "gender" -> "sex"
- :bug: add missing s to url name (#410)
- :bug: add missing s to url name
- :ambulance: add card.css to base.html
- :ambulance: add quotes around class name
- add background-size: cover to avoid "zoom in" on image
- specify styling to target <img> elements within a <nav> element
- remove border radius from navbar
- remove repeated dialog
- remove end of if-statement
- for readability, add <tr> tag around column metadata tables
- :zap: to avoid having multiple tbodies, move <tbody> out of loop
- don't include border-radius for any elements in metadata_columns_table elements
- remove beercss' default table borders
- :zap: remove unused/unseen style
- modify css for .metadata_columns_table to be applied to correct elements
- :lipstick: update styles to use theme variables
- :lipstick: update and add more colours to fit ui wireframes
- :lipstick: specify that only direct children of table-content should be grey
- fixing tests
- fix conflict
- apply suggestions from code review
- add "rows" to successful upload message
- :fire: remove unused import of datetime
- remove update to modified_at since it's not the metadata being updated here
- remove custom save method so modified_at is `None` before data upload
- change var name tables to table since it only contains one table
- data -> metadata
- only include semibold and bold Rajdhani fonts
- :zap: change normal strings to raw strings for regex patterns
- replace mentions of tables with metadata
- :pencil2: wrong function name used.
- :pencil2: this was changed to just `tables`
- :pencil2: fix model names after renaming for naming scheme
- add missing docstrings to write() and path_raw_storage()
- data-import and url
- :truck: update upload URL in metadata view to direct to data update
- :truck: fix forgotten naming schemes for Models
- :bug: typo, should be uppercase as a constant
- remove incorrect bracket
- fixing tests with small changes
- :truck: forgot to correct the `base.html` path after the change
- :pencil2: Typos in the code introduced during the renaming
- redirect to data-import page after update
- adjustments
- machine readable name is also removed from table overview
- use hidden attribute instead of hide class
- remove duplicate import
- DataType and Excluded flag should also work when switching views
- variable rename fail is fixed
- remove wrongly merged variable
- add column metadata to view
- __init__.py is required in migrations folder otherwise the command makemigrations is not working
- table -> metadata
- :lipstick: thead background colour and remove bottom border
- name was renamed to extracted_name
- add a test
- Resubmitting a file should delete previous file and columns
- update tests to include new column names
- remove error msg from tests since it has been removed from view
- merge conflict
- ruff line too long error
- remove old template view_existing_tables
- update data-import view in test to be minus instead of underscore
- add that no spaces are allowed in error message
- :zap: change referenced urls to kebab-case
- remove unused argument "table_id" from view
- remove import of old view from merge with main
- remove old urls from merge with main
- add missing </a>
- add that selected_metadata_id should be equal to metadata.id to change url
- empty description field and home-made tabindex templatetag is removed
- merge-conflict solved
- remove typo
- remove unused import
- Change empty message to not include "sorry"
- :sparkles: change table to div to enable the whole row being clickable/selectable
- remove style ".expandable"
- remove import of non-existing file-upload view
- remove unused import: ColumnMetadata
- :bug: Running tests told me datetime.UTC doesn't exist. Not sure why, so changed it to timezone.utc
- remove option for NULL in drop-down data-type
- :heavy_minus_sign: Forgot to remove this import
- **typo**: packagee -> package
- ruff format
- save method is overridden and a test is added
- tests are moved to tests_csv_reader
- missing docstring
- removed space
- remove autocomplete
- fix missing ) in url.py
- based on review comments
- merge-conflict
- merge-conflict
- merge-conflict
- migration removed
- ruff adjustments
- The folder staticfiles is automatically created to avoid the warning that the folder is missing
- renamed test file for ColumnDataType
- spelling mistake
- ruff format
- merge-conflict
- naming and docstrings
- naming and docstrings
- ruff format
- Disable suggestions for table name
- change label from "name" to "table name"
- form validation error
- corrected a typo in the tests
- updated form test to use new field
- update href to match name of view-existing-tables
- migrations are added in docker image and collectstatic is executed when the image is created (and not during startup)
- migration
- missed the init file first time
- sort out lint
- remove data type from PR
- add ruff exemptions to the last bits
- :construction: update to docstrings and format of imports
- add Ruff exemptions for a couple of D102 to see if that makes a difference for linting
- status code changed
- after rename
- after rename
- ruff, unused import
- extra / is removed in path
- create dir if missing
- removed bad code
- staticfiles needs to be present
- ruff import order
- why is preview deployment not triggered
- reverting deploy-pr-preview.yml
- Fixing if BytesIO instead of TextIO
- using selectors instead
- Docstring adjustments
- ruff adjustments
- ruff adjustments
- update initial migration to include original_name in columnmetadata
- centre align icon on it's own line
- :pencil2: apply suggestions from code review [skip ci]
- multiline comment
- Handle static assets when DEBUG=False
- resolve merge conflict
- :pencil2: apply suggestions from code review
- add bottom margin for name field when validation fails
- remove validationerror from return typehint
- remove validtionerror from return typehint
- ruff adjustments
- Remove python_type and pandas_type
- The columns are updated after a migration
- :bug: A function was forgotten to be renamed after it was changed.
- trying CSRF_TRUSTED_ORIGINS
- missing file
- trying to fix csrf adding comment
- trying to fix csrf adding comment
- trying to fix csrf
- if errors in form, show dialog
- add button to cancel class
- remove data-ui from create button to avoid closing dialog when validation fails
- remove description text field - we use the form field now
- remove default=None from created_by
- port 10000 -> 8000
- :pencil2: apply suggestions from code review
- :pencil2: apply suggestions from code review
- docstrings and type hints
- adjustments reviewed
- ruff formatting added
- rename to seedcase-sprout-preview which is more clear
- only seedcase-sprout
- hardcode seedcase-sprout-pr test
- Using FLY_APP variable
- update-migrations creates and applies migrations
- add migrations before loading sample
- small typo fix.
- move whitenoise up under securitymiddleware
- :coffin: Seems like this code wasn't used, so removed it
- Adjustments from review comments
- apply suggestions from code review
- -no-interaction --no-root
- Another fix to the test workflow
- semi colon -> comma
- change comment style from # to //
- :pencil2: Indentation was wrong...
- missing a just command
- Adding tests
- Reverting changes related to enforcing foreign key constraint in SQLite. This seems to be handled by Django
- Fixed poetry version
- Deploy to fly.io is fixed
- apply suggestions from code review
- rerun pumls to change "schema(s)" to "table(s)"
- replace "schema(s)" with "table(s)" in all files related to user flow
- apply suggestions from code review
- remove mention of "V2"
- :fire: delete outdated schema creation flow diagram
- :fire: remove "tricky part" png
- remove numbering from output file name
- Minor fixes to user flow diagrams based on review from @lwjohnst86
- add line from "continue" back validation check
- Minor text mods
- :fire: remove files that are created when rendering
- remove ordering from yaml
- add blank line before list so it renders correctly
- remove "design" from path to login sequence png
- apply suggestions from code review

### Refactor

- 🔥 remove everything Django-related (#848)
- :recycle: rename "sprout" folder to "seedcase_sprout" (#844)
- :recycle: create resource dir when making package (#788)
- 🔥 remove some functions in `create_properties_template()` (#685)
- ♻️  rename to `edit_property_field()` to be more inclusive (#658)
- :recycle: divide tests into app and core folders (#545)
- move some string helper functions to core (#541)
- :sparkles: add frictionless-style sample data and metadata (#530)
- ♻️  reorganize Sprout into core and app components (#522)
- ♻️ change label to "data type" (#519)
- :art: switch to using HTML dd for each item, rather than a break between
- renames based on PR review
- :construction: Incompletely update/expand on the C4 component for API
- :lipstick: move `background-image` into css to remove use of inline style
- :art: optimise the use of the innate theme variables
- :art: initiate the move of card styling to separate css file
- code is simplified
- :lipstick: move table css styling into own file and initiate ui
- :recycle: use URL Django shortcode
- :fire: remove placeholder home
- change redirects fit that projects_id_metadata_view is home
- make projects_id_metadata_view the home page
- :truck: include `includes` in path of these templates
- :pencil2: follow naming scheme for classes
- :pencil2: `projects id` not `project id`
- :recycle: convert URLs to use `reverse()` with full Django URL name (not path)
- :recycle: rename Tables class to match naming scheme
- :recycle: rename Files model to match naming scheme
- :recycle: this should be capitalized as it is a constant
- :recycle: rename to Columns (and columns) to match naming scheme of class
- :recycle: rename model class for DataTypes to match naming scheme
- move to user-tests folder
- :pencil2: use correct url for create metadata, plus use reverse for url
- :pencil2: projects-id instead of project-id (plural)
- :recycle: update URLs and links to reflect name change, but leads to test issues
- :truck: Fix paths to includes files, plus auto-reformat HTML
- :truck: Match scheme for data/id/metadata/create
- :truck: Match scheme for data/id/metadata/create
- :truck: Match scheme for data/id/metadata/edit/table
- :truck: Match naming scheme for data/id/metadata/create
- :truck: Match naming scheme for data/id/metadata/edit/table
- :truck: Rename functions to match scheme for metadata edit grid
- :truck: Fix names of URL in Python code
- :truck: Change function names after renaming
- :truck: Use `project-id-view` html file path
- :truck: fix path to base.html, plus reformat
- :truck: Use index.html instead in the Django view
- :recycle: revise to match naming scheme
- :lipstick: rename HTML template file to match naming scheme
- :recycle: URL should match naming scheme for URLs (minus project/id)
- :zap: merge expand feature into `project id metadata`
- separate create new metadata dialog
- simplified js and removed tests not valid with a js solution
- change buttons to anchors to slightly simplify code
- move table selectable styles to static
- handle redirect in template instead of view using js
- remove unused form name
- restructure if statement to avoid writing error msg twice
- :recycle: update links after consolidation
- :recycle: remove duplicated Django views and consolidated into `column_review.py`
- :recycle: remove duplicated/scatter code and consolidate into single `column-review` page
- convert to new naming scheme
- :recycle: True/False seems more appropriate than Yes/No.
- :truck: Renamed function to describe what it does better, given changes to other functions
- :recycle: Move file storage code into its own function for more generic use later
- :truck: Rename files to match the `metadata/create` format
- :recycle: Revise to indicate the upload is for creating metadata, not the final upload
- moved to csv folder
- :adhesive_bandage: rename to specify which models are included in this file
- split up tests for views into separate files
- migration and FileMetaData renamed to FileMetadata
- method name change
- move const dialog to showDialog()
- :lipstick: update error msg of no special characters validator
- :art: specify imports from django.forms
- add typehints and docstring to clean_name
- add type hints for returns
- move validation of special character to validator
- use redirect instead of httpresponseredirect
- move val table already exists to form instead of model
- explicitly state that create is a submit button
- rename val of no special characters
- :sparkles: update to match partial user flow diagrams
