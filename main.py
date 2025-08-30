from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/")
async def get_hello():
    return {"status": "ok"}


# if __name__ == "__main__":
#     main()
