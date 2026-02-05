# MSMS Lightsail 배포 가이드

## 📋 개요
이 패키지는 젠스파이크 샌드박스에서 개발한 MSMS 애플리케이션을 AWS Lightsail 서버에 배포하기 위한 모든 파일과 스크립트를 포함합니다.

## 🎯 배포 목표
- **서버 IP**: 43.203.181.195
- **포트**: 8501
- **접속 URL**: http://43.203.181.195:8501

## 📦 포함된 파일
1. **app_sqlite_v2.py** (50KB) - MSMS Streamlit 애플리케이션
2. **msms.db** (1MB) - SQLite 데이터베이스
   - 프로젝트: 573개
   - 매입: 1,281개
   - 매출처: 842개
   - 고객사: 256개
3. **requirements_lightsail.txt** - Python 패키지 의존성
4. **setup.sh** - 자동 배포 스크립트

## 🚀 빠른 배포 (Lightsail SSH에서 실행)

### 방법 1: GitHub에서 직접 다운로드 (추천)

```bash
# 1. GitHub에서 배포 패키지 다운로드
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/msms-deploy.git
cd msms-deploy

# 2. 배포 스크립트 실행
chmod +x setup.sh
./setup.sh
```

### 방법 2: wget으로 다운로드

```bash
# 1. 배포 패키지 다운로드
cd /home/ubuntu
wget https://github.com/YOUR_USERNAME/msms-deploy/archive/refs/heads/main.zip
unzip main.zip
cd msms-deploy-main

# 2. 배포 스크립트 실행
chmod +x setup.sh
./setup.sh
```

### 방법 3: 수동 복사 (파일 개별 업로드)

파일을 수동으로 Lightsail 서버에 업로드한 경우:

```bash
# 1. 업로드한 디렉토리로 이동
cd /home/ubuntu/msms-deploy  # 또는 파일을 업로드한 디렉토리

# 2. 배포 스크립트 실행
chmod +x setup.sh
./setup.sh
```

## ✅ 배포 후 확인사항

### 1. 서비스 상태 확인
```bash
sudo systemctl status msms
```

### 2. 로그 확인
```bash
sudo journalctl -u msms -f
```

### 3. 데이터베이스 검증
```bash
sqlite3 /home/ubuntu/msms/msms.db "SELECT COUNT(*) FROM projects;"
# 예상 출력: 573
```

### 4. 웹 접속 테스트
브라우저에서 접속: http://43.203.181.195:8501

## 🔧 서비스 관리 명령어

```bash
# 서비스 시작
sudo systemctl start msms

# 서비스 중지
sudo systemctl stop msms

# 서비스 재시작
sudo systemctl restart msms

# 서비스 상태 확인
sudo systemctl status msms

# 로그 실시간 확인
sudo journalctl -u msms -f

# 로그 최근 50줄
sudo journalctl -u msms -n 50
```

## 🛠️ 문제 해결

### 포트 8501이 열리지 않는 경우
```bash
# 방화벽 확인
sudo ufw status

# 포트 8501 열기
sudo ufw allow 8501/tcp
sudo ufw reload
```

### Lightsail 인스턴스 방화벽 설정
1. AWS Lightsail 콘솔 접속
2. 인스턴스 선택
3. "네트워킹" 탭
4. "방화벽" 섹션에서 "규칙 추가"
5. 사용자 지정 TCP, 포트 8501 추가

### 서비스가 시작되지 않는 경우
```bash
# 로그 확인
sudo journalctl -u msms -n 100

# Python 패키지 재설치
cd /home/ubuntu/msms
source venv/bin/activate
pip install --upgrade -r requirements_lightsail.txt

# 서비스 재시작
sudo systemctl restart msms
```

### 데이터베이스 파일이 없는 경우
```bash
# 파일 존재 확인
ls -lh /home/ubuntu/msms/msms.db

# 파일이 없으면 다시 복사
cp ~/msms-deploy/msms.db /home/ubuntu/msms/
sudo systemctl restart msms
```

## 📊 예상 데이터 수치

배포가 성공적으로 완료되면 다음 데이터가 표시됩니다:

- **총 프로젝트**: 573개
- **영업담당자**: 22명
- **매출처**: 237개
- **고객사**: 256개
- **매입 건수**: 1,281개

## 📝 시스템 요구사항

- **OS**: Ubuntu 20.04 이상
- **Python**: 3.12
- **RAM**: 최소 1GB (권장 2GB)
- **디스크**: 최소 500MB

## 🔄 업데이트 방법

```bash
# 1. 서비스 중지
sudo systemctl stop msms

# 2. 백업 생성
cp /home/ubuntu/msms/msms.db /home/ubuntu/msms/msms.db.backup

# 3. 새 파일로 교체
cp ~/msms-deploy/app_sqlite_v2.py /home/ubuntu/msms/
cp ~/msms-deploy/msms.db /home/ubuntu/msms/

# 4. 서비스 재시작
sudo systemctl restart msms
```

## 📧 지원

문제가 발생하면 다음 정보를 확인하세요:
1. 서비스 로그: `sudo journalctl -u msms -n 100`
2. 방화벽 상태: `sudo ufw status`
3. Python 버전: `python3.12 --version`
4. 패키지 설치: `pip list`

---

**마지막 업데이트**: 2026-02-05  
**버전**: 1.0.0  
**배포 환경**: AWS Lightsail Ubuntu 20.04
