from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ChoiceFormSet, ExamForm, QuestionForm
from .models import Exam


def exam_list(request):
    exams = Exam.objects.all()
    return render(request, "quiz/exam_list.html", {"exams": exams})


def exam_detail(request, pk):
    exam = get_object_or_404(
        Exam.objects.prefetch_related("questions__choices"), pk=pk
    )
    return render(request, "quiz/exam_detail.html", {"exam": exam})


def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            question = form.save()
            formset.instance = question
            formset.save()
            return redirect(reverse("quiz:exam_detail", args=[question.exam.pk]))
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()
    return render(request, "quiz/question_create.html", {"form": form, "formset": formset})