FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app/
COPY webUI/static /app/webUI/static
COPY webUI/template /app/webUI/template
COPY KineticHub/db_api.py /app/KineticHub/db_api.py
COPY RAPBuilderAPI/utils.py /app/RAPBuilderAPI/utils.py
COPY app.py /app/
COPY config.py /app/
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5000
CMD ["python", "app.py", "--host=0.0.0.0"]
