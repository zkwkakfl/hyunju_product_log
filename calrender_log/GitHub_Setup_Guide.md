# GitHub Actions를 사용한 Android APK 자동 빌드 설정 가이드

## 1. GitHub 저장소 생성 및 설정

### 1.1 새 저장소 생성
1. GitHub.com에 로그인
2. 우측 상단의 "+" 버튼 클릭 → "New repository" 선택
3. 저장소 정보 입력:
   - **Repository name**: `calrender_log` (또는 원하는 이름)
   - **Description**: "생산 내역 기록 Android 앱"
   - **Visibility**: Public 또는 Private 선택
   - **Initialize this repository with**: 체크하지 않음 (로컬 프로젝트가 이미 있으므로)

### 1.2 로컬 프로젝트를 GitHub에 연결
```bash
# 현재 프로젝트 디렉토리에서 실행
cd C:\Users\leesd86\Projects\calrender_log

# Git 초기화 (아직 안했다면)
git init

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: 생산 내역 기록 앱"

# GitHub 저장소를 원격 저장소로 추가
git remote add origin https://github.com/[사용자명]/calrender_log.git

# main 브랜치로 푸시
git branch -M main
git push -u origin main
```

## 2. GitHub Actions 활성화

### 2.1 Actions 탭 확인
1. GitHub 저장소 페이지에서 "Actions" 탭 클릭
2. "I understand my workflows, go ahead and enable them" 클릭
3. 워크플로우가 자동으로 활성화됨

### 2.2 워크플로우 실행 확인
1. 코드를 푸시하면 자동으로 빌드가 시작됨
2. Actions 탭에서 빌드 진행 상황 확인 가능
3. 빌드 완료 후 "Artifacts" 섹션에서 APK 다운로드 가능

## 3. 빌드 트리거 설정

### 3.1 자동 빌드 조건
- **Push to main**: main 브랜치에 코드가 푸시될 때마다 자동 빌드
- **Pull Request**: main 브랜치로 PR이 생성될 때 빌드
- **Manual**: 수동으로 빌드 실행 가능

### 3.2 빌드 실행 방법
1. **자동 실행**: 코드를 main 브랜치에 푸시
2. **수동 실행**: 
   - Actions 탭 → "Android APK Build" 워크플로우 선택
   - "Run workflow" 버튼 클릭

## 4. 빌드 결과 확인

### 4.1 빌드 로그 확인
1. Actions 탭에서 실행된 워크플로우 클릭
2. "build" 작업 클릭하여 상세 로그 확인
3. 빌드 과정에서 오류 발생 시 로그에서 원인 파악

### 4.2 APK 다운로드
1. 빌드 완료 후 "Artifacts" 섹션 확인
2. "production-logger-apk" 클릭하여 APK 파일 다운로드
3. 다운로드한 APK를 Android 기기에 설치

## 5. 주의사항

### 5.1 빌드 시간
- 첫 빌드: 약 10-15분 (의존성 다운로드 포함)
- 이후 빌드: 약 5-8분

### 5.2 저장소 크기 제한
- GitHub의 무료 계정은 500MB 제한
- 큰 파일들은 .gitignore에 추가 권장

### 5.3 빌드 실패 시
- 로그를 자세히 확인하여 오류 원인 파악
- buildozer.spec 파일 설정 확인
- Python 의존성 충돌 확인
