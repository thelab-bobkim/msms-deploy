# 🎉 MSMS Lightsail 배포 패키지 완성!

배포 패키지가 준비되었습니다. 이제 AWS Lightsail 서버 (43.203.181.195:8501)에 배포할 수 있습니다.

---

## 📦 패키지 위치
- **샌드박스 경로**: `/home/user/webapp/msms_lightsail_deploy/`
- **압축 파일**: `/home/user/webapp/msms_lightsail_deploy.tar.gz` (448KB)

---

## 🚀 Lightsail SSH 배포 - 3가지 방법

### 방법 1: 파일 다운로드 + SCP 업로드 (가장 빠름) ⭐

#### 1️⃣ 샌드박스에서 다운로드
브라우저에서 다운로드:
```
/home/user/webapp/msms_lightsail_deploy.tar.gz
```

#### 2️⃣ 로컬 PC에서 Lightsail로 업로드
```bash
scp msms_lightsail_deploy.tar.gz ubuntu@43.203.181.195:/home/ubuntu/
```

#### 3️⃣ Lightsail SSH에서 실행
```bash
# SSH 접속
ssh ubuntu@43.203.181.195

# 압축 해제
cd /home/ubuntu
tar -xzf msms_lightsail_deploy.tar.gz
cd msms_lightsail_deploy

# 배포 스크립트 실행 (5분 소요)
chmod +x setup.sh
./setup.sh
```

#### 4️⃣ 접속 확인
브라우저: **http://43.203.181.195:8501**

---

### 방법 2: GitHub 사용 (권장)

#### 1️⃣ 젠스파이크에서 GitHub 업로드
1. 화면 상단 **#github** 탭 클릭
2. GitHub 앱 연결 및 저장소 선택 (예: `msms-deploy`)
3. 배포 패키지 푸시

#### 2️⃣ Lightsail SSH에서 실행
```bash
# SSH 접속
ssh ubuntu@43.203.181.195

# GitHub에서 클론
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/msms-deploy.git
cd msms-deploy

# 배포 실행
chmod +x setup.sh
./setup.sh
```

---

### 방법 3: 개별 파일 수동 생성 (고급 사용자)

Lightsail SSH에서 직접 파일을 생성하고 실행합니다. 자세한 내용은 `QUICK_START.md` 참조.

---

## 🎯 setup.sh 스크립트가 수행하는 작업

```bash
./setup.sh
```

실행 시 자동으로 다음 작업을 수행합니다:

1. ✅ 시스템 업데이트 (`apt-get update && upgrade`)
2. ✅ Python 3.12 설치
3. ✅ 프로젝트 디렉토리 생성 (`/home/ubuntu/msms`)
4. ✅ Python 가상환경 생성 (`venv`)
5. ✅ 필수 패키지 설치 (Streamlit, pandas, numpy 등)
6. ✅ 방화벽 설정 (포트 8501 오픈)
7. ✅ Systemd 서비스 생성 및 등록
8. ✅ 서비스 자동 시작
9. ✅ 데이터베이스 검증

**소요 시간**: 약 5분

---

## ✅ 배포 성공 확인

### 1. 서비스 상태 확인
```bash
sudo systemctl status msms
```

출력 예시:
```
● msms.service - MSMS Streamlit Application
   Active: active (running) since ...
```

### 2. 데이터베이스 검증
```bash
cd /home/ubuntu/msms
sqlite3 msms.db "SELECT COUNT(*) FROM projects;"
```

출력 예시:
```
573
```

### 3. 웹 접속 확인
브라우저에서 접속: **http://43.203.181.195:8501**

예상 화면:
- 총 프로젝트: **573개**
- 영업담당자: **22명**
- 매출처: **237개**
- 고객사: **256개**
- 매입 건수: **1,281개**

---

## 🔧 서비스 관리

### 서비스 시작/중지
```bash
sudo systemctl start msms      # 시작
sudo systemctl stop msms       # 중지
sudo systemctl restart msms    # 재시작
sudo systemctl status msms     # 상태 확인
```

### 로그 확인
```bash
sudo journalctl -u msms -f              # 실시간 로그
sudo journalctl -u msms -n 100          # 최근 100줄
```

---

## 🛠️ 문제 해결

### 포트가 열리지 않는 경우

#### 1. UFW 방화벽 확인
```bash
sudo ufw status
sudo ufw allow 8501/tcp
sudo ufw reload
```

#### 2. AWS Lightsail 콘솔 방화벽 설정
1. AWS Lightsail 콘솔 접속
2. 인스턴스 선택 → **네트워킹** 탭
3. 방화벽 규칙 추가:
   - 애플리케이션: **사용자 지정**
   - 프로토콜: **TCP**
   - 포트: **8501**

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
# 파일 확인
ls -lh /home/ubuntu/msms/msms.db

# 파일이 없으면 다시 복사
cp ~/msms_lightsail_deploy/msms.db /home/ubuntu/msms/
sudo systemctl restart msms
```

---

## 📋 패키지 파일 목록

```
msms_lightsail_deploy/
├── app_sqlite_v2.py              (49KB)  - MSMS Streamlit 애플리케이션
├── msms.db                       (1MB)   - SQLite 데이터베이스
├── requirements_lightsail.txt    (85B)   - Python 패키지 의존성
├── setup.sh                      (4.2KB) - 자동 배포 스크립트
├── README.md                     (4.3KB) - 상세 배포 가이드
├── QUICK_START.md                (2.3KB) - 빠른 시작 가이드
└── .gitignore                    (265B)  - Git 제외 파일
```

---

## 📊 데이터베이스 정보

- **프로젝트**: 573개
- **매입**: 1,281개
- **매출처**: 842개
- **고객사**: 256개
- **영업담당자**: 22명
- **매출처 품목**: 1,712개

---

## 🔄 업데이트 방법

```bash
# 서비스 중지
sudo systemctl stop msms

# 백업 생성
cp /home/ubuntu/msms/msms.db /home/ubuntu/msms/msms.db.backup.$(date +%Y%m%d_%H%M%S)

# 새 파일로 교체
cp ~/msms_lightsail_deploy/app_sqlite_v2.py /home/ubuntu/msms/
cp ~/msms_lightsail_deploy/msms.db /home/ubuntu/msms/

# 서비스 재시작
sudo systemctl restart msms
```

---

## 📞 지원

### 로그 수집
문제 발생 시 다음 정보를 확인하세요:

```bash
# 서비스 로그
sudo journalctl -u msms -n 100 > msms_logs.txt

# 방화벽 상태
sudo ufw status > firewall_status.txt

# 시스템 정보
python3.12 --version > system_info.txt
pip list >> system_info.txt
```

---

**접속 URL**: http://43.203.181.195:8501  
**배포 시간**: 약 5분  
**마지막 업데이트**: 2026-02-05  
**버전**: 1.0.0

🎉 **배포 성공을 기원합니다!**
