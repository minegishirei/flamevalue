from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'design', 'short_tips.design_urls', name='design'),
    host(r'shortcutkey', 'short_tips.shortcutkey_urls', name='shortcutkey'),
    host(r'dialogue', 'short_tips.dialogue_urls', name='dialogue'),
    host(r'wordeffect', 'short_tips.wordeffect_urls', name='wordeffect')
)