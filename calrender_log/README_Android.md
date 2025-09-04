# 생산 내역 기록 안드로이드 앱

스마트폰에서 사용할 수 있는 생산 내역 기록 앱입니다.

## 📱 주요 기능

### 1. 생산 기록 입력
- 날짜, 모델, 수량 입력
- 자동 금액 계산
- 입력 검증 및 오류 처리

### 2. 달력 조회
- 월별 달력에서 생산 기록 확인
- 기록이 있는 날짜 시각적 표시
- 특정 날짜의 상세 기록 팝업

### 3. 통계 기능
- 월별 생산량 통계
- 모델별 통계 (수량, 금액, 평균단가)
- 일별 생산량 요약

### 4. 모델 관리
- 새 모델 추가/수정
- 모델별 단가 설정
- 등록된 모델 목록 조회

### 5. 데이터 내보내기
- CSV 파일로 데이터 내보내기
- 날짜 범위 선택 가능
- 한글 인코딩 지원

## 🛠️ 기술 스택

- **언어**: Kotlin
- **UI**: Material Design 3
- **데이터베이스**: Room (SQLite)
- **아키텍처**: MVVM
- **비동기 처리**: Kotlin Coroutines

## 📦 설치 및 실행

### 1. Android Studio 설치
- [Android Studio](https://developer.android.com/studio) 다운로드 및 설치
- Android SDK 및 에뮬레이터 설정

### 2. 프로젝트 열기
```bash
# Android Studio에서 프로젝트 열기
File → Open → android_project 폴더 선택
```

### 3. 빌드 및 실행
```bash
# Gradle 빌드
./gradlew build

# APK 생성
./gradlew assembleDebug

# 에뮬레이터에서 실행
./gradlew installDebug
```

## 📱 APK 설치

### 개발자 모드 활성화
1. 설정 → 휴대전화 정보 → 빌드 번호를 7번 연속 터치
2. 개발자 옵션 → USB 디버깅 활성화

### APK 설치
```bash
# USB로 연결된 기기에 설치
adb install app-debug.apk

# 또는 APK 파일을 직접 다운로드하여 설치
```

## 🗄️ 데이터베이스 구조

### ProductionRecord (생산 기록)
- id: 기본키
- date: 날짜 (YYYY-MM-DD)
- model: 모델명
- quantity: 수량
- unitPrice: 단가
- amount: 총 금액
- createdAt: 생성 시간

### ModelInfo (모델 정보)
- modelName: 모델명 (기본키)
- unitPrice: 단가
- description: 설명

## 🎨 UI/UX 특징

- **Material Design 3** 적용
- **반응형 레이아웃** (다양한 화면 크기 지원)
- **직관적인 네비게이션**
- **한국어 완전 지원**
- **터치 친화적 인터페이스**

## 📊 데이터 관리

- **로컬 SQLite 데이터베이스** 사용
- **데이터 백업**: CSV 내보내기 기능
- **데이터 무결성**: 입력 검증 및 제약 조건
- **성능 최적화**: Room 데이터베이스 사용

## 🔧 개발 환경

- **최소 SDK**: API 21 (Android 5.0)
- **타겟 SDK**: API 34 (Android 14)
- **Kotlin**: 1.9.10
- **Gradle**: 8.1.4

## 📝 라이선스

이 프로젝트는 개인/상업적 용도로 자유롭게 사용할 수 있습니다.

## 🤝 기여

버그 리포트나 기능 제안은 언제든 환영합니다!
