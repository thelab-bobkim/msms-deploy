# 🚀 MSMS Lightsail 배포 - 빠른 시작 가이드

## 📋 사전 준비사항
- AWS Lightsail 서버: **43.203.181.195**
- SSH 접속 가능
- Ubuntu 20.04 이상

---

## 방법 1: 파일 직접 업로드 (가장 빠름) ⭐

### 1️⃣ 샌드박스에서 다운로드
`/home/user/webapp/msms_lightsail_deploy.tar.gz` (448KB) 파일을 로컬 PC로 다운로드

### 2️⃣ Lightsail 서버에 업로드
```bash
# 로컬 PC에서 실행
scp msms_lightsail_deploy.tar.gz ubuntu@43.203.181.195:/home/ubuntu/
```

### 3️⃣ Lightsail SSH에서 실행
```bash
# SSH 접속
ssh ubuntu@43.203.181.195

# 압축 해제
cd /home/ubuntu
tar -xzf msms_lightsail_deploy.tar.gz
cd msms_lightsail_deploy

# 배포 스크립트 실행
chmod +x setup.sh
./setup.sh
```

---

## 방법 2: GitHub 사용 (추천)

### 1️⃣ 젠스파이크에서 GitHub 업로드
1. 젠스파이크 화면 상단 **#github** 탭 클릭
2. GitHub 앱 설치 및 권한 부여
3. 저장소 선택 또는 새로 생성 (예: `msms-deploy`)

### 2️⃣ Lightsail SSH에서 실행
```bash
# SSH 접속
ssh ubuntu@43.203.181.195

# GitHub에서 다운로드 (저장소 이름 변경 필요)
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/msms-deploy.git
cd msms-deploy

# 배포 스크립트 실행
chmod +x setup.sh
./setup.sh
```

---

## 방법 3: 개별 파일 붙여넣기 (수동)

### 3️⃣ Lightsail SSH에서 개별 파일 생성

```bash
# SSH 접속
ssh ubuntu@43.203.181.195

# 디렉토리 생성
cd /home/ubuntu
mkdir -p msms_lightsail_deploy
cd msms_lightsail_deploy

# 1. requirements_lightsail.txt 생성
cat > requirements_lightsail.txt << 'EOF'
streamlit==1.31.0
pandas==2.2.0
numpy==1.26.3
openpyxl==3.1.2
python-dateutil==2.8.2
EOF

# 2. setup.sh 다운로드 (아래 긴 스크립트 대신 wget 사용 가능)
# 파일이 크므로 GitHub나 파일 업로드 권장

# 3. msms.db 파일 업로드 필요 (1MB, 수동 업로드 권장)

# 4. app_sqlite_v2.py 파일 업로드 필요 (49KB, 수동 업로드 권장)
```

---

## ✅ 배포 완료 후 확인

### 서비스 상태 확인
```bash
sudo systemctl status msms
```

### 웹 접속
브라우저에서 접속:
```
http://43.203.181.195:8501
```

### 데이터 검증
```bash
sqlite3 /home/ubuntu/msms/msms.db "SELECT COUNT(*) FROM projects;"
# 예상 출력: 573

sqlite3 /home/ubuntu/msms/msms.db "SELECT COUNT(*) FROM purchases;"
# 예상 출력: 1281
```

---

## 🔧 문제 해결

### 포트가 열리지 않는 경우
```bash
# 방화벽 확인
sudo ufw status

# 포트 8501 열기
sudo ufw allow 8501/tcp
sudo ufw reload
```

### AWS Lightsail 콘솔에서 방화벽 설정
1. Lightsail 콘솔 접속
2. 인스턴스 선택 → "네트워킹" 탭
3. 방화벽 규칙 추가: **사용자 지정 TCP, 포트 8501**

### 서비스 로그 확인
```bash
sudo journalctl -u msms -f
```

---

## 🎯 예상 결과

배포 성공 시 다음 정보가 표시됩니다:
- **총 프로젝트**: 573개
- **영업담당자**: 22명
- **매출처**: 237개
- **고객사**: 256개
- **매입 건수**: 1,281개

---

**접속 URL**: http://43.203.181.195:8501  
**배포 완료 시간**: 약 5분  
**마지막 업데이트**: 2026-02-05
