# Laboratorio Semana 3 - Desarrollo de Aplicaciones Empresariales (D.A.E)

## 1. Datos del alumno

| Campo          | Valor                          |
|----------------|--------------------------------|
| Alumno         | Jeff Amaro                     |
| Título         | Laboratorio Semana 3 |
| Repositorio    | https://github.com/Jeff-amaro/Jeff-amaro-Semana3-D.A.E |
| Herramientas   | Python 3.12, Django 6.1, SQLite, Git, HTML/CSS |

## 2. Metodologia de equipo (simulacion de 4 agentes)

| Agente                          | Rol en este laboratorio                                                                    |
|---------------------------------|-------------------------------------------------------------------------------------------|
| Arquitecto de Software          | Definió los modelos `Exam`, `Question`, `Choice`, la justificación de campos y el proyecto `config` dentro de `src/`. |
| Desarrollador Lead              | Implementó formularios, formset, vistas, rutas y plantillas, además del campo `score`.     |
| QA / Code Reviewer              | Escribió 11 casos de prueba (modelos, formularios, formset de opciones y vistas) y revisó la migración `0001_initial.py` antes de aplicarla. |
| Git & DevOps Manager            | Creó el entorno virtual, instaló dependencias, aplicó migraciones y ejecutó `git init`, `commit` y `push` al repositorio del equipo. |

## 3. Desarrollo paso a paso

### Paso 1. Estructura del proyecto

Se creó el entorno virtual `venv/`, el paquete fuente `src/config` (proyecto) y la aplicación `quiz`, además de `requirements.txt` y `.gitignore`. La app `quiz` se declaró en `INSTALLED_APPS` y el `SECRET_KEY` se lee desde el entorno para no dejar credenciales escritas a mano.

#### Código (extracto de `config/settings.py`)

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-only-key-change-me')

INSTALLED_APPS = [
    'django.contrib.admin',
    # ...
    'quiz',
]
```

#### Captura del resultado

```
System check identified no issues (0 silenced).
CHECK OK
```

#### Estructura del proyecto en el editor

```
quiz_lab/
├── .gitignore
├── requirements.txt
├── venv/
└── src/
    ├── manage.py
    ├── db.sqlite3
    ├── config/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── quiz/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── forms.py
        ├── models.py
        ├── tests.py
        ├── urls.py
        ├── views.py
        ├── migrations/
        │   ├── __init__.py
        │   ├── 0001_initial.py
        │   └── 0002_question_score.py
        └── templates/quiz/
            ├── base.html
            ├── exam_list.html
            ├── exam_detail.html
            └── question_create.html
```

### Pasos 2-4. Modelos con `str`, orden y nombres singular/plural

#### Código (`src/quiz/models.py`)

```python
from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "exam"
        verbose_name_plural = "exams"

    def __str__(self):
        return self.title


class Question(models.Model):
    statement = models.TextField()
    score = models.IntegerField(default=1)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")

    class Meta:
        ordering = ["id"]
        verbose_name = "question"
        verbose_name_plural = "questions"

    def __str__(self):
        return self.statement[:50]


class Choice(models.Model):
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")

    class Meta:
        ordering = ["id"]
        verbose_name = "choice"
        verbose_name_plural = "choices"

    def __str__(self):
        return self.text
