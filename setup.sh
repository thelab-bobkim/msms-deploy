#!/bin/bash

# ========================================
# MSMS Lightsail 배포 스크립트
# AWS Lightsail 서버에 MSMS 앱 배포
# ========================================

set -e  # 에러 발생 시 중단

echo "================================"
echo "MSMS Lightsail 배포 시작"
echo "================================"
echo ""

# 현재 디렉토리 확인
CURRENT_DIR=$(pwd)
echo "현재 디렉토리: $CURRENT_DIR"
echo ""

# 1. 시스템 업데이트
echo "1️⃣  시스템 업데이트 중..."
sudo apt-get update -y
sudo apt-get upgrade -y
echo "✅ 시스템 업데이트 완료"
echo ""

# 2. Python 3.12 설치
echo "2️⃣  Python 3.12 설치 중..."
sudo apt-get install -y python3.12 python3.12-venv python3-pip
echo "✅ Python 3.12 설치 완료"
python3.12 --version
echo ""

# 3. 프로젝트 디렉토리 생성 및 파일 이동
echo "3️⃣  프로젝트 디렉토리 설정 중..."
cd /home/ubuntu
mkdir -p msms

# 현재 디렉토리에서 파일 복사
if [ -f "$CURRENT_DIR/app_sqlite_v2.py" ]; then
    cp "$CURRENT_DIR/app_sqlite_v2.py" /home/ubuntu/msms/
    cp "$CURRENT_DIR/msms.db" /home/ubuntu/msms/
    cp "$CURRENT_DIR/requirements_lightsail.txt" /home/ubuntu/msms/
    echo "✅ 파일 복사 완료"
else
    echo "❌ 파일을 찾을 수 없습니다. GitHub에서 다운로드했는지 확인해주세요."
    exit 1
fi

cd /home/ubuntu/msms
ls -lh
echo ""

# 4. 가상환경 생성
echo "4️⃣  Python 가상환경 생성 중..."
python3.12 -m venv venv
source venv/bin/activate
echo "✅ 가상환경 생성 완료"
echo ""

# 5. 필수 패키지 설치
echo "5️⃣  Python 패키지 설치 중..."
pip install --upgrade pip
pip install -r requirements_lightsail.txt
echo "✅ Python 패키지 설치 완료"
pip list
echo ""

# 6. 방화벽 설정 (포트 8501 열기)
echo "6️⃣  방화벽 설정 중 (포트 8501)..."
sudo ufw allow 8501/tcp
sudo ufw allow 22/tcp
sudo ufw --force enable
sudo ufw status
echo "✅ 방화벽 설정 완료"
echo ""

# 7. Systemd 서비스 생성
echo "7️⃣  Systemd 서비스 생성 중..."
sudo tee /etc/systemd/system/msms.service > /dev/null <<EOF
[Unit]
Description=MSMS Streamlit Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/msms
Environment="PATH=/home/ubuntu/msms/venv/bin"
ExecStart=/home/ubuntu/msms/venv/bin/streamlit run app_sqlite_v2.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
echo "✅ Systemd 서비스 파일 생성 완료"
echo ""

# 8. 서비스 활성화 및 시작
echo "8️⃣  서비스 활성화 중..."
sudo systemctl daemon-reload
sudo systemctl enable msms.service
sudo systemctl start msms.service

# 서비스 상태 확인
sleep 3
sudo systemctl status msms.service --no-pager
echo ""

# 데이터베이스 검증
echo "9️⃣  데이터베이스 검증 중..."
if command -v sqlite3 &> /dev/null; then
    echo "프로젝트 수: $(sqlite3 /home/ubuntu/msms/msms.db "SELECT COUNT(*) FROM projects;")"
    echo "매입 수: $(sqlite3 /home/ubuntu/msms/msms.db "SELECT COUNT(*) FROM purchases;")"
    echo "매출처 수: $(sqlite3 /home/ubuntu/msms/msms.db "SELECT COUNT(*) FROM vendors;")"
else
    echo "sqlite3 설치 중..."
    sudo apt-get install -y sqlite3
    echo "프로젝트 수: $(sqlite3 /home/ubuntu/msms/msms.db "SELECT COUNT(*) FROM projects;")"
    echo "매입 수: $(sqlite3 /home/ubuntu/msms/msms.db "SELECT COUNT(*) FROM purchases;")"
    echo "매출처 수: $(sqlite3 /home/ubuntu/msms/msms.db "SELECT COUNT(*) FROM vendors;")"
fi
echo ""

echo "================================"
echo "🎉 배포 완료!"
echo "================================"
echo ""
echo "📊 접속 URL: http://43.203.181.195:8501"
echo ""
echo "🔧 서비스 관리 명령어:"
echo "  - 시작:      sudo systemctl start msms"
echo "  - 중지:      sudo systemctl stop msms"
echo "  - 재시작:    sudo systemctl restart msms"
echo "  - 상태확인:  sudo systemctl status msms"
echo "  - 로그확인:  sudo journalctl -u msms -f"
echo ""
echo "✅ 웹 브라우저에서 http://43.203.181.195:8501 접속하세요!"
echo ""
