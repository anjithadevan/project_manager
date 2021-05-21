from django.db.models.signals import pre_save
from django.dispatch import receiver
from projects.models import LogActualHourEdit, Project
import inspect


@receiver(pre_save, sender=Project)
def create_user_profile(sender, instance, **kwargs):
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    if request:
        try:
            product = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            LogActualHourEdit.objects.create(changed_by=request.user, initial_value=instance.total_actual_hours,
                                             change_delta=0, final_value=instance.total_actual_hours)
        else:
            initial_value = product.total_actual_hours
            final_value = instance.total_actual_hours
            difference = final_value - initial_value
            if difference:
                LogActualHourEdit.objects.create(changed_by=request.user, initial_value=initial_value,
                                                 change_delta=difference, final_value=final_value)


