# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from core.utils import validate_status
from gsi.models import Run, RunStep, CardSequence, OrderedCardItem
from cards.models import CardItem

# update the status of the runs
# <RUN_ID>.<SEQUENCE_ID>.<CARD_ID>
# example:
# http://indy4.epcc.ed.ac.uk:/run/20.5.1/?status=running

@api_view(['GET'])
def update_run(request, run_id):
    """ update the status cards of the runs """

    data = validate_status(request.query_params.get('status', False))
    value_list = run_id.split('.')

    if data['status']:
        state = data['status']
        try:
            run = Run.objects.get(id=value_list[0])
            sequence = CardSequence.objects.get(id=value_list[1])
            card = OrderedCardItem.objects.get(id=value_list[2])
            step = RunStep.objects.get(
                parent_run=run,
                card_item=card)
            # step.state = state
            # run.state = state
            # step.save()
            # run.save()

            # Go to the next step only on success state
            if state == 'success':
                next_step, is_last_step = step.get_next_step()

                if next_step:
                    data['next_step'] = next_step.id
                if is_last_step:
                    data['is_last_step'] = True
                    step.state = 'success'
                    # run = step.parent_run
                    run.state = 'success'
                    step.save()
                    run.save()
            else:
                step.state = state
                # run = step.parent_run
                run.state = state
                step.save()
                run.save()

        except ObjectDoesNotExist as e:
            data['status'] = False
            data['message'] = str(e)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def update_step(request, step_id):
    """ update the status of the cards """

    data = validate_status(request.query_params.get('status', False))
    if data['status']:
        state = data['status']
        try:
            step = RunStep.objects.get(pk=step_id)
            step.state = state
            step.save()
            # Go to the next step only on success state
            if state == 'success':
                next_step, is_last_step = step.get_next_step()
                if next_step:
                    data['next_step'] = next_step.id
                if is_last_step:
                    data['is_last_step'] = True
                    # TODO: possibly finish the run (discuss)
                    # run = step.parent_run
                    # run.status = 'success'
                    # run.save()
        except ObjectDoesNotExist as e:
            data['status'] = False
            data['message'] = str(e)
    else:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_200_OK)