```

#### Explicación del resultado
- `Exam.title` ordena alfabéticamente; `Question` y `Choice` usan `ordering = ["id"]` para respetar el orden de ingreso.
- `related_name` (snake_case, plural) permite accesos como `exam.questions.all()` y `question.choices.all()`.
- Los `str` retornan `title`, los primeros 50 caracteres del enunciado y el texto de la opción, respectivamente, facilitando la lectura en el admin.

### Paso 5. Migraciones, revisión y verificación de tablas

#### Comandos

```
python manage.py makemigrations quiz
python manage.py migrate
```

#### Revisión (QA) de `quiz/migrations/0001_initial.py`

```python
operations = [
    migrations.CreateModel(
        name='Exam',
        fields=[
            ('id', models.BigAutoField(...)),
            ('title', models.CharField(max_length=200)),
            ('description', models.TextField(blank=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
        ],
        options={'verbose_name': 'exam', 'verbose_name_plural': 'exams', 'ordering': ['title']},
    ),
    # Creación de 'Question' y 'Choice' con sus ForeignKey y related_name...
]
```

#### Captura del resultado (tablas reales en `db.sqlite3`)

```
Tablas quiz: ['quiz_exam', 'quiz_question', 'quiz_choice']
quiz_exam     -> ['id', 'title', 'description', 'created_at']
quiz_question -> ['id', 'statement', 'exam_id']
quiz_choice   -> ['id', 'text', 'is_correct', 'question_id']
```

### Paso 6. Formularios y formset de opciones

#### Código (`src/quiz/forms.py`)

```python
class ChoiceFormSet = inlineformset_factory(
    Question, Choice, form=ChoiceForm, formset=BaseChoiceFormSet,
    extra=3, min_num=2, max_num=6, validate_min=True, can_delete=False,
)
```

`BaseChoiceFormSet.clean()` valida que **exactamente una** opción quede marcada como correcta.

### Paso 7. Vistas

- `exam_list`: lista los exámenes.
- `exam_detail`: muestra el examen con `prefetch_related("questions__choices")`.
- `question_create`: guarda la pregunta y su formset de opciones; si se marcan dos correctas devuelve el error del formset al formulario.

### Paso 8. Rutas y plantillas

```
/                 exam_list
/exam/<pk>/       exam_detail
/question/new/    question_create
```

Plantillas creadas: `base.html`, `exam_list.html`, `exam_detail.html` y `question_create.html`.

### Paso 9. Admin, superusuario y datos de prueba

Se registraron los tres modelos con inlines (`ExamAdmin` con `QuestionInline` y `QuestionAdmin` con `ChoiceInline`), se creó el superusuario y se dieron de alta **1 examen con 2 preguntas y 4 opciones cada una**.

#### Captura del resultado (carga de datos)

```
1 | What command creates the migration files? | choices: 4 | correct: python manage.py makemigrations
2 | Which field auto-stores the creation date? | choices: 4 | correct: DateTimeField(auto_now_add=True)
Total exams: 1 | Total questions: 2 | Total choices: 8
```

### Paso 10. Campo nuevo en `Question` (puntaje)

Se agregó `score = models.IntegerField(default=1)`.

#### Captura: se generó `quiz/migrations/0002_question_score.py`

```python
operations = [
    migrations.AddField(
        model_name='question',
        name='score',
        field=models.IntegerField(default=1),
    ),
]
```

La columna quedó así en la base de datos: `quiz_question -> ['id', 'statement', 'exam_id', 'score']`.

## 4. Justificación de tipos de campo (Paso 11)

### Exam
| Atributo     | Campo elegido                | Justificación                                                                 |
|--------------|------------------------------|-------------------------------------------------------------------------------|
| title        | `CharField(max_length=200)`  | Texto corto y acabado; limitar la longitud evita títulos desmedidos y da un tope lógico en el form. |
| description  | `TextField(blank=True)`      | Descripción libre de extensión variable; no es obligatoria, por eso `blank=True`. |
| created_at   | `DateTimeField(auto_now_add=True)` | Fecha/hora se fija automáticamente al insertar y no vuelve a cambiar; evita lógica manual. |

### Question
| Atributo   | Campo elegido                 | Justificación                                                                             |
|------------|-------------------------------|-------------------------------------------------------------------------------------------|
| statement  | `TextField()`                 | El enunciado de una pregunta puede tener varias líneas e incluir fórmulas o ejemplos.     |
| score      | `IntegerField(default=1)`     | Puntaje numérico entero; el default 1 da valor por defecto a preguntas ya existentes.     |
| exam       | `ForeignKey(CASCADE, related_name="questions")` | Cada pregunta pertenece a un examen; CASCADE borra las preguntas si se elimina el examen y `related_name` permite acceder desde el padre. |

### Choice
| Atributo   | Campo elegido                | Justificación                                                                  |
|------------|------------------------------|--------------------------------------------------------------------------------|
| text       | `CharField(max_length=200)`  | Texto de opción breve; 200 caracteres es suficiente para una respuesta típica. |
| is_correct | `BooleanField(default=False)` | Indicador binario de respuesta correcta; el default False evita que una opción quede marcada por error. |
| question   | `ForeignKey(CASCADE, related_name="choices")` | Toda opción pertenece a una pregunta; CASCADE preserva la integridad referencial y `related_name` facilita `question.choices.all()`. |

## 5. Casos de prueba (QA)

Se ejecutaron **11 pruebas** con `python manage.py test quiz`:

```
test_exactly_one_correct_marks_valid ... ok
test_two_correct_marks_is_rejected   ... ok
test_exam_form_valid                 ... ok
test_question_form_valid             ... ok
test_choice_str                      ... ok
test_exam_default_order              ... ok
test_exam_str                        ... ok
test_question_str                    ... ok
test_relations                       ... ok
test_exam_detail                     ... ok
test_exam_list                       ... ok
----------------------------------------------------------------------
Ran 11 tests in 0.084s  OK
```

Los casos clave son los del formset: registrar 1 opción correcta es válido (redirige tras guardar) y marcar 2 correctas se rechaza mostrando `Exactly one choice must be marked as correct.`

## 6. Captura de renderizado real (evidencia de funcionamiento)

- `GET /` devuelve el listado con el enlace "Django Fundamentals (2 questions)".
- `GET /exam/1/` muestra ambas preguntas con sus 4 opciones, la correcta en verde con marca ✔ y el puntaje (`Score: 1 point`).