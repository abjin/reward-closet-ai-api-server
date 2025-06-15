# Reward Closet AI API Server

의류 분류 및 결함 검출을 위한 AI 기반 API 서버입니다. PyTorch TorchScript 모델을 사용하여 의류 이미지를 15개 카테고리로 분류하고 결함을 검출합니다.

## 🚀 주요 기능

- **의류 분류**: 이미지 URL을 통한 의류 타입 분류
- **결함 검출**: 의류의 찢어짐, 오염, 마모 등 결함 감지
- **높은 성능**: TorchScript 최적화된 모델로 빠른 추론
- **다양한 배포 방식**: Docker 로컬, AWS Elastic Beanstalk, Docker Compose + Nginx
- **확장성**: AWS 클라우드 기반 자동 스케일링 지원

## 📋 분류 카테고리

### 의류 타입
- jacket (재킷)
- short pants (반바지)
- tailored pants (정장 바지)
- jumper (점퍼)
- shirts (셔츠)
- coat (코트)
- dress (드레스)
- casual pants (캐주얼 바지)
- blouse (블라우스)
- tshirts (티셔츠)
- skirt (치마)

### 결함 타입
- ripped (찢어짐)
- pollution (오염)
- tearing (해짐)
- frayed (닳음)

## 🛠 기술 스택

- **Framework**: FastAPI
- **AI/ML**: PyTorch, TorchScript, OpenCV
- **Image Processing**: PIL, NumPy
- **Deployment**: Docker, Nginx
- **Runtime**: Python 3.10

## 📦 설치 및 실행

### 로컬 개발 환경

1. **저장소 클론**
```bash
git clone <repository-url>
cd reward-closet-ai-api-server
```

2. **가상환경 설정**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate  # Windows
```

3. **의존성 설치**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

4. **서버 실행**
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### Docker 로컬 배포

1. **Docker 이미지 빌드**
```bash
docker build -t reward-closet-ai-api-server .
```

2. **컨테이너 실행**
```bash
docker run -p 8000:8000 reward-closet-ai-api-server
```

3. **Docker Compose로 전체 스택 실행**
```bash
docker-compose up -d
```

### AWS Elastic Beanstalk 배포

#### 사전 준비
- AWS CLI 설치 및 구성
- Elastic Beanstalk CLI (EB CLI) 설치
- Docker Hub 계정 (이미지 푸시용)

#### 배포 과정

1. **Docker 이미지 빌드 및 푸시**
```bash
# 이미지 빌드
docker build -t abjin/reward-closet-ai-api-server:latest .

# Docker Hub에 푸시
docker push abjin/reward-closet-ai-api-server:latest
```

2. **Elastic Beanstalk 환경 초기화**
```bash
# EB 초기화
eb init

# 애플리케이션 이름: reward-closet-ai-api-server
# 플랫폼: Docker
# 리전: 원하는 AWS 리전 선택
```

3. **환경 생성 및 배포**
```bash
# 환경 생성
eb create production

# 배포
eb deploy
```

4. **환경 상태 확인**
```bash
# 상태 확인
eb status

# 로그 확인
eb logs

# 애플리케이션 열기
eb open
```

#### Dockerrun.aws.json 설정
프로젝트에 포함된 `Dockerrun.aws.json` 파일은 Elastic Beanstalk에서 Docker 컨테이너를 실행하기 위한 설정을 정의합니다:

- **이미지**: `abjin/reward-closet-ai-api-server:latest` (Docker Hub에서 가져옴)
- **포트**: 8000 (FastAPI 애플리케이션 포트)
- **자동 업데이트**: 새로운 이미지 버전 자동 적용

이 파일이 프로젝트 루트에 있으면 Elastic Beanstalk가 자동으로 인식하여 배포에 사용합니다.

#### 환경 변수 설정
Elastic Beanstalk 콘솔에서 다음 환경 변수들을 설정할 수 있습니다:
- `PORT`: 8000 (기본값)
- `PYTHONPATH`: /app
- 기타 필요한 환경 변수

### 프로덕션 배포 (Docker + Nginx)

Nginx 프록시와 함께 프로덕션 환경에서 배포:

```bash
# Docker Compose로 전체 스택 배포
docker-compose up -d

# 또는 자동화된 빌드 및 배포 스크립트 실행
./start.sh
```

#### 자동화된 배포 스크립트 (start.sh)
`start.sh` 스크립트는 다음 작업을 자동으로 수행합니다:

```bash
#!/bin/bash
# Docker 이미지 빌드
docker build . --tag abjin/reward-closet-ai-api-server:latest

