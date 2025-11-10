.PHONY: setup day2 day3 test app

setup:
\tpython -m venv .venv && . .venv/Scripts/activate || . .venv/bin/activate; pip install -r requirements.txt

day2:
\tpython src/pipeline_day2.py

day3:
\tpython src/pipeline_day3.py

test:
\tpytest -q

app:
\tstreamlit run app/streamlit_app.py
