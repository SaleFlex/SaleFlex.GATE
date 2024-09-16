from django.db import models
from django.contrib.auth.models import User


class PosFormControl(models.Model):
    """
    Represents individual controls within a POS form. Each control has a variety of
    configuration options to customize its appearance and functionality.
    """

    # Foreign key to the form that this control belongs to
    form = models.ForeignKey('PosForm', on_delete=models.CASCADE, related_name='controls')

    # Optional foreign key to the parent control, if this control is nested within another
    parent_control = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_controls')

    # Control name and parent name
    name = models.CharField(max_length=255)
    parent_name = models.CharField(max_length=255, null=True, blank=True)

    # Primary and secondary functions for the control
    form_control_function1 = models.CharField(max_length=255)
    form_control_function2 = models.CharField(max_length=255, null=True, blank=True)

    # Control type number and description
    control_type_no = models.IntegerField(null=True, blank=True)
    control_type = models.CharField(max_length=50, default='NOTYPE')

    # Control dimensions
    width = models.IntegerField()
    height = models.IntegerField()

    # Control position on the form
    location_x = models.IntegerField()
    location_y = models.IntegerField()

    # Control start position and captions
    start_position = models.CharField(max_length=50, null=True, blank=True)
    caption1 = models.CharField(max_length=255, null=True, blank=True)
    caption2 = models.CharField(max_length=255, null=True, blank=True)

    # List items for the control (if applicable)
    control_list = models.TextField(null=True, blank=True)

    # Control docking and alignment
    dock = models.CharField(max_length=50, null=True, blank=True)
    alignment = models.CharField(max_length=50, null=True, blank=True)
    text_alignment = models.CharField(max_length=50, default='LEFT')

    # Text casing and font settings
    character_casing = models.CharField(max_length=50, default='NORMAL')
    font = models.CharField(max_length=100, default='Tahoma')

    # Optional control icon and tooltip
    icon = models.CharField(max_length=255, null=True, blank=True)
    tool_tip = models.CharField(max_length=255, null=True, blank=True)

    # Control images (default and selected)
    image = models.CharField(max_length=255, null=True, blank=True)
    image_selected = models.CharField(max_length=255, null=True, blank=True)

    # Font settings
    font_auto_height = models.BooleanField(default=True)
    font_size = models.FloatField(default=0)

    # Input type (e.g., 'NUMERIC', 'TEXT')
    input_type = models.CharField(max_length=50, default='NUMERIC')

    # Text and image relationship settings
    text_image_relation = models.CharField(max_length=50, default='Overlay')

    # Control colors
    back_color = models.CharField(max_length=50, default='Gray')
    fore_color = models.CharField(max_length=50, default='Black')

    # Keyboard value associated with the control
    keyboard_value = models.CharField(max_length=255, null=True, blank=True)

    # Relationships with POS, Store, and Merchant
    pos = models.ForeignKey('PointOfSale', on_delete=models.SET_NULL, null=True, blank=True, related_name='form_controls')
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='form_controls')
    merchant = models.ForeignKey('Merchant', on_delete=models.SET_NULL, null=True, blank=True, related_name='form_controls')

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='label_value_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='label_value_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PosFormControl'
        unique_together = ('form', 'name', 'pos', 'store', 'merchant')  # Ensures no duplicate controls for the same form/pos/store/merchant
