"""
Django settings for ESP_site project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv # python-dotenv 사용을 위해 추가

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# .env 파일에서 환경 변수 로드 (로컬 개발 시)
load_dotenv(BASE_DIR / '.env') # 프로젝트 루트에 .env 파일이 있다고 가정

# SECURITY WARNING: keep the secret key used in production secret!
# 환경 변수에서 SECRET_KEY를 가져오거나, 없으면 기본값(개발용) 사용
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# 환경 변수 DJANGO_DEBUG 값이 'False'가 아니면 True (기본값 True)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [] # 먼저 빈 리스트로 초기화
PYTHONANYWHERE_USERNAME_FROM_ENV = os.environ.get('PYTHONANYWHERE_USERNAME') # 변수 이름을 다르게 하여 혼동 방지

# PYTHONANYWHERE_USERNAME_FROM_ENV 값이 있고, 그 값이 임시 값이 아닐 때만 추가
if PYTHONANYWHERE_USERNAME_FROM_ENV and PYTHONANYWHERE_USERNAME_FROM_ENV != '아직_몰라도_됩니다_나중에_채울게요':
    ALLOWED_HOSTS.append(f'{PYTHONANYWHERE_USERNAME_FROM_ENV}.pythonanywhere.com')

if DEBUG: # DEBUG가 True일 때만 로컬 호스트 추가
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])

# CSRF 보호를 위해 신뢰할 수 있는 출처 설정
# HTTPS를 사용하므로 'https://'를 포함해야 합니다.
CSRF_TRUSTED_ORIGINS = ['https://icuu.pythonanywhere.com']

# 만약 www 서브도메인도 사용한다면 (지금은 해당 없음)
# CSRF_TRUSTED_ORIGINS = ['https://icuu.pythonanywhere.com', 'https://www.icuu.pythonanywhere.com']

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic", # Whitenoise, 개발 서버에서도 staticfiles 앱보다 먼저
    "django.contrib.staticfiles",
    'rankings',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # Whitenoise 미들웨어, 가능한 한 위쪽에 위치
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ESP_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ESP_site.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# PythonAnywhere에서 PostgreSQL 등을 사용한다면, 해당 정보도 환경 변수로 관리하는 것이 좋습니다.
# MVP에서는 SQLite를 그대로 사용한다고 가정합니다.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / 'static', # Pathlib 방식 사용
]
STATIC_ROOT = BASE_DIR / 'staticfiles' # collectstatic이 파일을 모을 디렉터리

# Whitenoise가 압축된 정적 파일을 제공하도록 설정 (선택 사항이지만 권장)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media files (User-uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'