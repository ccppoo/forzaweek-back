# Microsoft

## token configuration

### token claims reference

[token claims reference](https://learn.microsoft.com/en-us/entra/identity-platform/id-token-claims-reference)

토큰 구성 내용

### lifetime

[access-tokens#token-lifetime](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens#token-lifetime)

### lifetime configuration

[configurable-token-lifetime-properties](https://learn.microsoft.com/en-us/entra/identity-platform/configurable-token-lifetimes#configurable-token-lifetime-properties)

개발용으로 토큰 수명 줄이고 싶은데 `POST` data 부분에 뭘 넣어야할지 모르겠음

### JWT, kid

[MS JWT keys](https://login.microsoftonline.com/common/discovery/v2.0/keys)

JWT 검증할 때 사용하는 key 내용 담긴 JSON 파일

갱신하는 주기가 얼마나 되는지는 모르지만, 파일로 저장해서 사용하는건 XX

#### 서명의 유효성 검사

[서명의 유효성 검사](https://learn.microsoft.com/ko-kr/entra/identity-platform/access-tokens#validate-the-signature)

> 특정 시점에 Microsoft Entra ID는 특정 공용-프라이빗 키 쌍 집합 중 하나를 사용하여 ID 토큰에 서명할 수 있습니다. Microsoft Entra ID는 주기적으로 가능한 키 집합을 회전하므로 해당 키 변경 내용을 자동으로 처리하도록 애플리케이션을 작성합니다. Microsoft Entra ID에서 사용하는 공개 키에 대한 업데이트를 확인하는 합리적인 빈도는 24시간마다입니다.

Redis 같은 전역 캐시로 변경 내용있는지 확인하고 주기적으로 업데이트할 필요가 있음
