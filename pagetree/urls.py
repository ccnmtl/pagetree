import os.path
from django.urls import re_path
from pagetree.views import (
    reorder_pageblocks, reorder_section_children, add_child_section,
    add_pageblock, edit_pageblock, delete_section, edit_section,
    delete_pageblock,
)


media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    re_path(r'^reorder_pageblocks/(?P<section_id>\d+)/$',
            reorder_pageblocks, {}, "reorder-pageblocks"),
    re_path(r'^reorder_section_children/(?P<section_id>\d+)/$',
            reorder_section_children, {}, "reorder-section-children"),
    re_path(r'^section/add/(?P<section_id>\d+)/$',
            add_child_section, {}, "add-child-section"),
    re_path(r'^pageblock/add/(?P<section_id>\d+)/$',
            add_pageblock, {}, "add-pageblock"),
    re_path(r'^pageblock/edit/(?P<pageblock_id>\d+)/$',
            edit_pageblock, {}, "edit-pageblock"),
    re_path(r'^delete_section/(?P<section_id>\d+)/$',
            delete_section, {}, "delete-section"),
    re_path(r'^edit_section/(?P<section_id>\d+)/$',
            edit_section, {}, "edit-section"),
    re_path(r'^delete_pageblock/(?P<pageblock_id>\d+)/$',
            delete_pageblock, {}, "delete-pageblock"),
]
