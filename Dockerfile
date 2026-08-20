FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Flag lives at filesystem root, same as the original 3v@l challenge
RUN mv flag.txt /flag.txt

EXPOSE 5000

CMD ["python", "app.py"]
