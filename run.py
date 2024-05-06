import uvicorn
from uvicorn_setting import UvicornSettings
from argparser import args

if __name__ == "__main__":
    ENV_FILE = f"./uvicorn/.{args.mode}.env"
    APP_ENV_FILE = f"./envs/.{args.mode}.env"

    settings = UvicornSettings(_env_file=ENV_FILE)

    uvicorn.run(
        "app.main:app",
        **settings.model_dump(),
        env_file=APP_ENV_FILE,
        ssl_certfile="./ssl/cert.pem",
        ssl_keyfile="./ssl/key.pem",
    )
