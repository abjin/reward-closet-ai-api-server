# Reward Closet AI API Server

An AI-based API server for clothing classification and defect detection. Uses PyTorch TorchScript models to classify clothing images into 15 categories and detect defects.

## 🚀 Key Features

- **Clothing Classification**: Classify clothing types through image URLs
- **Defect Detection**: Detect clothing defects such as tears, stains, wear, etc.
- **High Performance**: Fast inference with TorchScript optimized models
- **Multiple Deployment Options**: Docker local, AWS Elastic Beanstalk, Docker Compose + Nginx
- **Scalability**: AWS cloud-based auto-scaling support

## 📋 Classification Categories

### Clothing Types
- jacket
- short pants
- tailored pants
- jumper
- shirts
- coat
- dress
- casual pants
- blouse
- tshirts
- skirt

### Defect Types
- ripped
- pollution
- tearing
- frayed

## 🛠 Tech Stack

- **Framework**: FastAPI
- **AI/ML**: PyTorch, TorchScript, OpenCV
- **Image Processing**: PIL, NumPy
- **Deployment**: Docker, Nginx
- **Runtime**: Python 3.10

## 📦 Installation and Setup

### Local Development Environment

1. **Clone Repository**
```bash
git clone <repository-url>
cd reward-closet-ai-api-server
```

2. **Setup Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

4. **Run Server**
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Local Deployment

1. **Build Docker Image**
```bash
docker build -t reward-closet-ai-api-server .
```

2. **Run Container**
```bash
docker run -p 8000:8000 reward-closet-ai-api-server
```

3. **Run Full Stack with Docker Compose**
```bash
docker-compose up -d
```

### AWS Elastic Beanstalk Deployment

#### Prerequisites
- AWS CLI installed and configured
- Elastic Beanstalk CLI (EB CLI) installed
- Docker Hub account (for image push)

#### Deployment Process

1. **Build and Push Docker Image**
```bash
# Build image
docker build -t abjin/reward-closet-ai-api-server:latest .

# Push to Docker Hub
docker push abjin/reward-closet-ai-api-server:latest
```

2. **Initialize Elastic Beanstalk Environment**
```bash
# Initialize EB
eb init

# Application name: reward-closet-ai-api-server
# Platform: Docker
# Region: Select desired AWS region
```

3. **Create Environment and Deploy**
```bash
# Create environment
eb create production

# Deploy
eb deploy
```

4. **Check Environment Status**
```bash
# Check status
eb status

# Check logs
eb logs

# Open application
eb open
```

#### Dockerrun.aws.json Configuration
The `Dockerrun.aws.json` file included in the project defines the configuration for running Docker containers in Elastic Beanstalk:

- **Image**: `abjin/reward-closet-ai-api-server:latest` (pulled from Docker Hub)
- **Port**: 8000 (FastAPI application port)
- **Auto Update**: Automatic application of new image versions

When this file is in the project root, Elastic Beanstalk automatically recognizes and uses it for deployment.

#### Environment Variables Configuration
The following environment variables can be set in the Elastic Beanstalk console:
- `PORT`: 8000 (default)
- `PYTHONPATH`: /app
- Other required environment variables

### Production Deployment (Docker + Nginx)

Deploy in production environment with Nginx proxy:

```bash
# Deploy full stack with Docker Compose
docker-compose up -d

# Or run automated build and deployment script
./start.sh
```

#### Automated Deployment Script (start.sh)
The `start.sh` script automatically performs the following tasks:

```bash
#!/bin/bash
# Build Docker image
docker build . --tag abjin/reward-closet-ai-api-server:latest

# Push image to Docker Hub (for Elastic Beanstalk deployment)
docker push abjin/reward-closet-ai-api-server:latest
```

When you run this script:
1. Docker image is built with the latest code
2. Image is uploaded to Docker Hub
3. Elastic Beanstalk can automatically deploy the new image

## 🌐 API Usage

### Base URL
- Local Development: `http://localhost:8000`
- Docker Compose: `http://localhost` (through Nginx proxy)
- AWS Elastic Beanstalk: `http://your-app-name.region.elasticbeanstalk.com`
- Production: Custom domain (if configured)

### API Endpoints

#### Clothing Classification Prediction
```http
POST /models/clothes/predict
Content-Type: application/json

{
  "url": "https://example.com/image.jpg"
}
```

**Response Example:**
```json
{
  "top1ClassName": "tshirts",
  "top1Score": 0.95
}
```

#### Health Check
```http
GET /health
```

### API Documentation
After running the server, you can view auto-generated API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📁 Project Structure

```
reward-closet-ai-api-server/
├── src/
│   ├── app.py                 # FastAPI main application
│   ├── api/                   # API routes
│   │   ├── models.py          # Model prediction router
│   │   └── health_check.py    # Health check router
│   ├── service/               # Business logic
│   │   └── models.py          # Model inference service
│   ├── ai/                    # AI model related
│   │   ├── session/           # Model sessions
│   │   │   └── clothes.py     # Clothing classification model
│   │   └── torchscript/       # TorchScript model files
│   ├── dto/                   # Data transfer objects
│   │   └── models.py          # API request/response models
│   └── exception_handler.py   # Exception handling
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker image build configuration
├── Dockerrun.aws.json         # Elastic Beanstalk Docker configuration
├── nginx.conf                 # Nginx proxy configuration
├── requirements.txt           # Python dependencies
├── start.sh                   # Deployment script
└── README.md                  # Project documentation
```

## 🔧 Key Dependencies

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

## 🚦 Development Guidelines

### Code Style
- Follow Python PEP 8
- Use type hints when possible
- Data validation through Pydantic models

### Model Updates
1. Place new TorchScript models in the `src/ai/torchscript/` directory
2. Update model path and labels in `src/ai/session/clothes.py`
3. Modify preprocessing logic if necessary

## 📊 Performance Optimization

- **TorchScript**: Optimized model inference speed
- **CPU Only**: Improved versatility by removing GPU dependencies
- **Image Preprocessing**: Efficient image processing with OpenCV and PIL
- **NMS**: Non-Maximum Suppression for duplicate detection removal

## 🐛 Troubleshooting

### Common Errors

1. **Model File Missing**
   - Check if TorchScript model file is in the correct path
   - Verify model file permissions

2. **Image Load Failure**
   - Check image URL accessibility
   - Verify supported image formats (JPEG, PNG, etc.)

3. **Memory Issues**
   - Resize images if they are too large
   - Adjust batch size for batch processing

### Elastic Beanstalk Related Issues

1. **Deployment Failure**
   - Verify image is correctly pushed to Docker Hub
   - Check image name in `Dockerrun.aws.json` file
   - Verify AWS permissions configuration

2. **Application Start Failure**
   - Check detailed logs with `eb logs`
   - Verify environment variable configuration
   - Check port configuration (default: 8000)

3. **Performance Issues**
   - Check EC2 instance type (CPU intensive tasks)
   - Review load balancer configuration
   - Review Auto Scaling settings

### Docker Related Issues

1. **Container Build Failure**
   - Check Docker image size (can be large due to PyTorch)
   - Check for errors during dependency installation
   - Verify network connectivity

2. **Container Runtime Errors**
   - Check for port conflicts
   - Verify volume mount permissions
   - Check environment variable configuration

## 📄 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions, please reach out through the Issues tab. 