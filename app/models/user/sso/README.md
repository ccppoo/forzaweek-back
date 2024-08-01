# User :: SSO

## microsoft (xbox)

```py
# python
class XboxUserInfo(BaseModel):
    gamer_tag: str
    user_hash: str
    xuid: str

class MircrosoftUserInfo(BaseModel):
    uid: str 
    email: str 
    xbox: XboxUserInfo
```

```json
// JSON
{
    "uid" : "AAAAAAAAAA...",
    "email" : "user@example.com", // email used for logging in MS account,
    "xbox" : {
        "gamer_tag" : "game_player123", // gamer tag (username displayed in game, xbox apps, ect.)
        "user_hash" : "123123123123", // unknown
        "xuid" : "123123123123123" // Xbox User ID
    }
}
```
