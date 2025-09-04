# GitHub Secrets 설정 가이드 (고급 기능)

## 개요
GitHub Secrets는 민감한 정보를 안전하게 저장하고 GitHub Actions에서 사용할 수 있게 해주는 기능입니다. 
현재 프로젝트에서는 기본적인 빌드만 수행하므로 필수는 아니지만, 향후 앱 서명이나 배포를 위해 알아두면 유용합니다.

## 1. GitHub Secrets 설정 방법

### 1.1 Secrets 페이지 접근
1. GitHub 저장소 페이지에서 "Settings" 탭 클릭
2. 왼쪽 메뉴에서 "Secrets and variables" → "Actions" 클릭
3. "New repository secret" 버튼 클릭

### 1.2 일반적으로 사용되는 Secrets

#### Android 앱 서명용 (릴리즈 빌드시)
```
ANDROID_KEYSTORE_BASE64: Base64로 인코딩된 keystore 파일
ANDROID_KEYSTORE_PASSWORD: keystore 비밀번호
ANDROID_KEY_ALIAS: 키 별칭
ANDROID_KEY_PASSWORD: 키 비밀번호
```

#### Google Play Console 배포용 (선택사항)
```
GOOGLE_PLAY_SERVICE_ACCOUNT: JSON 서비스 계정 키
GOOGLE_PLAY_TRACK: 배포 트랙 (internal, alpha, beta, production)
```

## 2. 워크플로우에서 Secrets 사용

### 2.1 서명된 APK 빌드 예시
```yaml
- name: Build signed APK
  run: |
    # keystore 파일 복원
    echo "${{ secrets.ANDROID_KEYSTORE_BASE64 }}" | base64 -d > keystore.jks
    
    # buildozer.spec에 서명 정보 추가
    echo "android.keystore = keystore.jks" >> buildozer.spec
    echo "android.keyalias = ${{ secrets.ANDROID_KEY_ALIAS }}" >> buildozer.spec
    echo "android.keypass = ${{ secrets.ANDROID_KEY_PASSWORD }}" >> buildozer.spec
    echo "android.keystorepass = ${{ secrets.ANDROID_KEYSTORE_PASSWORD }}" >> buildozer.spec
    
    # 서명된 APK 빌드
    buildozer android release
```

## 3. 현재 프로젝트에서의 활용

### 3.1 현재 상태
- 현재는 디버그 APK만 빌드하므로 Secrets 불필요
- 기본 워크플로우로 충분히 작동

### 3.2 향후 확장 가능성
- **앱 서명**: Google Play Store 배포를 위한 서명된 APK
- **자동 배포**: Firebase App Distribution 등으로 자동 배포
- **알림**: 빌드 완료 시 Slack, Discord 등으로 알림

## 4. 보안 주의사항

### 4.1 Secrets 보안
- Secrets는 저장소 설정에서만 확인 가능
- 로그에 Secrets 값이 노출되지 않음
- 팀원과 공유하려면 저장소 권한 필요

### 4.2 권장사항
- 불필요한 Secrets는 삭제
- 정기적으로 Secrets 값 변경
- 최소 권한 원칙 적용

## 5. 현재 프로젝트에서는 생략 가능

현재 생산 내역 기록 앱의 경우:
- 디버그 APK만 필요
- 내부 사용 목적
- 복잡한 배포 과정 불필요

따라서 GitHub Secrets 설정 없이도 기본 워크플로우로 충분히 사용 가능합니다.
