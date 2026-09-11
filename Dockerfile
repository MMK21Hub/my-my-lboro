FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY .python-version .
COPY uv.lock .
RUN uv sync --locked
COPY *.py .
COPY entrypoint.sh .

EXPOSE 9000
ENV PATH="/app/.venv/bin:$PATH"
RUN ln -s /app/entrypoint.sh /app/.venv/bin/my_my_lboro
ENTRYPOINT ["my_my_lboro"]
