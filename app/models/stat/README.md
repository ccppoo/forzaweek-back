# stat

stat 항목들은 Pydantic - BaseModel 상속 받아서 만든 Component 형태임 (MongoDB Document로 직접 저장 X)

## FH5

### CarBaseStat_FH5

자동차 정보 검색할 때 기본으로 제공하는 정보

1. Performance (0 ... 10)
2. Meta (가격, 기본 PI, division, rarity)

### TuningStat_FH5

튜닝 글 작성할 때 세부적인 차 성능 파츠 제공하는 정보

1. PI
2. detailedTuning (damping, spring, ...)
3. performance (0 ... 10)
4. testReadings (0-100kmh, kg, ... )
5. tuningMajorParts (AWD/RWD/FWD, suspension type, tire type)
