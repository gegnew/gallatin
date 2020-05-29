# Is the Gallatin Dry Enough to Climb?

Data warehousing project to determine if the weather is good for climbing in
the Gallatin Canyon (or anywhere else!).

Uses the Synoptic weather API and the Mountain Project API (along with some
scraping) to collect data. Warehouses to Redshift.

## Getting Started

Clone this repo


### Installing

Create a virtual environment. You can use [this script for setting up direnv](https://github.com/gegnew/auto-direnv) or do:
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

End with an example of getting some data out of the system or using it for a little demo

### Usage

Set your Redshift configs in `dwh.config`. Run `etl.py`. If things don't work,
open `MP.ipynb` for a more-or-less logical flow of what's supposed to happen.

## Authors

* **Gerrit Egnew** - *Initial work* - [Github](https://github.com/gegnew)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
