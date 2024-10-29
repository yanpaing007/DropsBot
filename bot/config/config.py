from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    REF_ID: str = 'V101C'
    
    FAKE_USERAGENT: bool = False
    MIN_DELAY: list[int] = [2,5]
    BIG_SLEEP_TIME: list[int] = [3900,4000]
    TASK_SLEEP_TIME : list[int] = [40,60]
    
    AUTO_CLAIM_REFERRAL: bool = True
    AUTO_CLAIM_DAILY_BONUS: bool = True
    AUTO_CLAIM_REFERRAL_BONUS: bool = True
    AUTO_CLAIM_WELCOME_BONUS: bool = True
    AUTO_FINISH_TASK: bool = True
    AUTO_PLACE_ORDER: bool = True
    
    
    

    USE_RANDOM_DELAY_IN_RUN: bool = True
    RANDOM_DELAY_IN_RUN: list[int] = [5, 15]

    USE_PROXY_FROM_FILE: bool = False


settings = Settings()

