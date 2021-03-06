from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from pagetree.models import Section, PageBlock
from django.template.defaultfilters import slugify


def reorder_pageblocks(request, section_id, id_prefix="pageblock_id_"):
    if request.method != "POST":
        return HttpResponse("only use POST for this")
    section = get_object_or_404(Section, id=section_id)
    keys = list(request.GET.keys())
    keys.sort(key=lambda x: int(x.split('_')[-1]))
    pageblocks = [int(request.GET[k]) for k in keys if k.startswith(id_prefix)]
    section.update_pageblocks_order(pageblocks)
    return HttpResponse("ok")


def reorder_section_children(request, section_id, id_prefix="section_id_"):
    if request.method != "POST":
        return HttpResponse("only use POST for this")
    section = get_object_or_404(Section, id=section_id)
    keys = list(request.GET.keys())
    keys.sort(key=lambda x: int(x.split('_')[-1]))
    children = [int(request.GET[k]) for k in keys if k.startswith(id_prefix)]
    section.update_children_order(children)
    return HttpResponse("ok")


def delete_pageblock(request, pageblock_id, success_url=None):
    block = get_object_or_404(PageBlock, id=pageblock_id)
    section = block.section
    try:
        block.block().delete()
    except AttributeError:
        # if the model has been refactored, we sometimes
        # end up with 'stub' pageblocks floating around
        # that no longer have a block object associated
        # it's nice to still be able to delete them
        # without having to scrap the whole db and start over
        pass
    block.delete()
    section.renumber_pageblocks()
    if success_url is None:
        success_url = "/edit" + section.get_absolute_url()
    return HttpResponseRedirect(success_url)


def edit_pageblock(request, pageblock_id, success_url=None):
    block = get_object_or_404(PageBlock, id=pageblock_id)
    section = block.section
    block.edit(request.POST, request.FILES)
    if success_url is None:
        success_url = "/edit" + section.get_absolute_url()
    return HttpResponseRedirect(success_url)


def edit_section(request, section_id, success_url=None):
    section = get_object_or_404(Section, id=section_id)
    section.label = request.POST.get('label', '')
    section.slug = request.POST.get('slug', slugify(section.label))
    section.save()
    if success_url is None:
        success_url = "/edit" + section.get_absolute_url()
    return HttpResponseRedirect(success_url)


def delete_section(request, section_id, success_url=None):
    section = get_object_or_404(Section, id=section_id)
    if request.method == "POST":
        parent = section.get_parent()
        section.delete()
        if success_url is None:
            success_url = "/edit" + parent.get_absolute_url()
        return HttpResponseRedirect(success_url)
    return HttpResponse("""
<html><body><form action="." method="post">Are you Sure?
<input type="submit" value="Yes, delete it" /></form></body></html>
""")


def add_pageblock(request, section_id, success_url=None):
    section = get_object_or_404(Section, id=section_id)
    blocktype = request.POST.get('blocktype', '')
    # now we need to figure out which kind of pageblock to create
    for pb_class in section.available_pageblocks():
        if pb_class.display_name == blocktype:
            # a match
            block = pb_class.create(request)
            section.append_pageblock(
                label=request.POST.get('label', ''),
                content_object=block)
    if success_url is None:
        success_url = "/edit" + section.get_absolute_url()
    return HttpResponseRedirect(success_url)


def add_child_section(request, section_id, success_url=None):
    section = get_object_or_404(Section, id=section_id)
    section.append_child(request.POST.get('label', 'unnamed'),
                         request.POST.get('slug', ''))
    if success_url is None:
        success_url = "/edit" + section.get_absolute_url()
    return HttpResponseRedirect(success_url)
