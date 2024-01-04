if not exist "./data/packages_info.txt" (
  echo Installing requirements...
  pip install -r requirements.txt
  echo Requirements installed successfully > "./data/packages_info.txt"
)

python ./src/main.py
pause