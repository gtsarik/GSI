# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.conf import settings

# from cards.models import QRF, RFScore
from cards.cards_forms import *


def qrf_card_update_create(form, qrf_id=None):
    if qrf_id:
        QRF.objects.filter(id=qrf_id).update(
            name=form.cleaned_data["name"],
            interval=form.cleaned_data["interval"],
            number_of_trees=form.cleaned_data["number_of_trees"],
            number_of_threads=form.cleaned_data["number_of_threads"],
            directory=form.cleaned_data["directory"],
        )
        qrf_card = QRF.objects.get(id=qrf_id)
    else:
        qrf_card = QRF.objects.create(
            name=form.cleaned_data["name"],
            interval=form.cleaned_data["interval"],
            number_of_trees=form.cleaned_data["number_of_trees"],
            number_of_threads=form.cleaned_data["number_of_threads"],
            directory=form.cleaned_data["directory"],
        )

    return qrf_card


@login_required
@render_to('cards/processing_card_new_run.html')
def proces_card_new_run(request):
    title = 'Create New Processing Cards'

    if request.method == "POST":
        if request.POST.get('qrf_button') is not None:
            return HttpResponseRedirect(reverse('new_run_qrf'))
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(reverse('new_run'))

    data = {
        'title': title,
    }

    return data


@login_required
@render_to('cards/proces_card_sequence_card_edit.html')
def proces_card_sequence_card_edit(request, run_id, cs_id):
    title = 'Create New Processing Cards'

    if request.method == "POST":
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                reverse('card_sequence_update', args=[run_id, cs_id])
            )

    data = {
        'title': title,
        'run_id': run_id,
        'cs_id': cs_id,
    }

    return data


@login_required
@render_to('cards/proces_card_sequence_card_new.html')
def proces_card_sequence_card_new(request, run_id):
    title = 'Create New Processing Cards'

    if request.method == "POST":
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                reverse('add_card_sequence', args=[run_id])
            )

    data = {
        'title': title,
        'run_id': run_id,
    }

    return data


@login_required
@render_to('cards/new_run_qrf.html')
def new_run_qrf(request):
    title = 'New QRF Card'
    form = None

    if request.method == "POST":
        if request.POST.get('save_button') is not None:
            form = QRFForm(request.POST)

            if form.is_valid():
                qrf_card = qrf_card_update_create(form)

                return HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse('proces_card_new_run'),
                        (u"The QRF Card {0} created successfully".format(qrf_card.name)))
                )
        elif request.POST.get('save_and_another_button') is not None:
            form = QRFForm(request.POST)

            if form.is_valid():
                qrf_card = qrf_card_update_create(form)

                return HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse('new_run_qrf'),
                        (u"The QRF Card {0} was added successfully. \
                        You may add another qrf below".format(qrf_card.name)))
                )
        elif request.POST.get('save_and_continue_editing_button') is not None:
            form = QRFForm(request.POST)

            if form.is_valid():
                qrf_card = qrf_card_update_create(form)

                return HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse('new_run_qrf_edit', args=[qrf_card.id]),
                        (u"The QRF Card {0} was added successfully. \
                        You may add another QRF Card below".format(qrf_card.name)))
                )
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse('proces_card_new_run'),
                    (u"The QRF Card created canceled"))
            )
    else:
        form = QRFForm()

    data = {
        'title': title,
        'form': form,
    }

    return data


@login_required
@render_to('cards/new_run_qrf_edit.html')
def new_run_qrf_edit(request, qrf_id):
    title = 'New QRF Card'
    qrf_card = get_object_or_404(QRF, pk=qrf_id)
    form = None

    if request.method == "POST":
        if request.POST.get('save_button') is not None:
            form = QRFForm(request.POST)

            if form.is_valid():
                qrf_card = qrf_card_update_create(form, qrf_id)

                return HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse('proces_card_new_run'),
                        (u"The QRF Card {0} created successfully".format(qrf_card.name)))
                )
        elif request.POST.get('save_and_another_button') is not None:
            form = QRFForm(request.POST)

            if form.is_valid():
                qrf_card = qrf_card_update_create(form, qrf_id)

                return HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse('new_run_qrf'),
                        (u"The QRF Card {0} was added successfully. \
                        You may add another qrf below".format(qrf_card.name)))
                )
        elif request.POST.get('save_and_continue_editing_button') is not None:
            form = QRFForm(request.POST)

            if form.is_valid():
                qrf_card = qrf_card_update_create(form, qrf_id)

                return HttpResponseRedirect(
                        u'%s?status_message=%s' % (reverse('new_run_qrf_edit', args=[qrf_id]),
                        (u"The QRF Card {0} was added successfully. \
                        You may add another QRF Card below".format(qrf_card.name)))
                )
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse('proces_card_new_run'),
                    (u"The QRF Card created canceled"))
            )
    elif isinstance(qrf_card, QRF):
        form = QRFForm(instance=qrf_card)

    data = {
        'title': title,
        'form': form,
        'qrf_id': qrf_id,
    }

    return data