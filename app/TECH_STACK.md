# 📦 Tech Stack — DevSecOps Pipeline Project

ملخص شامل لكل التقنيات والأدوات المستخدمة في المشروع.

---

## 1. Backend (الواجهة الخلفية)

| التقنية | الاستخدام | الدور |
|---------|-----------|-------|
| **Python 3.11** | لغة البرمجة الأساسية | لغة التطوير الرئيسية للتطبيق والسكريبتات |
| **FastAPI 0.141.1** | Framework ويب | بناء الـ API endpoints: `/health` و `/login` |
| **Uvicorn 0.52.3** | ASGI Server | تشغيل وتقديم تطبيق FastAPI |
| **PyJWT 2.13.0** | JWT Tokens | إنشاء وتوقيع توكنات المصادقة بعد تسجيل الدخول |
| **Passlib 1.7.4** | Password Hashing | تشفير كلمات المرور باستخدام `pbkdf2_sha256` |
| **Pydantic** | Data Validation | التحقق من بيانات الطلبات الواردة (اعتماد ضمني من FastAPI) |

---

## 2. Endpoints

| الطريقة | المسار | الوظيفة |
|---------|--------|---------|
| `GET` | `/health` | فحص حالة التطبيق — يرجع `{"status": "ok"}` |
| `POST` | `/login` | تسجيل الدخول وإرجاع JWT موقّع |

---

## 3. Containerization (الحاوية)

| التقنية | الاستخدام |
|---------|-----------|
| **Docker** | بناء وتغليف التطبيق في صورة (Image) |
| **python:3.11-slim** | صورة أساسية خفيفة الوزن (Base Image) لتقليل حجم وسطح الهجوم |
| **Non-root User** | تشغيل التطبيق بمستخدم غير صلاحيات النظام `appuser` |

---

## 4. CI/CD — GitHub Actions

| التقنية | الاستخدام |
|---------|-----------|
| **GitHub Actions** | منصة الـ CI/CD المتكاملة مع GitHub |
| **Ubuntu Latest Runner** | بيئة تشغيل الـ workflow |
| **actions/checkout@v4** | سحب الكود من الـ repository |
| **actions/setup-python@v5** | تجهيز بيئة Python 3.11 |

---

## 5. Security Tools (أدوات الحماية)

| الأداة | النوع | وظيفتها | فشل عند |
|--------|-------|---------|---------|
| **Bandit** | SAST | فحص كود Python بحثًا عن ثغرات أمنية | وجود مشاكل **HIGH** |
| **pip-audit** | SCA | فحص المكتبات بحثًا عن CVEs معروفة | أي CVE معروفة |
| **Safety** | SCA | بديل لـ pip-audit (يتطلب API key) | أي CVE معروفة |
| **TruffleHog** | Secret Scanning | فحص الكود والتاريخ بحثًا عن أسرار ومفاتيح API | أي سر أو مفتاح مكتشف |
| **Trivy** | Container Scanning | فحص صورة Docker بحثًا عن ثغرات OS والمكتبات | ثغرات **CRITICAL/HIGH** |

---

## 6. الـ Pipeline — الـ 5 Gates

| Gate | الأداة | الاختصار |
|------|--------|----------|
| Gate 1 | Checkout & Setup Python 3.11 | CI Setup |
| Gate 2 | Bandit | SAST |
| Gate 3 | pip-audit / Safety | SCA |
| Gate 4 | TruffleHog | Secret Scanning |
| Gate 5 | Docker Build + Trivy | Container Security |

> ✅ النتيجة النهائية: `Security Verification Passed - Ready for Deployment`

---

## 7. بنية الملفات

```plaintext
devsecops-pipeline/
├── .github/workflows/devsecops-pipeline.yml
├── app/{__init__.py, main.py}
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 8. لغة التوثيق والتنسيق

| التقنية | الاستخدام |
|---------|-----------|
| **Markdown** | كتابة التوثيق (README.md) |
| **Git / GitHub** | إدارة الإصدارات ورفع الكود |

---

## ملاحظة أمنية

- `JWT_SECRET_KEY` يتم قراءته من Environment Variables وليس مكتوبًا في الكود.
- كلمة مرور الـ demo (`admin`/`password`) محفوظة كـ hash وليس نصًا صريحًا.
