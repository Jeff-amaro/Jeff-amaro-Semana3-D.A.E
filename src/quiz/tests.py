from django.test import TestCase
from django.urls import reverse

from .forms import ChoiceFormSet, ExamForm, QuestionForm
from .models import Choice, Exam, Question


class ModelTests(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(
            title="Math Basics", description="Arithmetic review"
        )
        self.question = Question.objects.create(
            exam=self.exam, statement="What is 2 + 2?"
        )
        Choice.objects.create(
            question=self.question, text="4", is_correct=True
        )
        Choice.objects.create(
            question=self.question, text="5", is_correct=False
        )

    def test_exam_str(self):
        self.assertEqual(str(self.exam), "Math Basics")

    def test_question_str(self):
        self.assertEqual(str(self.question), "What is 2 + 2?")

    def test_choice_str(self):
        self.assertEqual(str(self.question.choices.first()), "4")

    def test_relations(self):
        self.assertEqual(self.exam.questions.count(), 1)
        self.assertEqual(self.question.choices.count(), 2)

    def test_exam_default_order(self):
        Exam.objects.create(title="Advanced Math")
        exams = list(Exam.objects.all())
        self.assertEqual(exams[0].title, "Advanced Math")
        self.assertEqual(exams[1].title, "Math Basics")


class FormTests(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(title="Science", description="")

    def test_exam_form_valid(self):
        form = ExamForm(
            data={"title": "History", "description": "World history"}
        )
        self.assertTrue(form.is_valid())

    def test_question_form_valid(self):
        form = QuestionForm(
            data={
                "statement": "Capital of France?",
                "exam": self.exam.pk,
                "score": "2",
            }
        )
        self.assertTrue(form.is_valid())


class ChoiceFormSetTests(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(title="Geography", description="")

    def _post(self, choices):
        data = {
            "statement": "Capital of France?",
            "exam": self.exam.pk,
            "score": "1",
        }
        data.update(choices)
        response = self.client.post(
            reverse("quiz:question_create"), data
        )
        return response

    def test_exactly_one_correct_marks_valid(self):
        data = {
            "choices-TOTAL_FORMS": "3",
            "choices-INITIAL_FORMS": "0",
            "choices-MIN_NUM_FORMS": "2",
            "choices-MAX_NUM_FORMS": "6",
            "choices-0-text": "Paris",
            "choices-0-is_correct": "on",
            "choices-1-text": "Rome",
            "choices-1-is_correct": "",
            "choices-2-text": "Madrid",
            "choices-2-is_correct": "",
        }
        response = self._post(data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.get().choices.filter(is_correct=True).count(), 1)

    def test_two_correct_marks_is_rejected(self):
        data = {
            "choices-TOTAL_FORMS": "3",
            "choices-INITIAL_FORMS": "0",
            "choices-MIN_NUM_FORMS": "2",
            "choices-MAX_NUM_FORMS": "6",
            "choices-0-text": "Paris",
            "choices-0-is_correct": "on",
            "choices-1-text": "Rome",
            "choices-1-is_correct": "on",
            "choices-2-text": "Madrid",
            "choices-2-is_correct": "",
        }
        response = self._post(data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Exactly one choice must be marked as correct.")


class ViewTests(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(
            title="Computing", description="Intro"
        )
        self.question = Question.objects.create(
            exam=self.exam, statement="Is Python dynamic?"
        )
        Choice.objects.create(
            question=self.question, text="Yes", is_correct=True
        )

    def test_exam_list(self):
        response = self.client.get(reverse("quiz:exam_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Computing")

    def test_exam_detail(self):
        response = self.client.get(
            reverse("quiz:exam_detail", args=[self.exam.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Is Python dynamic?")
        self.assertContains(response, "Yes")