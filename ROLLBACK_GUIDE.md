# 🔄 MSMS 롤백 가이드

## 📌 백업 버전

### msms-ver1 (현재 안정 버전)
- **날짜**: 2026-02-05
- **커밋**: cb31216
- **설명**: 초기 배포 완료 버전
- **기능**:
  - ✅ 프로젝트 목록 표시 (행 클릭 선택)
  - ✅ 컬럼 순서: ID → 영업담당자 → 매출처 → 고객사 → 프로젝트명 → 상태
  - ✅ "클라이언트" → "매출처"로 변경
  - ✅ 필터 및 검색 기능
  - ✅ 프로젝트 573개, 매입 1,281개

---

## 🚨 롤백이 필요한 경우

- 새로운 개발 후 오류 발생
- 데이터베이스 문제
- 서비스가 시작되지 않음
- 화면이 정상적으로 표시되지 않음

---

## 🔧 롤백 방법

### 방법 1: Lightsail SSH에서 롤백 (추천)

#### 1️⃣ msms-ver1으로 롤백

```bash
# 1. 서비스 중지
sudo systemctl stop msms

# 2. 현재 파일 백업
cd /home/ubuntu/msms
mv app_sqlite_v2.py app_sqlite_v2.py.backup_$(date +%Y%m%d_%H%M%S)
mv msms.db msms.db.backup_$(date +%Y%m%d_%H%M%S)

# 3. GitHub에서 msms-ver1 버전 받기
cd /home/ubuntu
rm -rf msms-deploy
git clone -b msms-ver1 https://github.com/thelab-bobkim/msms-deploy.git

# 4. 파일 복원
cp /home/ubuntu/msms-deploy/app_sqlite_v2.py /home/ubuntu/msms/
cp /home/ubuntu/msms-deploy/msms.db /home/ubuntu/msms/
cp /home/ubuntu/msms-deploy/requirements_lightsail.txt /home/ubuntu/msms/

# 5. 서비스 재시작
sudo systemctl start msms
sleep 5

# 6. 상태 확인
sudo systemctl status msms --no-pager

echo ""
echo "✅ msms-ver1으로 롤백 완료!"
echo "🌐 http://43.203.181.195:8501"
```

---

### 방법 2: 특정 커밋으로 롤백

```bash
# 1. 서비스 중지
sudo systemctl stop msms

# 2. 특정 커밋 체크아웃
cd /home/ubuntu
rm -rf msms-deploy
git clone https://github.com/thelab-bobkim/msms-deploy.git
cd msms-deploy
git checkout cb31216  # msms-ver1 커밋

# 3. 파일 복원
cp app_sqlite_v2.py /home/ubuntu/msms/
cp msms.db /home/ubuntu/msms/
cp requirements_lightsail.txt /home/ubuntu/msms/

# 4. 서비스 재시작
cd /home/ubuntu/msms
sudo systemctl start msms
sudo systemctl status msms --no-pager
```

---

### 방법 3: 최신 버전으로 업데이트

```bash
# 1. 서비스 중지
sudo systemctl stop msms

# 2. 최신 main 브랜치 받기
cd /home/ubuntu
rm -rf msms-deploy
git clone https://github.com/thelab-bobkim/msms-deploy.git

# 3. 파일 업데이트
cp /home/ubuntu/msms-deploy/app_sqlite_v2.py /home/ubuntu/msms/
cp /home/ubuntu/msms-deploy/msms.db /home/ubuntu/msms/

# 4. 서비스 재시작
sudo systemctl start msms
sudo systemctl status msms --no-pager
```

---

## 📋 롤백 전 체크리스트

- [ ] 현재 버전 백업 완료
- [ ] 데이터베이스 백업 완료
- [ ] 롤백할 버전 확인 (msms-ver1)
- [ ] 서비스 중지 확인

---

## 🔍 버전 확인 방법

### GitHub에서 확인
```bash
# 사용 가능한 태그 목록
git ls-remote --tags https://github.com/thelab-bobkim/msms-deploy.git

# 커밋 히스토리
git log --oneline
```

### 현재 실행 중인 버전 확인
```bash
# 파일 수정 시간 확인
ls -lh /home/ubuntu/msms/app_sqlite_v2.py

# 파일 크기 확인
du -h /home/ubuntu/msms/app_sqlite_v2.py
```

---

## 🛠️ 문제 해결

### 서비스가 시작되지 않는 경우
```bash
# 로그 확인
sudo journalctl -u msms -n 50 --no-pager

# 프로세스 정리
sudo pkill -9 -f streamlit
sudo fuser -k 8501/tcp

# 서비스 리셋
sudo systemctl reset-failed msms
sudo systemctl start msms
```

### 데이터베이스 문제
```bash
# 데이터베이스 검증
sqlite3 /home/ubuntu/msms/msms.db "SELECT COUNT(*) FROM projects;"
# 예상: 573

# 데이터베이스 백업에서 복원
cp /home/ubuntu/msms/msms.db.backup_YYYYMMDD_HHMMSS /home/ubuntu/msms/msms.db
```

---

## 📊 버전 비교

### msms-ver1 (안정 버전)
- **커밋**: cb31216
- **날짜**: 2026-02-05
- **특징**: 
  - 초기 배포 완료
  - 프로젝트 클릭 선택 가능
  - 컬럼 순서 최적화
  - 데이터: 573개 프로젝트

---

## 🔐 백업 위치

### GitHub 백업
- **저장소**: https://github.com/thelab-bobkim/msms-deploy
- **태그**: msms-ver1
- **브랜치**: main

### 로컬 백업 (Lightsail 서버)
- **경로**: `/home/ubuntu/msms/`
- **백업 파일**: `app_sqlite_v2.py.backup_*`, `msms.db.backup_*`

---

## 📞 지원

문제가 발생하면 다음을 확인하세요:
1. 서비스 로그: `sudo journalctl -u msms -f`
2. 프로세스 상태: `ps aux | grep streamlit`
3. 포트 상태: `sudo lsof -i :8501`

---

**마지막 업데이트**: 2026-02-05  
**안정 버전**: msms-ver1 (cb31216)  
**접속 URL**: http://43.203.181.195:8501
