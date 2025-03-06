from django.contrib import admin

from .models import Bus, BusLog, BusRoute, Route, Station, StationAssignment

class BusRouteInline(admin.StackedInline):
    model = BusRoute

class BusLogInline(admin.StackedInline):
    model = BusLog

class StationAssignmentInline(admin.StackedInline):
    model = StationAssignment

class BusAdmin(admin.ModelAdmin):
    model = Bus
    inlines = [BusRouteInline, BusLogInline]

class RouteAdmin(admin.ModelAdmin):
    model = Route
    inlines = [StationAssignmentInline]

class StationAdmin(admin.ModelAdmin):
    model = Station

class BusLogAdmin(admin.ModelAdmin):
    model = BusLog

class BusRouteAdmin(admin.ModelAdmin):
    model = BusRoute

class StationAssignmentAdmin(admin.ModelAdmin):
    model = StationAssignment

admin.site.register(Bus, BusAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(BusLog, BusLogAdmin)
admin.site.register(BusRoute, BusRouteAdmin)
admin.site.register(StationAssignment, StationAssignmentAdmin)