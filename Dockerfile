FROM python:latest
WORKDIR /app
COPY . .
RUN python3 -m venv .venv
ENV PATH="/venv/bin:$PATH"
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "-m", "server.py"]