from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Notice, Announcement


@admin.register(Notice)
class NoticeAdmin(ModelAdmin):
    list_display = (
        'id',
        'title',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
    )

    list_filter = (
        'created_at',
    )

    ordering = ('-created_at',)

    list_per_page = 20

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Notice Information', {
            'fields': (
                'title',
                'description',
            )
        }),

        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )


@admin.register(Announcement)
class AnnouncementAdmin(ModelAdmin):
    list_display = (
        'text',
        'order',
        'is_active',
        'created_at',
    )

    list_editable = (
        'order',
        'is_active',
    )

    search_fields = (
        'text',
    )

    list_filter = (
        'is_active',
        'created_at',
    )

    ordering = ('order', '-created_at')

    list_per_page = 20

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('ঘোষণা / রানিং বার্তা', {
            'fields': (
                'text',
                'order',
                'is_active',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )
