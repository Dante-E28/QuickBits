FROM python:3.12
WORKDIR /src
COPY . .
RUN pip install alembic
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "src.main:app --reload"]