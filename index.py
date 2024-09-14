from src.frontend.streamlit import run_st
from src.utils.streamlit import check_streamlit
from src.server import app
import uvicorn


def main():
    if check_streamlit():
        run_st()
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
