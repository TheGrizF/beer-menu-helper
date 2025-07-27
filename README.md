# Beer Menu Helper for High Side

Automated tool to streamline product entry into the Toast pos systems and Untappd for Business.

Goals:
- [x] Untappd for business API integration
  - [x] Beer search functionality
  - [x] Handle multiple search responses
- [x] Generate Toast-compatible CSV output
  - [x] Price calculation
  - [x] POS Name for longer entries
  - [x] Container size selection (Dropdown?)
- [ ] Push beers directly to Untappd Menus
- [ ] GUI version

Toast automation was planned, but not currently available with the current Toast API

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