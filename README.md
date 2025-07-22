# Beer Menu Helper for High Side

Automated tool to streamline product entry into the Toast pos systems and Untappd for Business.

Goals:
- [ ] Untappd for business API integration
  - [ ] Beer search functionality
  - [ ] Handle multiple search responses
- [ ] Generate Toast-compatible CSV output
  - [ ] Price calculation
  - [ ] POS Name for longer entries
  - [ ] Container size selection (Dropdown?)
- [ ] Push beers directly to Untappd Menus
- [ ] GUI version

# Usage

1. Create a `.env` file containing:

```
EMAIL={your email}
UTFB_READ_ONLY_TOKEN={your read only token}
UTFB_READ_WRITE_TOKEN={your read and write token}
```
Note: Email must be linked to an Untappd for Business account.  You can find your tokens at: `https://business.untappd.com/account`

2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run the Script
```
python beer_togo.py
````