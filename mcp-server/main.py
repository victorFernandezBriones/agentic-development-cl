import logging
import os
import sys

from dotenv import load_dotenv

from server import mcp
import tools.chilean_data  # noqa: F401  (import con efecto: registra las tools)

load_dotenv()

# Logging a stderr: en stdio, stdout es el canal del protocolo MCP.
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)

if __name__ == "__main__":
    mcp.run()
