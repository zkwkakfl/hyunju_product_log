# GitHub Actions Android 빌드 문제 해결 가이드

## 1. 빌드 실패 시 확인사항

### 1.1 빌드 로그 확인
1. GitHub 저장소 → Actions 탭
2. 실패한 워크플로우 클릭
3. "build" 작업 클릭하여 상세 로그 확인
4. 빨간색 ❌ 표시된 부분부터 위로 스크롤하여 오류 원인 파악

### 1.2 일반적인 오류 유형
- **의존성 설치 실패**: Python 패키지 충돌
- **Android SDK 오류**: SDK 버전 불일치
- **빌드 도구 오류**: Java, Gradle 설정 문제
- **메모리 부족**: 빌드 과정에서 메모리 초과

## 2. 자주 발생하는 문제와 해결방법

### 2.1 Python 의존성 문제
```
오류: ModuleNotFoundError: No module named 'kivy'
해결: requirements.txt에 모든 필요한 패키지 추가
```

**해결방법:**
```bash
# requirements.txt 파일 확인
cat requirements.txt

# 누락된 패키지 추가
echo "kivy>=2.1.0" >> requirements.txt
echo "buildozer>=1.5.0" >> requirements.txt
```

### 2.2 Android SDK 버전 문제
```
오류: Android SDK not found
해결: SDK 경로 및 버전 확인
```

**해결방법:**
1. 워크플로우 파일에서 Android API 레벨 확인
2. buildozer.spec의 android.api 값과 일치하는지 확인
3. 필요시 SDK 버전 업데이트

### 2.3 메모리 부족 문제
```
오류: Out of memory during build
해결: 빌드 과정 최적화
```

**해결방법:**
1. 워크플로우에 메모리 제한 설정 추가
2. 불필요한 파일 제외 (.gitignore 활용)
3. 빌드 캐시 활용

### 2.4 Java 버전 문제
```
오류: Unsupported Java version
해결: Java 11 사용 확인
```

**해결방법:**
워크플로우 파일에서 Java 11 설치 확인:
```yaml
- name: Install system dependencies
  run: |
    sudo apt-get install -y openjdk-11-jdk
```

## 3. 빌드 최적화 방법

### 3.1 .gitignore 파일 생성
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Buildozer
.buildozer/
bin/
*.apk
*.aab

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### 3.2 워크플로우 최적화
```yaml
# 빌드 캐시 활용
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

# 불필요한 단계 제거
- name: Clean up
  run: |
    # 빌드 후 불필요한 파일 정리
    rm -rf .buildozer/android/platform/build-*/build
```

## 4. 디버깅 방법

### 4.1 로컬에서 테스트
```bash
# 로컬에서 buildozer 테스트
pip install buildozer
buildozer android debug

# 오류 발생시 상세 로그 확인
buildozer android debug -v
```

### 4.2 워크플로우 디버깅
```yaml
# 디버그 모드로 실행
- name: Debug build
  run: |
    echo "=== 환경 변수 확인 ==="
    echo "ANDROID_HOME: $ANDROID_HOME"
    echo "PATH: $PATH"
    
    echo "=== Python 버전 확인 ==="
    python3 --version
    
    echo "=== 설치된 패키지 확인 ==="
    pip list
```

## 5. 성공적인 빌드를 위한 체크리스트

### 5.1 빌드 전 확인사항
- [ ] 모든 소스 파일이 저장소에 포함됨
- [ ] requirements.txt에 필요한 패키지 모두 포함
- [ ] buildozer.spec 설정이 올바름
- [ ] .gitignore로 불필요한 파일 제외

### 5.2 빌드 후 확인사항
- [ ] APK 파일이 Artifacts에 업로드됨
- [ ] APK 파일 크기가 합리적 (10-50MB)
- [ ] Android 기기에서 APK 설치 가능

## 6. 추가 도움말

### 6.1 유용한 링크
- [Buildozer 공식 문서](https://buildozer.readthedocs.io/)
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Android 개발자 가이드](https://developer.android.com/)

### 6.2 커뮤니티 지원
- GitHub Issues에 문제 보고
- Stack Overflow에서 관련 질문 검색
- Kivy 공식 포럼 참여
