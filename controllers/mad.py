# -*- coding: utf-8 -*-

"""
    Mobile Assessment of Damage

    @author: Pat Tressel
"""

# Administrators can view existing assessments and create assessments.
# Non-admins can only add assessments and update the newly created assessment.
# They cannot currently alter an assessment once created.

module = request.controller
resourcename = request.function

if module not in deployment_settings.modules:
    session.error = T("Module disabled!")
    redirect(URL(r=request, c="default", f="index"))

# Options Menu (available in all Functions' Views)
def shn_menu():
    """ Options Menu """
    if s3_has_role(1):
        menu = [
            [T("Residence Assessments"), False, URL(r=request, f="residence"), [
                [T("List"), False, URL(r=request, f="residence")],
                [T("Add"), False, URL(r=request, f="residence", args="create")],
                # @ToDo Search by person, county
                #[T("Search"), False, URL(r=request, f="residence", args="search")],
            ]],
            [T("Business Property Assessments"), False, URL(r=request, f="business"), [
                [T("List"), False, URL(r=request, f="business")],
                [T("Add"), False, URL(r=request, f="business", args="create")],
                # @ToDo Search by person, county
                #[T("Search"), False, URL(r=request, f="business", args="search")],
            ]],
            #[T("Reports"), False, "#", [
            #    [T("Map of Assessments"), False, URL(r=request, f="assessment_map")],
            #    [T("Estimated Damage"), False, URL(r=request, f="estimated_damage")],
            #]],
        ]
    else:
        menu = [
            [T("Add assessment for a residence"), False, URL(r=request, f="residence", args="create")],
            [T("Add assessment for a business property"), False, URL(r=request, f="business", args="create")],
        ]
    response.menu_options = menu

shn_menu()

# S3 framework functions

# -----------------------------------------------------------------------------
def index():
    """ Module's Home Page """

    response.view = "mad/index.html"
    module_name = deployment_settings.modules[module].name_nice
    response.title = module_name

    return dict(module_name=module_name)

# -----------------------------------------------------------------------------
def shn_mad_rheader(r, rheader_table, tabs=[]):
    """ Resource headers """

    # If we don't have a record, e.g. this is a list or create form,
    # we should not show tabs.
    if r.record is None:
        return None

    if r.representation == "html":
        rheader_tabs = shn_rheader_tabs(r, tabs)
        rheader = DIV(rheader_table(r), rheader_tabs)
        return rheader

    return None

# -----------------------------------------------------------------------------
def generic(resourcename, rheader_table, list_fields):
    """ Common code in controllers """

    #from pprint import pformat
    #print >> sys.stderr, pformat(request.post_vars)
    #print >> sys.stderr, pformat(request.args)

    tablename = "%s_%s" % (module, resourcename)
    s3xrc.model.configure(db[tablename],
        create_next = URL(r=request, c=module, f=resourcename, args=["[id]"]),
        list_fields=list_fields)

    resource_image = "%s_image" % resourcename
    #print >> sys.stderr, "In mad generic, resource_image = %s" % resource_image
    resource_tabs = [(T("Basic Details"), None),
                     (T("Add Images"), resource_image)]
    rheader = lambda r: shn_mad_rheader(r, rheader_table=rheader_table, tabs=resource_tabs)

    #print >> sys.stderr, "pre rest controller"
    output = s3_rest_controller(module, resourcename,
                                rheader=rheader)
    #print >> sys.stderr, "post rest controller"
    #print >> sys.stderr, "---- output ----"
    #print >> sys.stderr, output

    return output

# -----------------------------------------------------------------------------
def residence():
    """ RESTful CRUD controller """

    def rheader_table(r):
        if r.record:
            return TABLE( TR( TH("%s: %s %s %s" % (T("Name"),
                                                   r.record.first_name,
                                                   r.record.middle_name,
                                                   r.record.last_name)),
                              TH("%s: %s %s" % (T("Address"),
                                                r.record.street1,
                                                r.record.street2))))
        return None

    list_fields = ["first_name", "middle_name", "last_name",
                   "address1", "address2", "city", "county"]

    return generic(resourcename, rheader_table, list_fields)

# -----------------------------------------------------------------------------
def business():
    """ RESTful CRUD controller """

    def rheader_table(r):
        if r.record:
            return TABLE( TR( TH("%s: %s" % (T("Name"),
                                             r.record.business_name)),
                              TH("%s: %s %s" % (T("Address"),
                                                r.record.street1,
                                                r.record.street2))))
        return None

    list_fields = ["business_name", "owner_name",
                   "address1", "address2", "city", "county"]

    return generic(resourcename, rheader_table, list_fields)
