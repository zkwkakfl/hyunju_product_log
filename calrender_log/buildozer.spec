[app]

# (str) 제목
title = 생산내역기록

# (str) 패키지명
package.name = productionlogger

# (str) 도메인
package.domain = com.productionlogger

# (str) 소스 코드 디렉토리
source.dir = .

# (list) 소스 파일들
source.include_exts = py,png,jpg,kv,atlas,db

# (str) 메인 파일
source.main = main.py

# (str) 앱 버전
version = 1.0

# (list) 필요한 권한들
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) 안드로이드 API 레벨
android.api = 33

# (str) 최소 안드로이드 API 레벨
android.minapi = 21

# (str) 안드로이드 NDK 버전
android.ndk = 25b

# (list) Python 모듈들
requirements = python3,kivy,sqlite3,json,datetime,calendar

# (str) 아이콘 파일 (선택사항)
# icon.filename = %(source.dir)s/icon.png

# (str) 배경색
# background_color = 1,1,1,1

# (str) 방향 (portrait, landscape, sensor)
orientation = portrait

# (bool) 전체화면 모드
fullscreen = 0

# (str) 로그 레벨
log_level = 2

# GitHub Actions 환경을 위한 추가 설정
# (str) 빌드 디렉토리
build_dir = .buildozer

# (str) 빌드 타입 (debug, release)
build_type = debug

# (bool) 빌드 캐시 사용
buildozer.cache = True

# (str) Java 버전
android.gradle_dependencies = 

# (str) ProGuard 설정 (릴리즈 빌드시)
# android.proguard = 

# (str) 앱 서명 설정 (릴리즈 빌드시)
# android.keystore = 
# android.keyalias = 
# android.keypass = 
# android.keystorepass = 


