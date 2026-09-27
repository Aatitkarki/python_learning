"""Authoring helpers; generated notebooks are the learner-facing course."""
from textwrap import dedent

LESSONS = []

def exercise(title, task, starter, answer, checks, hint, why):
    return dict(title=title, task=task, starter=dedent(starter).strip(), answer=dedent(answer).strip(), checks=dedent(checks).strip(), hint=hint, why=why)

def lesson(id, title, group, objectives, theory, example, exercises, transfer, oral, reading):
    LESSONS.append(dict(id=id, title=title, group=group, objectives=objectives, theory=dedent(theory).strip(), example=dedent(example).strip(), exercises=exercises, transfer=transfer, oral=oral, reading=reading))
