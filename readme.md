# This is an experimental dashboard based on what was discussed in last Wednesday's meeting

## Usage

This dashboard is built using Shiny and Python. To run it, ensure you have the necessary packages installed and then execute the following command in your terminal:

```bash
shinylive export app docs
```

Then, you will see a command that looks like 

```bash
python3 -m http.server --directory docs --bind localhost 8008
```

Depending on your os, you may need to use `python` instead of `python3`.

Open your web browser and navigate to `http://localhost:8008` to view the dashboard.

It should look something like this.

![Screenshot of the dashboard](docs/dashboard_screenshot.png)