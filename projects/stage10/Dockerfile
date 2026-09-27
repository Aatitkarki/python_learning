FROM python:3.12-slim
WORKDIR /app
COPY requirements/api.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home learner
COPY projects /app/projects
COPY datasets /app/datasets
RUN mkdir /app/work && chown learner:learner /app/work
USER learner
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "projects.api:app", "--host", "0.0.0.0", "--port", "8000"]
