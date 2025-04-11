# ShooterCounter - Overwatch Hero Database

A desktop application built with CustomTkinter that displays information about Overwatch heroes using the [overfast-api](https://overfast-api.tekrop.fr/).

[ShooterCounter Preview - Watch Video](https://imgur.com/gallery/overwatch-api-python-interface-cEcutC3)

## Features

- Browse all Overwatch heroes with a clean, modern UI
- Filter heroes by role (Tank, Damage, Support)
- View detailed information for each hero:
  - Portrait and role
  - Location and biographical information
  - Age and birthday
  - Character background
  - Health, armor, and shield statistics with visual bars
  - Complete list of abilities with descriptions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Viniciusmq25/Overwatch-API-CustomTkinter.git
cd Overwatch-API-CustomTkinter
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python interface.py
```

- Click on a hero card to browse the hero roster
- Use the filter buttons to sort heroes by role
- Click "Click for more info" on any hero card to view detailed information

## Requirements

- Python 3.7+
- CustomTkinter 5.2.2
- Pillow 11.1.0
- Requests 2.32.3

See `requirements.txt` for a complete list of dependencies.

## Project Structure

- `interface.py` - Main application file with the UI implementation
- `shootcounter.ico` - Application icon file

## Error Handling

The application includes error handling for:
- Failed API connections
- Missing hero data or images
- Invalid responses from the overfast-api

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Author

Vinicius Quintian

## Acknowledgements

- [overfast-api](https://overfast-api.tekrop.fr/) - For providing Overwatch hero data
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - For the modern UI components
- Blizzard Entertainment - Creator of Overwatch