# Docker Hub에 이미지 푸시 (Elastic Beanstalk 배포용)
docker push abjin/reward-closet-ai-api-server:latest
```

이 스크립트를 실행하면:
1. 최신 코드로 Docker 이미지가 빌드됩니다
2. Docker Hub에 이미지가 업로드됩니다
3. Elastic Beanstalk에서 새로운 이미지를 자동으로 배포할 수 있습니다

## 🌐 API 사용법

### Base URL
- 로컬 개발: `http://localhost:8000`
- Docker Compose: `http://localhost` (Nginx 프록시를 통해)
- AWS Elastic Beanstalk: `http://your-app-name.region.elasticbeanstalk.com`
- 프로덕션: 커스텀 도메인 (설정된 경우)

### API 엔드포인트

#### 의류 분류 예측
```http
POST /models/clothes/predict
Content-Type: application/json

{
  "url": "https://example.com/image.jpg"
}
```

**응답 예시:**
```json
{
  "top1ClassName": "tshirts",
  "top1Score": 0.95
}
```

#### 헬스 체크
```http
GET /health
```

### API 문서
서버 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📁 프로젝트 구조

```
reward-closet-ai-api-server/
├── src/
│   ├── app.py                 # FastAPI 메인 애플리케이션
│   ├── api/                   # API 라우터
│   │   ├── models.py          # 모델 예측 라우터
│   │   └── health_check.py    # 헬스 체크 라우터
│   ├── service/               # 비즈니스 로직
│   │   └── models.py          # 모델 추론 서비스
│   ├── ai/                    # AI 모델 관련
│   │   ├── session/           # 모델 세션
│   │   │   └── clothes.py     # 의류 분류 모델
│   │   └── torchscript/       # TorchScript 모델 파일
│   ├── dto/                   # 데이터 전송 객체
│   │   └── models.py          # API 요청/응답 모델
│   └── exception_handler.py   # 예외 처리
├── docker-compose.yml         # Docker Compose 설정
├── Dockerfile                 # Docker 이미지 빌드 설정
├── Dockerrun.aws.json         # Elastic Beanstalk Docker 설정
├── nginx.conf                 # Nginx 프록시 설정
├── requirements.txt           # Python 의존성
├── start.sh                   # 배포 스크립트
└── README.md                  # 프로젝트 문서
```

## 🔧 주요 의존성

```
fastapi==0.115.6
uvicorn==0.32.1
torch==2.2.2
torchvision==0.17.2
opencv-python==4.10.0.84
pillow==11.0.0
numpy==1.26.4
requests==2.32.3
pydantic==2.10.3
```

## 🚦 개발 가이드라인

### 코드 스타일
- Python PEP 8 준수
- Type hints 사용 권장
- Pydantic 모델을 통한 데이터 검증

### 모델 업데이트
1. 새로운 TorchScript 모델을 `src/ai/torchscript/` 디렉토리에 배치
2. `src/ai/session/clothes.py`에서 모델 경로 및 레이블 업데이트
3. 필요시 전처리 로직 수정

## 📊 성능 최적화

- **TorchScript**: 모델 추론 속도 최적화
- **CPU 전용**: GPU 의존성 제거로 범용성 향상
- **이미지 전처리**: OpenCV와 PIL을 통한 효율적인 이미지 처리
- **NMS**: Non-Maximum Suppression을 통한 중복 검출 제거

## 🐛 문제 해결

### 일반적인 오류

1. **모델 파일 없음**
   - TorchScript 모델 파일이 올바른 경로에 있는지 확인
   - 모델 파일의 권한 확인

2. **이미지 로드 실패**
   - 이미지 URL의 접근 가능성 확인
   - 지원되는 이미지 형식인지 확인 (JPEG, PNG 등)

3. **메모리 부족**
   - 이미지 크기가 너무 큰 경우 리사이징 필요
   - 배치 처리 시 배치 크기 조정

### Elastic Beanstalk 관련 문제

1. **배포 실패**
   - Docker Hub에 이미지가 올바르게 푸시되었는지 확인
   - `Dockerrun.aws.json` 파일의 이미지 이름 확인
   - AWS 권한 설정 확인

2. **애플리케이션 시작 실패**
   - `eb logs`로 상세 로그 확인
   - 환경 변수 설정 확인
   - 포트 설정 확인 (기본값: 8000)

3. **성능 문제**
   - EC2 인스턴스 타입 확인 (CPU 집약적 작업)
   - 로드 밸런서 설정 확인
   - Auto Scaling 설정 검토

### Docker 관련 문제

1. **컨테이너 빌드 실패**
   - Docker 이미지 크기 확인 (PyTorch로 인해 클 수 있음)
   - 의존성 설치 과정에서 오류 확인
   - 네트워크 연결 확인

2. **컨테이너 실행 오류**
   - 포트 충돌 확인
   - 볼륨 마운트 권한 확인
   - 환경 변수 설정 확인

## 📄 라이선스

MIT License

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 지원

문제가 발생하거나 질문이 있으시면 Issues 탭에서 문의해 주세요.
