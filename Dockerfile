FROM python:3.10
COPY . .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]