# Car Model

이 Car는 게임에 종속된 차에 대한 정보 X

포르자 호라이즌4, 포르자 호라이즌5, 등 차에 대한 세부 정보는 각자 Document 정보를 통해서 저장될 예정임

## Car Document과 인게임 정보를 분리하는 방식

예시 - `Chevrolet C8 2020`

Car Document에 저장되는 정보 (게임에 상관없이 불변하는 정보)

- 차 출시일
- 차 엔진 타입
- 제조사, 제조일
- 엔진, 좌석수, 문 정보

인게임 자동차 정보는

`FH5/car` FH5.Car 에 저장됨

- PI 스탯
- Driving System 개조 가능 여부 (AWD, FWD, RWD)
- 튜닝 가능 여부
- 바닐라 최고속도, 성능표
