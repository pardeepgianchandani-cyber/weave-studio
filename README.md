# Fabric Weave Studio

An interactive educational web application for Textile Engineering students to create and study woven fabric structures.

## Features

- Plain 1/1 and basket 2/2 weave drafts
- Configurable right- and left-hand twill structures
- 5-, 7-, 8-, 9- and 11-end satin structures with valid satin step selection
- Custom binary interlacement editor
- Warp and weft colour selection
- EPI, PPI and yarn-count construction inputs
- Interlacement diagram and conceptual woven appearance
- Repeat and float analysis
- Export technical summary (CSV), weave matrix (CSV), and diagram (PNG)

## Interlacement convention

The application uses a binary matrix:

- `1` = warp yarn is above the weft yarn at that intersection.
- `0` = weft yarn is above the warp yarn at that intersection.
- Matrix columns represent warp ends.
- Matrix rows represent weft picks.

## Run locally

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/YOUR-USERNAME/fabric-weave-studio.git
cd fabric-weave-studio
python -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will open in your browser, normally at `http://localhost:8501`.

## Deploy on GitHub and Streamlit Community Cloud

1. Create a GitHub repository named `fabric-weave-studio`.
2. Upload `app.py`, `requirements.txt`, and `README.md` to the repository root.
3. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) using GitHub.
4. Select **Create app** and choose your repository, branch (usually `main`), and main file path (`app.py`).
5. Deploy. Streamlit will install the packages listed in `requirements.txt`.
6. Share the generated public app URL with students and exhibition visitors.

## Suggested exhibition demonstration

1. Select Plain 1/1 and explain warp-over and weft-over intersections.
2. Change to 2/2 twill and compare the diagonal effect.
3. Select satin and discuss longer floats and surface characteristics.
4. Change EPI and PPI to demonstrate construction settings.
5. Export a weave diagram and technical sheet.

## Engineering limitations

This is a teaching and visualization tool. The rendered fabric is a conceptual representation, not a calibrated optical simulation. EPI and PPI are construction inputs and do not automatically alter the geometric repeat. The current version does not calculate yarn crimp, cover factor, GSM, tensile strength, drape, shrinkage, loom settings, or production feasibility. Those require additional assumptions, yarn/fibre data, and validated models.

## Project information

**Project:** Fabric Weave Studio  
**Domain:** Textile Engineering — Weaving Technology  
**Platform:** Python, Streamlit, NumPy, Pandas, Matplotlib  
**Purpose:** Student learning and project exhibition
